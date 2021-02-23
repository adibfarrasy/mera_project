try:
    import os, json

except Exception:
    print("WARNING: Some modules are missing {}".format(Exception))

class MetaClass(type):
    
    _instance = {}
    
    def __call__(cls, *args, **kwargs):
        
        """ Singleton Design Pattern """
        
        if cls not in cls._instance:
            cls._instance[cls] = super(MetaClass, cls).__call__(*args, **kwargs)
            return cls._instance[cls]


class VideoPlayerConfigure(metaclass=MetaClass):
    
    def __init__(self, video_dir='video/'):
        
        """ Configure Video Player """
        
        self.video_dir = video_dir
        

class VideoPlayer():
    
    def __init__(self, video_conf):
        
        """
        :param video_conf: Object of class VideoPlayerConfigure
        """
        
        self.video_conf = video_conf
        print("Warming up video player...")
        
    def __enter__(self):
        
        print("__enter__")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        
        print("__exit__")
        
    def RunVideos(self):
        
#         self._vlc_cmd = "vlc --fullscreen --video-on-top --no-video-title --loop " + self.video_conf.video_dir
        self._vlc_cmd = "vlc --no-video-title --no-audio --loop " + self.video_conf.video_dir
        self._execute_cmd = os.system(self._vlc_cmd)


if __name__ == "__main__":
    
    config = None
    
    with open('/home/pi/Desktop/device_firmware/state_of_the_art/config.json') as f:
        config = json.load(f)
        
    VIDEO_DIR = config["video_dir"]
    
    video_config = VideoPlayerConfigure(VIDEO_DIR)
    video_player = VideoPlayer(video_config)
    video_player.RunVideos()
