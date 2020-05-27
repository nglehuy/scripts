import argparse
import unicodedata

parser = argparse.ArgumentParser()

parser.add_argument("file", type=str, help="transcript file")

args = parser.parse_args()

with open(args.file, "r", encoding="utf-8") as fi:
    text = fi.read()

text = unicodedata.normalize("NFC", text)

with open(args.file, "w", encoding="utf-8") as fo:
    fo.write(text)
