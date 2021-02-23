try:
    import os, time, json, requests, datetime
    from subprocess import run

except Exception:
    print("WARNING: Some modules are missing {}".format(Exception))


class MetaClass(type):
    
    _instance = {}
    
    def __call__(cls, *args, **kwargs):
        
        """ Singleton Design Pattern """
        
        if cls not in cls._instance:
            cls._instance[cls] = super(MetaClass, cls).__call__(*args, **kwargs)
            return cls._instance[cls]


class VideoTrackerConfigure(metaclass=MetaClass):
    
    def __init__(self, device_id, video_dir, url, video_dump):
        
        """ Configure Video Tracker """
        
        self.device_id = device_id
        self.video_dir = video_dir
        self.url = url
        self.video_dump = video_dump
        
        
class VideoTracker():
    
    def __init__(self, video_conf):
        
        """
        :param video_conf: Object of class VideoTrackerConfigure
        """
        
        self.video_conf = video_conf
        
    def __enter__(self):
        
        print("__enter__")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        
        print("__exit__")
        
    def GetVideoData(self):
        
        _output_split = []
        self._output = run(["vlc-ctrl", "info"], capture_output=True).stdout
        self._output_delim = str(self._output).split('\\n')
        
        for i in self._output_delim:
            _out = i.split(': ')[-1]
            _output_split.append(_out)
        
        self._video_name = _output_split[4].split('/')[-1]
        self._video_name = self._video_name.split('.')[0]
        self._video_duration = int(_output_split[3])

    def SendReport(self):
    
        _t = datetime.datetime.utcnow()
        _t_corrected = _t - datetime.timedelta(seconds=5)
        self._tmp_time = _t_corrected.strftime("%Y-%m-%d %H:%M:%S")
    
        body = {"device_id": self.video_conf.device_id,
                "adv_content": self._video_name,
                "timestamp": self._tmp_time} 
        head = {'content-type': 'application/json'}
        
        with open(self.video_conf.video_dump, 'w') as outfile:
            """ To be read by uploader.py for data upload. """
            
            json.dump(body, outfile)
        
        try:
            """ To send to online database and count number of ad-plays. """
            
            _r = requests.post(self.video_conf.url, data=json.dumps(body), headers=head)
            print("===> advertisement: ", _r.status_code)
        
        except Exception as e: 
            print ("-->> " , e)
        
        time.sleep(self._video_duration)
    
    
if __name__ == "__main__":
    
    print("Warming up video tracker...")
    
    config = None
        
    with open('/home/pi/Desktop/device_firmware/state_of_the_art/config.json') as f:
        config = json.load(f)
        
    ID = config["id"]
    VIDEO_DIR = config["video_dir"]
    URL_CONTENT = config["url_adv"]
    VIDEO_DUMP = config["current_ad"]
        
    video_config = VideoTrackerConfigure(ID, VIDEO_DIR, URL_CONTENT, VIDEO_DUMP)
    video_tracker = VideoTracker(video_config)
    
    while True:

        video_tracker.GetVideoData()
        video_tracker.SendReport()
