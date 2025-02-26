from paper_processing import PaperProcessor
import json

def test_paper_processing():
    try:
        # Initialize paper processor
        processor = PaperProcessor()
        
        # Test with a small sample text as PDF content
        sample_text = """
        Title: Understanding AI's Impact on Society
        
        Abstract: This paper examines the societal implications of artificial intelligence,
        focusing on its effects on employment, privacy, and ethical considerations.
        Our research indicates that while AI brings significant benefits, careful
        consideration must be given to its implementation and regulation.
        """
        
        # Save sample text as a temporary PDF file
        with open('test.pdf', 'w') as f:
            f.write(sample_text)
        
        # Process the test PDF
        result = processor.process_pdf('test.pdf')
        
        # Print the result
        print("\nGenerated Podcast Script:")
        print(result)
        
        # Try to parse as JSON to verify format
        try:
            json_result = json.loads(result)
            print("\nSuccessfully generated valid JSON podcast script!")
            
            # Print first few exchanges
            print("\nFirst few exchanges:")
            for i, exchange in enumerate(json_result[:4]):
                print(f"{exchange['voice']}: {exchange['text']}")
                if i >= 3:
                    break
                    
        except json.JSONDecodeError:
            print("\nWarning: Output is not in JSON format")
            print("Raw output:", result)
            
    except Exception as e:
        print(f"Error during test: {str(e)}")
    finally:
        # Clean up test file
        import os
        if os.path.exists('test.pdf'):
            os.remove('test.pdf')

if __name__ == "__main__":
    test_paper_processing()