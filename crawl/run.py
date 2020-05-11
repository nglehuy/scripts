import os
import argparse
import librosa
import numpy as np

parser = argparse.ArgumentParser(description="crawl text from websites")

parser.add_argument("--output", "-o", type=str, help="Output file text")
parser.add_argument("file", type=str, help="Path to file containing links to websites")

args = parser.parse_args()

with open(args.file, "r", encoding="utf-8") as f:
  lines = f.read().splitlines()


