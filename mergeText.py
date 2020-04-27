import os
import argparse
import glob

WINDOWS_LINE_ENDING = '\r\n'
UNIX_LINE_ENDING = '\n'

parser = argparse.ArgumentParser(description="mergeText command flags")

parser.add_argument("name", help="Name of the file to save")
parser.add_argument("--output", "-o", type=str, help="Directory to save output file")
parser.add_argument("--input", "-i", type=str, help="Directory to scan text files")

args = parser.parse_args()

if not (args.output and args.input and args.name):
  raise ValueError("must specify --output and --input")


def word_count(x):
  x = x.replace("\n", " ")
  return len(x.split())


num_words = 0

text = ""

for filepath in glob.iglob(os.path.join(args.input, "**", "*.txt"),
                           recursive=True):
  with open(filepath, "rb") as inp:
    content = inp.read()

  try:
    content = content.decode("utf-8")
  except Exception:
    content = content.decode("utf-16le")

  content = content.replace(WINDOWS_LINE_ENDING, UNIX_LINE_ENDING)

  text += content
  count = word_count(content)
  num_words += count

  with open(filepath, "w", encoding="utf-8") as inp:
    inp.write(content)

  print(filepath, count)


with open(os.path.join(args.output, f"{args.name}_{num_words}.txt"),
          "a", encoding="utf-8") as outp:
  outp.write(text)

print("End merging text files")
