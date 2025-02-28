import streamlit as st
import os
import tempfile
from datetime import datetime
from paper_processing import PaperProcessor

# Set page config and custom styling
st.set_page_config(
    page_title="PaperCast-AI",
    page_icon="🎙️",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton > button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #FF4B4B;
        color: white;
    }
    .stButton > button:hover {
        background-color: #FF6B6B;
        color: white;
    }
    .status-box {
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    # Header section with description
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🎙️ PaperCast-AI")
        st.markdown("""
        Transform research papers into engaging audio content! Upload your PDF and let AI do the work.
        
        **Features:**
        - 📄 PDF text extraction
        - 🤖 AI-powered summarization
        - 🎧 Natural voice synthesis
        """)
    
    # Initialize the paper processor
    processor = PaperProcessor()

    # File upload section with improved styling
    st.markdown("### 📎 Upload Your Paper")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None:
        # Create a temporary file to store the PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            pdf_path = tmp_file.name

        try:
            # Enhanced PDF preview
            with st.expander("📑 Document Details", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**File Information**")
                    st.write(f"📄 Name: {uploaded_file.name}")
                    st.write(f"📦 Size: {uploaded_file.size / 1024:.2f} KB")
                with col2:
                    st.markdown("**Processing Status**")
                    st.write("✅ File uploaded successfully")
                    st.write("⏳ Ready for conversion")

            # Convert to Podcast button with improved styling
            st.markdown("### 🎯 Generate Podcast")
            if st.button("Start Processing"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                with st.spinner(""):
                    try:
                        # Process the PDF
                        status_text.text("📚 Analyzing the paper...")
                        progress_bar.progress(25)
                        summary = processor.process_pdf(pdf_path)
                        progress_bar.progress(50)
                        
                        # Show script generation success
                        status_text.text("✅ Script generated successfully!")
                        
                        # Save the summary
                        status_text.text("💾 Saving the script...")
                        progress_bar.progress(75)
                        json_path = "podcast_script.json"
                        with open(json_path, 'w') as f:
                            f.write(summary)

                        # Generate audio
                        status_text.text("🔊 Generating audio...")
                        os.system(f"python podcast_generation.py")
                        progress_bar.progress(100)
                        status_text.text("✨ Processing complete!")
                        
                        # Audio player and download section
                        if os.path.exists("podcast.wav"):
                            st.markdown("### 🎧 Your Podcast")
                            st.audio("podcast.wav")
                            
                            # Download audio option
                            st.markdown("### 📥 Download Audio")
                            with open("podcast.wav", "rb") as f:
                                st.download_button(
                                    label="📁 Download Audio (WAV)",
                                    data=f,
                                    file_name=f"podcast_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav",
                                    mime="audio/wav"
                                )
                        else:
                            st.error("❌ Audio generation failed. Please try again.")
                            
                    except Exception as e:
                        st.error(f"❌ Error during processing: {str(e)}")
                        progress_bar.empty()
                        status_text.empty()
        finally:
            # Clean up temporary file
            if os.path.exists(pdf_path):
                os.unlink(pdf_path)

if __name__ == "__main__":
    main()