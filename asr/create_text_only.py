import argparse
import os
import unicodedata

parser = argparse.ArgumentParser(description="Preprocess transcript for vivos dataset")

parser.add_argument("transcripts", nargs="+", type=str, help="transcript file")
parser.add_argument("--output", type=str)

args = parser.parse_args()

text = ""
for t in args.transcripts:
    with open(t, "r", encoding="utf-8") as ft:
        temp = ft.read().splitlines()
        temp = temp[1:]
    for line in temp:
        line = line.split("\t")
        line = unicodedata.normalize("NFC", line[-1])
        text += f"{line}\n"

with open(args.output, "w", encoding="utf-8") as fo:
    fo.write(text)
