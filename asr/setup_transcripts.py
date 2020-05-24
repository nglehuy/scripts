import os
import sys
import argparse
import unicodedata

parser = argparse.ArgumentParser()

parser.add_argument("transcript", type=str, help="transcript file")
parser.add_argument("--dir", type=str, help="directory")
parser.add_argument("--level", type=int, help="tree level")

args = parser.parse_args()

with open(args.transcript, "r", encoding="utf-8") as f:
    lines = f.read().splitlines()
    first_line = lines[0]
    lines = lines[1:]

args.dir = os.path.abspath(args.dir)

tokens = ".,;/\\\"@#$%^&*()_-+={}[]~`-|?!1234567890"

for i, line in enumerate(lines):
    line = line.split("\t")
    path = line[0].split("/")
    path = path[-args.level:]
    path = "/".join(path)
    line[0] = os.path.join(args.dir, path)
    line[-1] = unicodedata.normalize("NFC", line[-1].lower())
    if any([token in line[-1] for token in tokens]):
        print(line[-1])
        line[-1] = str(input("Input: ")).lower()
    lines[i] = "\t".join(line)

with open(args.transcript, "w", encoding="utf-8") as f:
    f.write(first_line + "\n")
    for i, line in enumerate(lines, 1):
        f.write(line + "\n")
        sys.stdout.write("\033[K")
        print(f"\rProcessed {i}/{len(lines)}", end="")
