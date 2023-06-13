#!/bin/bash

while read -r line; do
  edge-tts -t "$line" --write-media "$line.mp3"
done < text.txt

