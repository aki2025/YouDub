import argparse
import os
import shutil
import subprocess
import pytube
import whisper
from transformers import pipeline
from TTS.api import TTS
from pathlib import Path

# Constants
OUTPUT_DIR = Path("output")
TTS_MODELS_DIR = Path("tts_models")

# Ensure directories exist
OUTPUT_DIR.mkdir(exist_ok=True)
TTS_MODELS_DIR.mkdir(exist_ok=True)

def get_duration(file):
    """Get duration of a media file using ffprobe."""
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', file],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        return float(result.stdout.strip())
    except Exception as e:
        raise Exception(f"Failed to get duration of {file}: {e}")

def download_tts_model(language):
    """Download TTS model for the target language if not present."""
    model_name = f"tts_models/tts-1-{language}"  # Example: tts-1-hi for Hindi
    model_path = TTS_MODELS_DIR / language
    if not model_path.exists():
        print(f"Downloading TTS model for {language}...")
        tts = TTS(model_name=model_name, progress_bar=True)
        tts.download_model()
        shutil.move(tts.model_dir, model_path)
    return str(model_path / "model.pth"), str(model_path / "config.json")

def dub_video(url, source_lang, target_lang, output_file="output.mp4", cleanup=True):
    """Dub a YouTube video into another language."""
    try:
        # 1. Download video and audio
        print("Downloading YouTube video...")
        yt = pytube.YouTube(url)
        video_stream = yt.streams.filter(adaptive=True, only_video=True).first()
        audio_stream = yt.streams.filter(adaptive=True, only_audio=True).first()
        
        if not video_stream or not audio_stream:
            raise ValueError("No suitable video or audio streams found.")
        
        video_path = OUTPUT_DIR / "video.mp4"
        audio_path = OUTPUT_DIR / "audio.mp4"
        video_stream.download(output_path=str(OUTPUT_DIR), filename="video.mp4")
        audio_stream.download(output_path=str(OUTPUT_DIR), filename="audio.mp4")

        # 2. Transcribe audio
        print("Transcribing audio...")
        whisper_model = whisper.load_model("base")
        result = whisper_model.transcribe(str(audio_path), language=source_lang)
        transcription = result["text"]
        if not transcription:
            raise ValueError("Transcription failed or audio is silent.")

        # 3. Translate text
        print("Translating text...")
        try:
            translator = pipeline(f"translation_{source_lang}_to_{target_lang}", model=f"Helsinki-NLP/opus-mt-{source_lang}-{target_lang}")
        except Exception:
            print(f"Direct {source_lang} to {target_lang} translation not available. Using pivot through English.")
            translator_en = pipeline(f"translation_{source_lang}_to_en", model=f"Helsinki-NLP/opus-mt-{source_lang}-en")
            translator_target = pipeline(f"translation_en_to_{target_lang}", model=f"Helsinki-NLP/opus-mt-en-{target_lang}")
            text_en = translator_en(transcription)[0]["translation_text"]
            translated_text = translator_target(text_en)[0]["translation_text"]
        else:
            translated_text = translator(transcription)[0]["translation_text"]

        # 4. Generate new audio
        print("Generating dubbed audio...")
        tts_checkpoint, tts_config = download_tts_model(target_lang)
        tts = TTS(model_name=f"tts_models/tts-1-{target_lang}", progress_bar=True)
        new_audio_path = OUTPUT_DIR / "new_audio.wav"
        tts.tts_to_file(text=translated_text, file_path=str(new_audio_path))

        # 5. Sync audio
        print("Syncing audio...")
        original_duration = get_duration(str(audio_path))
        new_duration = get_duration(str(new_audio_path))
        speed_factor = original_duration / new_duration
        
        # Ensure speed factor is within FFmpeg's atempo limits (0.5 to 2.0)
        if not 0.5 <= speed_factor <= 2.0:
            print(f"Warning: Speed factor {speed_factor} outside FFmpeg atempo range. Clamping to 0.5-2.0.")
            speed_factor = max(0.5, min(2.0, speed_factor))
        
        adjusted_audio_path = OUTPUT_DIR / "adjusted_audio.wav"
        subprocess.run([
            'ffmpeg', '-i', str(new_audio_path), '-filter:a', f'atempo={speed_factor}', '-y',
            str(adjusted_audio_path)
        ], check=True)

        # 6. Combine video and audio
        print("Muxing video and audio...")
        final_output = OUTPUT_DIR / output_file
        subprocess.run([
            'ffmpeg', '-i', str(video_path), '-i', str(adjusted_audio_path), '-c:v', 'copy', '-c:a', 'aac', '-y',
            str(final_output)
        ], check=True)

        print(f"Dubbed video saved as {final_output}")

        # 7. Cleanup
        if cleanup:
            print("Cleaning up intermediate files...")
            for file in OUTPUT_DIR.glob("*.mp4"):
                if file != final_output:
                    file.unlink()
            for file in OUTPUT_DIR.glob("*.wav"):
                file.unlink()

    except Exception as e:
        print(f"Error: {e}")
        return False
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dub a YouTube video into another language.")
    parser.add_argument("--url", required=True, help="YouTube video URL")
    parser.add_argument("--source_lang", required=True, help="Source language code (e.g., 'en' for English)")
    parser.add_argument("--target_lang", required=True, help="Target language code (e.g., 'hi' for Hindi)")
    parser.add_argument("--output_file", default="output.mp4", help="Output file name (default: output.mp4)")
    parser.add_argument("--no-cleanup", action="store_false", dest="cleanup", help="Keep intermediate files")
    
    args = parser.parse_args()

    success = dub_video(
        url=args.url,
        source_lang=args.source_lang,
        target_lang=args.target_lang,
        output_file=args.output_file,
        cleanup=args.cleanup
    )
    if not success:
        print("Dubbing process failed. Check the error message above.")# YouDub main script 
