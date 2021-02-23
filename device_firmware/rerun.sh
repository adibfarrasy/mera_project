#!/bin/sh
sudo pkill -9 python

python3 main.py &
python3 video_player.py &
sleep 1
python3 video_tracker.py &

