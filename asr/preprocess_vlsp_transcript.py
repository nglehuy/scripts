import argparse
import os
import json
import random
import shutil
import multiprocessing

parser = argparse.ArgumentParser(description="Preprocess transcript for vlsp dataset")

parser.add_argument("transcript", type=str, help="transcript file")
parser.add_argument("--output_dir", "-o", type=str, help="output dir")

args = parser.parse_args()

with open(args.transcript, "r", encoding="utf-8") as i:
    lines = i.read().splitlines()

train_set_count = int(len(lines) * 0.8)
test_set_count = len(lines) - train_set_count
dev_set_count = int(train_set_count * 0.1)
train_set_count = train_set_count - dev_set_count

random.shuffle(lines)
train_set = lines[0:train_set_count]
dev_set = lines[train_set_count + 1:train_set_count + dev_set_count]
test_set = lines[train_set_count + dev_set_count + 1:]

cur_parent_dir = os.path.dirname(args.transcript)
tokens = ".,;/\\\"@#$%^&*()_-+={}[]~`-|?!1234567890"

slices = [[train_set, "train"], [dev_set, "dev"], [test_set, "test"]]


def write_transcript(dataset, mode="train"):
    with open(os.path.join(args.output_dir, f"{mode}_transcripts.tsv"), "w", encoding="utf-8") as o:
        for audio_path, duration, text in dataset:
            o.write(f"{audio_path}\t{duration}\t{text}\n")


def map_fn(aslice):
    dataset, mode = aslice
    for idx, line in enumerate(dataset):
        line = json.loads(line)
        key = line["key"].split("/")
        key = key[5:]
        key = "/".join(key)
        cur_key = os.path.join(cur_parent_dir, key)
        key = os.path.join(args.output_dir, key)
        try:
            os.makedirs(os.path.dirname(key))
        except Exception:
            pass
        shutil.move(cur_key, key)
        if any([token in line["text"] for token in tokens]):
            print(line["text"])
            line["text"] = str(input("Input: "))
        dataset[idx] = [key, line["duration"], line["text"].lower()]
        print(f"\r{key}", end="")
    write_transcript(dataset, mode=mode)
    print(f"\nDone processing {mode} dataset")


with multiprocessing.Pool(3) as pool:
    pool.map(map_fn, slices)
