import os
import subprocess
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "whisper-1")
SEGMENT_LENGTH = int(os.getenv("SEGMENT_LENGTH", 300))

def split_audio(file_path, segment_length=SEGMENT_LENGTH):
    """
    Splits the audio file into segments.
    Each segment will be `segment_length` seconds long.
    """
    split_files = []
    base, ext = os.path.splitext(file_path)
    total_duration = get_audio_duration(file_path)
    for start in range(0, total_duration, segment_length):
        end = min(start + segment_length, total_duration)
        split_file = f"{base}_{start}_{end}{ext}"
        split_files.append(split_file)
        subprocess.run([
            "ffmpeg", "-i", file_path, "-ss", str(start), "-to", str(end),
            "-c", "copy", split_file
        ])
    return split_files

def get_audio_duration(file_path):
    """
    Returns the duration of the audio file in seconds.
    """
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "format=duration", "-of",
         "default=noprint_wrappers=1:nokey=1", file_path],
        text=True, capture_output=True
    )
    return int(float(result.stdout.strip()))

def transcribe_audio(file_path):
    """
    Transcribes the audio file using OpenAI's Whisper API.
    """
    client = OpenAI(api_key=OPENAI_API_KEY)
    with open(file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model=WHISPER_MODEL,
            file=audio_file
        )
    return transcript["text"]

def main(audio_file, output_file):
    # Split the audio file
    segments = split_audio(audio_file)

    # Transcribe each segment
    transcriptions = [transcribe_audio(segment) for segment in segments]

    # Merge transcriptions and save to a file
    with open(output_file, 'w') as f:
        f.write("\n".join(transcriptions))

    # Optional: Clean up split files
    for segment in segments:
        os.remove(segment)

if __name__ == "__main__":
    main("path_to_your_30min_audio_file.m4a", "transcription.txt")
