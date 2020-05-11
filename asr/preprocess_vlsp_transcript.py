import argparse
import os
import glob
import librosa
import json

parser = argparse.ArgumentParser(description="Preprocess transcript for vivos dataset")

parser.add_argument("transcript", type=str, help="transcript file")
parser.add_argument("--train_dir", type=str, help="Training set dir")
parser.add_argument("--dev_dir", type=str, help="Dev set dir")
parser.add_argument("--test_dir", type=str, help="Testing set dir")

args = parser.parse_args()

with open(args.transcript, "r", encoding="utf-8") as i:
  lines = i.read().splitlines()

tokens = ".,;/\\\"@#$%^&*()_-+={}[]~`-|?!1234567890"

for idx, line in enumerate(lines):
  line = json.load(line)
  key = line["key"].split("/")
  key = key[4:]
  key = "/".join(key)
  key = os.path.join(parent_dir, key)
  if any([token in line["text"] for token in tokens]):
    print(line["text"])
    line["text"] = str(input("Input: "))
  lines[idx] = [key, line["duration"], line["text"].lower()]

with open(args.output, "w", encoding="utf-8") as o:
  for audio_path, duration, text in lines:
    o.write(f"{audio_path}\t{duration}\t{text}\n")
