#!/bin/sh

python3 /home/pi/Desktop/device_firmware/video_player.py &
sleep 5
gnome-terminal -- /bin/sh -c "python3 /home/pi/Desktop/device_firmware/video_tracker.py; exec bash" 
gnome-terminal -- /bin/sh -c "sudo python3 /home/pi/Desktop/device_firmware/main.py; exec bash"
gnome-terminal -- /bin/sh -c "sudo python3 /home/pi/Desktop/device_firmware/controller.py; exec bash" 
