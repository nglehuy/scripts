import os
import argparse

parser = argparse.ArgumentParser(description="Preprocess transcript for infore dataset")

parser.add_argument("csv", type=str)
parser.add_argument("--output", type=str)
parser.add_argument("--dir", type=str)

args = parser.parse_args()

with open(args.csv, "r", encoding="utf-8") as i:
    lines = i.read().splitlines()

for idx, line in enumerate(lines):
    lines[idx] = line.split("|")
    lines[idx][0] = os.path.join(os.path.abspath(args.dir), lines[idx][0])

with open(args.output, "w", encoding="utf-8") as o:
    o.write("PATH\tDURATION\tTRANSCRIPT\n")
    for path, transcript, duration in lines:
        o.write(f"{path}\t{float(duration):.2f}\t{transcript}\n")
