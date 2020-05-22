import argparse
import random
import sys

parser = argparse.ArgumentParser()

parser.add_argument("--transcript", "-t", type=str, help="Transcript file")
parser.add_argument("--output", "-o", type=str, help="Output dir")
parser.add_argument("ratio", type=float, help="Percent")

args = parser.parse_args()

with open(args.transcript, "r", encoding="utf-8") as i:
  lines = i.read().splitlines()
  firstline = lines[0]
  lines = lines[1:]

random.shuffle(lines)
lines = lines[:int(args.ratio * len(lines))]

with open(args.output, "w", encoding="utf-8") as o:
  o.write(f"{firstline}\n")
  for i, line in enumerate(lines, 1):
    o.write(f"{line}\n")
    sys.stdout.write("\033[K")
    print(f"\rProcessed {i}/{len(lines)}", end="")
