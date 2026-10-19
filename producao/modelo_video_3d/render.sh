#!/bin/bash
cd "$(dirname "$0")"
NF=$(python3 -c "from timeline import END; print(int(round(END*30)))"); H=$((NF/2))
python3 compose.py partA.mp4 0 $H > logA.txt 2>&1 & PA=$!
python3 compose.py partB.mp4 $H $NF > logB.txt 2>&1 & PB=$!
wait $PA $PB
printf "file 'partA.mp4'\nfile 'partB.mp4'\n" > parts.txt
ffmpeg -v error -y -f concat -safe 0 -i parts.txt -c copy raw.mp4 && ffmpeg -v error -y -i raw.mp4 -i mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -af "loudnorm=I=-14:TP=-1.5" -shortest out_final.mp4 && mv out_final.mp4 LojaDoImigrante_checagem_Moro_3D.mp4 && ffprobe -v error -show_entries format=duration -of csv=p=0 LojaDoImigrante_checagem_Moro_3D.mp4
