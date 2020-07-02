import os
import argparse
import random
import sys
import unicodedata

parser = argparse.ArgumentParser()

parser.add_argument("--transcript", "-t", type=str, help="Transcript file")
parser.add_argument("--output", "-o", type=str, help="Output transcript file")
parser.add_argument("ratio", type=float, help="Ratio of first part over second part")

args = parser.parse_args()

with open(args.transcript, "r", encoding="utf-8") as i:
    lines = i.read().splitlines()
    firstline = lines[0]
    lines = lines[1:]

random.shuffle(lines)
lines1 = lines[:int(args.ratio * len(lines))]

with open(args.output, "w", encoding="utf-8") as o:
    o.write(f"{firstline}\n")
    for i, line in enumerate(lines1, 1):
        line = line.split("\t")
        line[-1] = unicodedata.normalize('NFC', line[-1])
        line = "\t".join(line)
        o.write(f"{line}\n")
        sys.stdout.write("\033[K")
        print(f"\rProcessed {i}/{len(lines1)}", end="")
