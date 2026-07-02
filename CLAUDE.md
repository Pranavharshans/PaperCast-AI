# CLAUDE.md — PaperCast AI

Transforms research papers into podcast-style audio conversations using LLMs and Kokoro TTS.

## Pipeline

1. PDF text extraction
2. LLM script generation (podcast dialogue format)
3. Kokoro TTS voice synthesis for each speaker
4. Audio assembly and export

## Key files

- `app.py` — main Streamlit application
- Script generation uses LLM APIs
- Audio generation uses Kokoro ONNX TTS

## Running

```bash
pip install -r requirements.txt
streamlit run app.py
```

Set `GEMINI_API_KEY` or equivalent in `.env`.
