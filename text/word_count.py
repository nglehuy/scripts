import argparse
import unicodedata

parser = argparse.ArgumentParser()

parser.add_argument("file", type=str, help="transcript file")

args = parser.parse_args()

with open(args.file, "r", encoding="utf-8") as f:
    text = f.read()

text.replace("\n", " ")
print(f"Words count: {len(text.split(' '))}")
