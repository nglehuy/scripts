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

tokens = ".,;/\\\"@#$%^&*()_-+={}[]~`-|?!1234567890"

for idx, line in enumerate(lines):
  lines[idx] = line.split(" ", 1)
  lines[idx][-1] = lines[idx][-1].lower()
  if any([token in lines[idx][-1] for token in tokens]):
    print(lines[idx])
    lines[idx][-1] = str(input("Input: "))

with open(args.output, "w", encoding="utf-8") as o:
  for line in lines:
    o.write(f"{line[0]} {line[-1]}\n")
