import streamlit as st
import os
import tempfile
from datetime import datetime
from paper_processing import PaperProcessor

def main():
    st.title("PaperCast-AI")
    st.subheader("Convert Research Papers to Podcasts")

    # Initialize the paper processor
    processor = PaperProcessor()

    # File upload section
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    
    if uploaded_file is not None:
        # Create a temporary file to store the PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            pdf_path = tmp_file.name

        try:
            # Display PDF preview
            with st.expander("Preview PDF", expanded=True):
                st.write("PDF Preview:")
                st.write(f"Filename: {uploaded_file.name}")
                st.write(f"Size: {uploaded_file.size} bytes")

            # Convert to Podcast button
            if st.button("Convert to Podcast"):
                with st.spinner("Processing your PDF..."):
                    try:
                        # Process the PDF
                        summary = processor.process_pdf(pdf_path)
                        
                        # Display the generated summary
                        st.subheader("Generated Summary")
                        st.write(summary)
                        
                        st.success("PDF processing complete!")

                        # TODO: Implement audio conversion from summary
                        # Audio player section (placeholder for now)
                        st.subheader("Listen to Podcast")
                        st.info("Audio conversion coming soon!")
                        
                        # Download button for summary (temporary)
                        st.download_button(
                            label="Download Summary",
                            data=summary,
                            file_name=f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            mime="text/plain"
                        )
                    except Exception as e:
                        st.error(f"Error processing PDF: {str(e)}")
        finally:
            # Clean up temporary file
            if os.path.exists(pdf_path):
                os.unlink(pdf_path)

if __name__ == "__main__":
    main()