import os
import argparse
import random
import sys
import unicodedata

parser = argparse.ArgumentParser()

parser.add_argument("--transcript", "-t", type=str, help="Transcript file")
parser.add_argument("--first", type=str, help="First transcript part")
parser.add_argument("--second", type=str, help="Second transcript part")
parser.add_argument("ratio", type=float, help="Ratio of first part over second part")

args = parser.parse_args()

with open(args.transcript, "r", encoding="utf-8") as i:
    lines = i.read().splitlines()
    firstline = lines[0]
    lines = lines[1:]

random.shuffle(lines)
lines1 = lines[:int(args.ratio * len(lines))]
lines2 = lines[len(lines1):]

with open(args.first, "w", encoding="utf-8") as o:
    o.write(f"{firstline}\n")
    for i, line in enumerate(lines1, 1):
        line = line.split("\t")
        line[-1] = unicodedata.normalize('NFC', line[-1])
        line = "\t".join(line)
        o.write(f"{line}\n")
        sys.stdout.write("\033[K")
        print(f"\rProcessed {i}/{len(lines1)}", end="")

with open(args.second, "w", encoding="utf-8") as o:
    o.write(f"{firstline}\n")
    for i, line in enumerate(lines2, 1):
        line = line.split("\t")
        line[-1] = unicodedata.normalize('NFC', line[-1])
        line = "\t".join(line)
        o.write(f"{line}\n")
        sys.stdout.write("\033[K")
        print(f"\rProcessed {i}/{len(lines2)}", end="")