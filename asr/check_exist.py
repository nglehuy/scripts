import os
import argparse
import multiprocessing
import numpy as np

parser = argparse.ArgumentParser(description="Check enough files")

parser.add_argument("transcript", type=str, help="transcript file")

args = parser.parse_args()

with open(args.transcript, "r", encoding="utf-8") as f:
    lines = f.read().splitlines()

cores = multiprocessing.cpu_count()

slices = np.array_split(lines, cores)


def map_fn(aslice):
    for line in aslice:
        line = line.split("\t")
        if not os.path.exists(line[0]):
            print(f"Not existed: {line[0]}")


print("Processing ...")

with multiprocessing.Pool(cores) as pool:
    pool.map(map_fn, slices)
