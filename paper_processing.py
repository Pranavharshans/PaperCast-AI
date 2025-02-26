from google import genai
from google.genai import types
import pathlib

class PaperProcessor:
    def __init__(self):
        self.client = genai.Client()
    
    def process_pdf(self, pdf_path: str, prompt: str = "Summarize this document") -> str:
        """
        Process a PDF file and generate content using Gemini AI
        
        Args:
            pdf_path (str): Path to the PDF file
            prompt (str): Prompt for content generation
            
        Returns:
            str: Generated content
        """
        filepath = pathlib.Path(pdf_path)
        
        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[
                    types.Part.from_bytes(
                        data=filepath.read_bytes(),
                        mime_type='application/pdf',
                    ),
                    prompt
                ]
            )
            return response.text
        except Exception as e:
            raise Exception(f"Error processing PDF: {str(e)}")