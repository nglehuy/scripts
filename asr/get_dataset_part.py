import argparse
import random

parser = argparse.ArgumentParser()

parser.add_argument("--transcript", "-t", type=str, help="Transcript file")
parser.add_argument("--output", "-o", type=str, help="Output dir")
parser.add_argument("percent", type=float, help="Percent")

args = parser.parse_args()

with open(args.transcript, "r", encoding="utf-8") as i:
  lines = i.read().splitlines()
  lines = lines[1:]

random.shuffle(lines)
lines = lines[:int(args.percent * len(lines))]

with open(args.output, "w", encoding="utf-8") as o:
  o.write("PATH\tDURATION\tTRANSCRIPT\n")
  for line in lines:
    o.write(f"{line}\n")

print("\nDone processing.")
