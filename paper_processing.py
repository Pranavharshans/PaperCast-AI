import google.generativeai as genai
import pathlib
import os
from dotenv import load_dotenv
import json

class PaperProcessor:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Get API key from environment variable
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        # System prompt for podcast-style conversation
        self.system_prompt = """You are an AI assistant that converts research papers into engaging, podcast-style conversations. Your task is to process the provided research paper, extract key insights, and generate a podcast script in JSON format. The script should be structured as a dynamic two-way conversation between two AI hosts, making complex topics easy to understand and engaging.

Instructions:
Analyze Content Length:
- If the paper is short (1-3 pages) → Generate a 5-7 minute podcast (8-12 exchanges).
- If the paper is medium (4-10 pages) → Generate a 10-15 minute podcast (15-25 exchanges).
- If the paper is long (10+ pages) → Generate a 20+ minute podcast (30+ exchanges).

Extract & Summarize Key Insights:
- Identify the main problem, findings, methodology, and significance of the research.
- Focus on what makes the research interesting and relevant.

Structure the Podcast Script:
- Hook (Engaging Intro): Start with a fun, conversational opening.
- Main Discussion: Break down the research in simple terms with analogies, clarifications, and reactions.
- Conclusion & Takeaways: Summarize key points and discuss real-world applications.
- Call to Action: End with an engaging message.

Format Output as JSON:
- Use "af_sarah" for Sarah's dialogue and "am_michael" for Michael's dialogue.
- Each entry must have the format: {
  "voice": "af_sarah",
  "text": "Welcome back, listeners! Today, we're diving into an exciting topic: black hole physics. Ready, Michael?"
},
{
  "voice": "am_michael",
  "text": "Absolutely, Sarah! Black holes sound mysterious, but let's break them down in a way that makes sense!"
}

- Maintain a balanced exchange between both speakers.

Ensure Natural Flow & Engagement:
- Use a friendly, engaging tone with humor and analogies.
- Ask and answer questions to mimic a real conversation.
- Adjust complexity based on the topic (simplify technical terms).

Maintain Scalability:
- Ensure longer research papers result in proportionally longer podcasts without overwhelming detail.
- Prioritize the most impactful insights to keep the conversation engaging."""

        # Configure Gemini API
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Set generation config
        self.generation_config = {
            'temperature': 0.7,  # Add some creativity while maintaining coherence
            'top_p': 0.8,
            'top_k': 40,
            'max_output_tokens': 2048,
        }
    
    def process_pdf(self, pdf_path: str) -> str:
        """
        Process a PDF file and generate a podcast-style conversation using Gemini AI
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            str: JSON formatted podcast script
        """
        try:
            # Read the PDF file
            with open(pdf_path, 'rb') as file:
                file_content = file.read()

            # Create the prompt with system instructions
            prompt = f"{self.system_prompt}\n\nAnalyze the following research paper and generate a podcast script according to the instructions above.\n\nPaper content:"
            
            # Generate content with configuration
            response = self.model.generate_content(
                [prompt, {"mime_type": "application/pdf", "data": file_content}],
                generation_config=self.generation_config
            )
            
            if response.text:
                try:
                    # Try to parse and format as JSON
                    json_response = json.loads(response.text)
                    return json.dumps(json_response, indent=2)
                except json.JSONDecodeError:
                    # If not valid JSON, return the raw text
                    return response.text
            else:
                raise Exception("No response generated from the model")
        except Exception as e:
            raise Exception(f"Error processing PDF: {str(e)}")