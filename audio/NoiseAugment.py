from __future__ import absolute_import

import math
import glob
import os
import argparse
import random
import librosa
import numpy as np

sample_rate = 16000

parser = argparse.ArgumentParser(description="add noise")

parser.add_argument("--input", "-i", type=str, help="Input dir")
parser.add_argument("--noise", "-n", type=str, help="Noise dir")
parser.add_argument("--output", "-o", type=str, help="Output dir")

args = parser.parse_args()

snr_min = 5
snr_max = 15
min_noises = 1
max_noises = 3


def add_white_noise(signal: np.ndarray, snr=10):
  RMS_s = math.sqrt(np.mean(signal ** 2))
  # RMS values of noise
  RMS_n = math.sqrt(RMS_s ** 2 / (pow(10, snr / 20)))
  # Additive white gausian noise. Thereore mean=0
  # Because sample length is large (typically > 40000)
  # we can use the population formula for standard daviation.
  # because mean=0 STD=RMS
  STD_n = RMS_n
  noise = np.random.normal(0, STD_n, signal.shape[0])
  return noise


def add_noise_from_sound(signal: np.ndarray, noise_wavs: list):
  random.shuffle(noise_wavs)
  num_noises = random.randint(min_noises, max_noises)
  noises = random.choices(noise_wavs, k=num_noises)  # randomly choose a noise from a list of noises
  added_noise = []
  for noise_type in noises:
    snr = random.uniform(snr_min, snr_max)
    if noise_type == "white_noise":
      added_noise.append(add_white_noise(signal, snr))
    else:
      noise = read_audio(noise_type)

      if len(noise) < len(signal):
        continue
      idx = random.choice(range(0, len(noise) - len(signal)))  # randomly crop noise wav
      noise = noise[idx:idx + len(signal)]

      RMS_s = math.sqrt(np.mean(signal ** 2))
      # required RMS of noise
      RMS_n = math.sqrt(RMS_s ** 2 / (pow(10, snr / 20)))

      # current RMS of noise
      RMS_n_current = math.sqrt(np.mean(noise ** 2))
      noise = noise * (RMS_n / (RMS_n_current + 1e-6))

      added_noise.append(noise)

  for noise in added_noise:
    signal = np.add(signal, noise)
  return signal


def read_audio(path):
  signal, _ = librosa.core.load(path, sr=sample_rate)
  return signal


def write_audio(path, signal):
  librosa.output.write_wav(path, signal, sample_rate)


noises_dir = glob.glob(os.path.join(args.noise, "**", "*.wav"), recursive=True)
noises_dir.append("white_noise")

for wav_file in glob.glob(os.path.join(args.input, "**", "*.wav"), recursive=True):
  signal = read_audio(wav_file)
  signal = add_noise_from_sound(signal, noises_dir)
  new_file = wav_file.replace(args.input, args.output)
  try:
    os.makedirs(os.path.dirname(new_file))
  except Exception:
    pass
  write_audio(new_file, signal)
  print(f"Processed: {wav_file}", end="\r", flush=True)
print("\nDone adding noises")
