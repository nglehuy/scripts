import argparse
import os
import glob
import librosa
import unicodedata

parser = argparse.ArgumentParser(description="Preprocess transcript for vivos dataset")

parser.add_argument("transcripts", nargs="+", type=str, help="transcript file")
parser.add_argument("--frame", type=int, default=25)
parser.add_argument("--stride", type=int, default=10)
parser.add_argument("--sr", type=int, default=16000)

args = parser.parse_args()

lines = []
for f in args.transcripts:
    with open(f, "r", encoding="utf-8") as t:
        temp = t.read().splitlines()
        temp = temp[1:]
        lines += temp

duration = 0.0
max_duration = 0.0


args = parser.parse_args()

lines = []
for f in args.transcripts:
    with open(f, "r", encoding="utf-8") as t:
        temp = t.read().splitlines()
        temp = temp[1:]
        lines += temp

duration = 0.0
max_duration = 0.0
for line in lines:
    dur = float(line.split("\t")[1])
    duration += dur
    if dur > max_duration:
        max_duration = dur

args.frame = int(args.sr * (args.frame / 1000))
args.stride = int(args.sr * (args.stride / 1000))
max_time = int(max_duration * (1 + ((args.sr + 2 * (args.frame // 2)) - args.frame) // args.stride))


print(f"Duration: {len(lines)}, {duration / (60 * 60)} hours")
print(f"Max Time: {max_duration}, {max_time} frames")
