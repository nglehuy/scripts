#!/bin/bash
fileid="$1"
filename="$2"
curl -c /tmp/gdcookie -s -L "https://drive.google.com/uc?export=download&id=${fileid}" > /dev/null
curl -Lb /tmp/gdcookie "https://drive.google.com/uc?export=download&confirm=`awk '/download/ {print $NF}' /tmp/gdcookie`&id=${fileid}" -o ${filename}
rm /tmp/gdcookie

