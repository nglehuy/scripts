from __future__ import unicode_literals
import os
import argparse
import youtube_dl

parser = argparse.ArgumentParser(description="crawlYoutube command flags")

parser.add_argument("--playlist", "-p", nargs="+", type=str, help="Playlist to crawl")
parser.add_argument("--save_dir", "-s", type=str,
                    help="Directory to save crawled files")
parser.add_argument("--sublang", type=str, help="Subtitle language")

args = parser.parse_args()

if not (args.playlist and args.save_dir and args.sublang):
  raise ValueError("must specify --playlist and --save_dir")


def my_hook(d):
  if d['status'] == 'finished':
    print('Done downloading, now converting ...')


ydl_opt = {
  "format": "bestaudio/best",
  "postprocessors": [{
    "key": "FFmpegExtractAudio",
    "preferredcodec": "wav",
    "preferredquality": "192"
  }],
  "progress_hooks": [my_hook],
  "writesubtitles": True,
  "writeautomaticsub": True,
  "subtitlesformat": "txt",
  "subtitleslangs": [args.sublang],
  "outtmpl": os.path.join(args.save_dir, "%(title)s.%(ext)s")
}

with youtube_dl.YoutubeDL(ydl_opt) as ydl:
  ydl.download(args.playlist)
