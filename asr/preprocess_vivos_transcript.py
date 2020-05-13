import argparse
import os
import glob
import librosa

parser = argparse.ArgumentParser(description="Preprocess transcript for vivos dataset")

parser.add_argument("--transcript", "-t", type=str, help="transcript file")
parser.add_argument("--output", "-o", type=str, help="Output transcript file")

args = parser.parse_args()

with open(args.transcript, "r", encoding="utf-8") as f:
  lines = f.read().splitlines()

with open(args.output, "w", encoding="utf-8") as w:
  w.write("PATH\tDURATION\tTRANSCRIPT\n")

transcript_dict = {}

for idx, line in enumerate(lines):
  lines[idx] = line.split(" ", 1)
  transcript_dict[lines[idx][0]] = lines[idx][-1]

for wav_file in glob.glob(os.path.join(os.path.dirname(args.transcript), "**", "*.wav"), recursive=True):
  wav_file = os.path.abspath(wav_file)
  name, ftype = os.path.splitext(os.path.basename(wav_file))
  transcript = transcript_dict[name].lower()
  y, sr = librosa.load(wav_file, sr=None)
  duration = librosa.core.get_duration(y=y, sr=sr)
  with open(args.output, "a", encoding="utf-8") as w:
    w.write(f"{wav_file}\t{duration}\t{transcript}\n")
  print(f"Processed: {wav_file}", end="\r", flush=True)
print("\nDone preprocessing vivos transcript")
