try:
    import json, datetime, base64, requests, time, ast
    from PIL import Image
    
except Exception:
    print("WARNING: Some modules are missing {}".format(Exception))


class MetaClass(type):
    
    _instance = {}
    
    def __call__(cls, *args, **kwargs):
        
        """ Singleton Design Pattern """
        
        if cls not in cls._instance:
            cls._instance[cls] = super(MetaClass, cls).__call__(*args, **kwargs)
            return cls._instance[cls]
        

class UploaderConfigure(metaclass=MetaClass):
    
    def __init__(self, device_id, url, image_dump, video_dump):
        
        """ Configure Video Tracker """
        
        self.device_id = device_id
        self.url = url
        self.image_dump = image_dump
        self.video_dump = video_dump
        
        
class Uploader():
    
    def __init__(self, up_conf):
        
        """
        :param up_conf: Object of class UploaderConfigure
        """
        
        self.up_conf = up_conf
        
    def __enter__(self):
        
        print("__enter__")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        
        print("__exit__")
    
    def PackageImage(self):
        
        with open(self.up_conf.image_dump, "rb") as _img_file:
            _tmp_img = base64.b64encode(_img_file.read())
            self._tmp_img = _tmp_img.decode('utf-8')
    
    def TransformVideoData(self):
        
        with open(self.up_conf.video_dump, 'r') as _ad_file:
                _ad_ori = _ad_file.read()
                _ad_ori = ast.literal_eval(_ad_ori)
                self._ad = _ad_ori["adv_content"]
            
    def SendReport(self):
        
        _t = datetime.datetime.utcnow()
        _tmp_time = _t.strftime("%Y-%m-%d %H:%M:%S")
        
        body = {"device_id": self.up_conf.device_id,
                "timestamp": _tmp_time,
                "advertiser": self._ad,
                "image": self._tmp_img}
        head = {'content-type': 'application/json'}
        
        try:
            """ To send to online database for camera image and video ad data. """
            _r = requests.post(URL_UPLOAD, data=json.dumps(body), headers=head)
            print("====> uploader: ", _r.status_code)
        
        except Exception as e: 
            print ("-->> " , e)
        
#         with open('/home/pi/Desktop/device_firmware/state_of_the_art/final_result.txt','w') as f:
#             f.write('\n')
#             json.dump(body,f)
#         print("====> local_file: 200")
        
        
        time.sleep(1)


if __name__ == "__main__":
    
    print("Warming up uploader...")
    
    config = None
    
    with open('/home/pi/Desktop/device_firmware/state_of_the_art/config.json') as f:
        config = json.load(f)
        
    ID = config["id"]
    URL_UPLOAD = config["url_analytics"]
    IMAGE_DUMP = config["current_image"]
    VIDEO_DUMP = config["current_ad"]
    
    uploader_conf = UploaderConfigure(ID, URL_UPLOAD, IMAGE_DUMP, VIDEO_DUMP)
    uploader = Uploader(uploader_conf)
    
    while True:
        
        uploader.PackageImage()
        uploader.TransformVideoData()
        uploader.SendReport()
    

