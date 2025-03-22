# YouDub - YouTube Video Dubbing Tool

**YouDub** is a free, open-source Python tool that dubs YouTube videos into different languages (e.g., English to Hindi) and saves the result locally. It uses state-of-the-art models for transcription, translation, and text-to-speech, all running locally at no cost.

---

## Features
- Downloads YouTube video and audio streams.
- Transcribes audio with Whisper (multi-language support).
- Translates text with Helsinki-NLP models (direct or pivot through English).
- Generates dubbed audio with Mozilla/Coqui TTS.
- Syncs and combines audio with video using FFmpeg.
- Customizable output file name and cleanup options.

---

## Prerequisites

- **Python 3.8+**
- **FFmpeg**: Install via:
  - Linux: `sudo apt-get install ffmpeg`
  - Mac: `brew install ffmpeg`
  - Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/username/YouDub.git
   cd YouDub# YouDub - YouTube Video Dubbing Tool 


Install dependencies:


pip install -r requirements.txt

Ensure FFmpeg is installed and accessible in your PATH.

Usage
Run the script with:


python youdub.py --url "https://www.youtube.com/watch?v=example" --source_lang "en" --target_lang "hi"

Options
--url: YouTube video URL (required).

--source_lang: Source language code (e.g., "en" for English).

--target_lang: Target language code (e.g., "hi" for Hindi).

--output_file: Output file name (default: output.mp4).

--no-cleanup: Keep intermediate files (default: cleans up).

Example


python youdub.py --url "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --source_lang "en" --target_lang "hi" --output_file "dubbed_video.mp4"

How It Works
Downloads video and audio streams from YouTube.

Transcribes audio into text.

Translates text into the target language.

Generates new audio using TTS.

Syncs the audio duration with the original.

Combines the new audio with the video.

Saves the dubbed video and optionally cleans up intermediates.

Directory Structure

YouDub/
├── youdub.py              # Main script
├── requirements.txt       # Dependencies
├── README.md              # Documentation
├── LICENSE                # MIT License
├── tts_models/            # Auto-downloaded TTS models
├── utils/                 # Helper functions (future)
├── tests/                 # Unit tests (future)
└── output/                # Generated files

Limitations
TTS Quality: Depends on available Coqui TTS models.

Syncing: Basic speed adjustment; no lip-sync precision.

Processing Time: Slow for long videos without GPU support.

Legal: Ensure compliance with YouTube’s terms and copyright laws.

Troubleshooting
FFmpeg Errors: Verify FFmpeg is installed and in PATH.

Model Download Fails: Check internet connection and Coqui TTS model availability.

Translation Issues: Ensure language codes are valid (e.g., "en", "hi").

Contributing
Submit pull requests or issues on GitHub!

Acknowledgments

Whisper
Helsinki-NLP
Coqui TTS
pytube
FFmpeg

---

### 4. `LICENSE`

---

### 5. `tts_models/README.md`

```markdown
# TTS Models Directory

This directory stores Text-to-Speech (TTS) models downloaded automatically by `youdub.py` using Coqui TTS. Each subdirectory corresponds to a language (e.g., `hi` for Hindi).

## Adding Models Manually

If a model isn’t auto-downloaded:
1. Find a compatible model from [Coqui TTS](https://github.com/coqui-ai/TTS).
2. Place the `model.pth` and `config.json` files in a subdirectory named after the language code (e.g., `hi/`).
3. The script will use these if present.

## Notes

- Models are downloaded on-demand when a new target language is specified.
- Ensure sufficient disk space for model files (~500MB each).