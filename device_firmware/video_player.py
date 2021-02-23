import os, json

config = None
with open('/home/pi/Desktop/device_firmware/config.json') as f:
    config = json.load(f)
VIDEO_DIR = config["video_dir"]

def play_videos():
    execute_vlc = "vlc --fullscreen --video-on-top --loop " + VIDEO_DIR
    #execute_vlc = "vlc --loop " + VIDEO_DIR
    os.system(execute_vlc)

if __name__ == "__main__":
    play_videos()