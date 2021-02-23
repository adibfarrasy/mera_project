#!/bin/sh

#activate CMS
python3 /home/pi/Desktop/device_firmware/state_of_the_art/video_player_sota.py &

#buffer time  post CMS boot
sleep 5

#activate CMS tracker
python3 /home/pi/Desktop/device_firmware/state_of_the_art/video_tracker_sota.py &

#activate program sequence
gnome-terminal -- /bin/sh -c "python3 /home/pi/Desktop/device_firmware/state_of_the_art/camera_sota.py; exec bash"
#gnome-terminal -- /bin/sh -c "python3 /home/pi/Desktop/device_firmware/state_of_the_art/video_tracker_sota.py; exec bash" 
gnome-terminal -- /bin/sh -c "sudo python3 /home/pi/Desktop/device_firmware/state_of_the_art/uploader_sota.py; exec bash"
gnome-terminal -- /bin/sh -c "sudo python3 /home/pi/Desktop/device_firmware/state_of_the_art/monitor_sota.py; exec bash" 
