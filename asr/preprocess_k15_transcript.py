import os
import sys
import argparse
import random
import unicodedata
import glob
import librosa

parser = argparse.ArgumentParser()

parser.add_argument("data_dir", type=str, help="Dataset dir")

args = parser.parse_args()

audio_files = glob.glob(os.path.join(os.path.abspath(args.data_dir), "**", "*.wav"), recursive=True)

with open(os.path.join(args.data_dir, "transcripts.tsv"), "w", encoding="utf-8") as t:
    t.write("PATH\tDURATION\tTRANSCRIPT\n")
    for idx, audio_file in enumerate(audio_files, 1):
        transcript_file = os.path.join(os.path.dirname(audio_file), f"{os.path.splitext(os.path.basename(audio_file))[0]}.txt")
        if not os.path.exists(transcript_file):
            continue
        with open(transcript_file, "r", encoding="utf-8") as i:
            transcript = i.read()
        transcript = unicodedata.normalize("NFC", transcript.lower())
        transcript = transcript.replace("\n", "")

        y, sr = librosa.load(audio_file, sr=None)
        duration = librosa.core.get_duration(y, sr=sr)

        t.write(f"{audio_file}\t{duration:.2f}\t{transcript}\n")

        sys.stdout.write("\033[K")
        print(f"\rProcessed {idx}/{len(audio_files)}: {audio_file}", end="")
