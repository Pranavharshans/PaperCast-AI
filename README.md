# 🎙️ PaperCast-AI

PaperCast-AI is an innovative application that transforms research papers into engaging podcast-style conversations. It uses AI to convert complex academic content into accessible, entertaining audio content with natural-sounding voices.

## 🌟 Features

- 📄 PDF Text Extraction: Upload and process any research paper in PDF format
- 🤖 AI-Powered Summarization: Converts technical content into conversational dialogue using Google's Gemini AI
- 🎧 Natural Voice Synthesis: Generates human-like voices using Kokoro TTS
- 🎯 Interactive Web Interface: User-friendly Streamlit application
- 🔄 Dynamic Content Scaling: Automatically adjusts content length based on paper size
- 🗣️ Multi-Voice Conversation: Simulates engaging dialogue between two hosts (Sarah and Michael)

## ⚙️ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/PaperCast-AI.git
cd PaperCast-AI
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install Kokoro TTS dependencies:
```bash
pip install kokoro-onnx soundfile
```

4. Download required model files:
```bash
wget https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
wget https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
```

## 🔑 Configuration

1. Create a `.env` file in the project root:
```bash
GOOGLE_API_KEY=your_google_api_key_here
```

2. Ensure the voices.json file is present in the project directory (used by Kokoro TTS)

## 🚀 Usage

1. Start the Streamlit application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the displayed URL (typically http://localhost:8501)

3. Upload your research paper (PDF format)

4. Click "Start Processing" to begin the conversion

5. Wait for the processing to complete:
   - Text extraction and analysis
   - Script generation
   - Audio synthesis

6. Listen to or download the generated podcast

## 🛠️ Technical Details

- **Frontend**: Streamlit
- **AI Model**: Google Gemini 2.0 Flash
- **Text-to-Speech**: Kokoro TTS
- **Audio Processing**: SoundFile and NumPy
- **File Processing**: PyPDF2

## ⚠️ Important Notes

- Requires a valid Google API key for Gemini AI
- Processing time varies based on paper length
- Generated audio is saved as WAV format
- Minimum conversation length is 40 exchanges

## 📝 System Requirements

- Python 3.8 or higher
- Sufficient disk space for model files
- Internet connection for AI processing
- Modern web browser for interface

## 🔮 Future Enhancements

### Complete Local Operation
- Replace Gemini AI with a local LLM for offline processing:


### Enhanced Text-to-Speech
- Implement advanced TTS capabilities:
  * Improved prosody and emotional expression
  * Support for multiple languages and accents
  * Better conversation flow with natural pauses and intonation

### System Improvements
- Offline operation support
- Reduced system resource requirements
- Faster processing times
- Enhanced audio quality control

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests, report bugs, and suggest features.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
