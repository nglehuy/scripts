import argparse
import os
import json
import random
import shutil

parser = argparse.ArgumentParser(description="Preprocess transcript for vivos dataset")

parser.add_argument("transcript", type=str, help="transcript file")
parser.add_argument("--train_dir", type=str, help="Training set dir")
parser.add_argument("--dev_dir", type=str, help="Dev set dir")
parser.add_argument("--test_dir", type=str, help="Testing set dir")
parser.add_argument("--output", type=str, help="output transcript file")

args = parser.parse_args()

with open(args.transcript, "r", encoding="utf-8") as i:
  lines = i.read().splitlines()

train_set = int(len(lines) * 0.8)
test_set = len(lines) - train_set
dev_set = int(len(train_set) * 0.1)
train_set = train_set - dev_set

random.shuffle(lines)
train_set = lines[0:train_set]
dev_set = lines[train_set+1:train_set+dev_set]
test_set = lines[train_set+dev_set+1:]

cur_parent_dir = os.path.dirname(args.transcript)
tokens = ".,;/\\\"@#$%^&*()_-+={}[]~`-|?!1234567890"

for parent_dir, dataset in [[args.train_dir, train_set], [args.dev_dir, dev_set], [args.test_dir. test_set]]:
  for idx, line in enumerate(dataset):
    line = json.load(line)
    key = line["key"].split("/")
    key = key[4:]
    key = "/".join(key)
    cur_key = os.path.join(cur_parent_dir, key)
    key = os.path.join(parent_dir, key)
    shutil.move(cur_key, key)
    if any([token in line["text"] for token in tokens]):
      print(line["text"])
      line["text"] = str(input("Input: "))
    lines[idx] = [key, line["duration"], line["text"].lower()]

with open(args.output, "w", encoding="utf-8") as o:
  for audio_path, duration, text in lines:
    o.write(f"{audio_path}\t{duration}\t{text}\n")
