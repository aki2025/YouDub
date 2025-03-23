# YouDub - YouTube Video Dubbing Tool

**YouDub** is a free, open-source Python tool that dubs YouTube videos into different languages (e.g., English to Hindi) and saves the result locally. It uses state-of-the-art models for transcription, translation, and text-to-speech, all running locally at no cost.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/username/YouDub.git
   cd YouDub
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Ensure FFmpeg is installed and accessible in your PATH.

## Usage

Run the script with:

```bash
python youdub.py --url "https://www.youtube.com/watch?v=example" --source_lang "en" --target_lang "hi"
```

### Options

- `--url`: YouTube video URL (required).
- `--source_lang`: Source language code (e.g., "en" for English).
- `--target_lang`: Target language code (e.g., "hi" for Hindi).
- `--output_file`: Output file name (default: `output.mp4`).
- `--no-cleanup`: Keep intermediate files (default: cleans up).

### Example

```bash
python youdub.py --url "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --source_lang "en" --target_lang "hi" --output_file "dubbed_video.mp4"
```

## API

The main script `youdub.py` provides the following functionality:

- Downloads video and audio streams from YouTube.
- Transcribes audio into text.
- Translates text into the target language.
- Generates new audio using TTS.
- Syncs the audio duration with the original.
- Combines the new audio with the video.
- Saves the dubbed video and optionally cleans up intermediates.

## Acknologement

Whisper
Helsinki-NLP
Coqui TTS
pytube
FFmpeg

## Contributing

Submit pull requests or issues on GitHub!

## License

This project is licensed under the [MIT License](LICENSE).

## Testing

(Future plans for unit tests)
