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