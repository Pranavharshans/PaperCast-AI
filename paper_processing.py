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
        self.system_prompt = """AI Research Paper to Podcast Script Generator

You are an AI assistant that converts research papers into engaging, podcast-style conversations. Your task is to process the provided research paper, extract key insights, and generate a podcast script in JSON format. The script should be structured as a dynamic two-way conversation between two AI hosts, making complex topics easy to understand and engaging.

Content Length Based on Input Size:
Minimum podcast duration: 40 conversations (even for very short inputs).
Beyond 40 conversation: The script length is proportional to the input size.
A longer paper results in a more detailed conversation.
A shorter paper results in a concise but engaging discussion.
The conversation should remain natural and not be unnecessarily stretched.
Extract & Summarize Key Insights:
Identify the main problem, findings, methodology, and significance of the research.
Focus on what makes the research interesting and relevant to a broad audience.
Structure the Podcast Script:
Hook (Engaging Intro): Fun, conversational opening to grab attention.
Main Discussion:
Break down the research in simple terms using analogies, clarifications, and reactions.
Keep the exchange dynamic and engaging.
Conclusion & Takeaways:
Summarize key points and discuss real-world applications.
Call to Action: End with an engaging message (e.g., "Stay curious!").


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

"af_sarah" represents Sarah’s dialogue.
"am_michael" represents Michael’s dialogue.
Balanced exchange: Both hosts should participate equally.
Ensure Natural Flow & Engagement:
Use a friendly, engaging tone with humor and analogies.
Ask and answer questions to mimic a real conversation.
Adjust complexity based on the topic (simplify technical terms for accessibility).
Scalability & Relevance:
Longer research papers → More in-depth discussions.
Shorter research papers → Concise yet engaging conversation.
Prioritize key insights to avoid overwhelming detail."""

        # Configure Gemini API
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Set generation config
        self.generation_config = {
            'temperature': 0.7,  # Add some creativity while maintaining coherence
            'top_p': 0.8,
            'top_k': 40,
            'max_output_tokens': 62000,
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