import os
import argparse
import librosa
import numpy as np

sample_rate = 16000

parser = argparse.ArgumentParser(description="split audio files")

parser.add_argument("--input", "-i", type=str, help="Input audio file")
parser.add_argument("--length", "-l", type=int, help="Number of seconds to split")
parser.add_argument("--output", "-o", type=str, help="Output directory")


args = parser.parse_args()


def read_audio(path):
  signal, _ = librosa.core.load(path, sr=sample_rate)
  return signal


def write_audio(path, signal):
  librosa.output.write_wav(path, signal, sample_rate)


signal = read_audio(args.input)
name, ftype = os.path.splitext(os.path.basename(args.input))
offset = int(args.length * sample_rate)
n_samples = signal.shape[0]
for idx, value in enumerate(zip(range(0, n_samples, offset), range(offset, n_samples + offset, offset))):
  slice_ = signal[value[0]:value[-1]]
  name_ = name + str(idx) + ftype
  write_audio(os.path.join(args.output, name_), slice_)
  print(f"Splitted: {idx}", end="\r", flush=True)
print("\nDone splitting")
