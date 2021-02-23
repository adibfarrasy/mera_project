try:
    from picamera import PiCamera
    import time, io, json
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
        
        
class CameraConfigure(metaclass=MetaClass):
    
    def __init__(self, rotation, brightness, length, width, framerate, image_dump):
        
        """ Configure Camera """
        
        self.rotation = rotation
        self.brightness = brightness
        self.length = length
        self.width = width
        self.framerate = framerate
        self.image_dump = image_dump
        

class Camera():
    
    def __init__(self, cam_conf):
        
        """
        :param ctrl_conf: Object of class CameraConfigure
        """
        
        self.cam_conf = cam_conf
        
    def __enter__(self):
        
        print("__enter__")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.instance.close()
        print("__exit__")

    def StartCamera(self):
        
        self.instance = PiCamera()
        self.instance.rotation = self.cam_conf.rotation
        self.instance.brightness = self.cam_conf.brightness
        self.instance.resolution = (self.cam_conf.length, self.cam_conf.width)
        self.instance.framerate = self.cam_conf.framerate
        time.sleep(0.1)
        return self.instance

    def GetFrame(self):
        
        _stream = io.BytesIO()
        #self.instance.start_preview()
        time.sleep(1)
        self.instance.capture(_stream, format='jpeg', use_video_port=False)
        
        """ Reduce file size by PIL.Image compression """
        
        _image = Image.open(_stream)
        _image = _image.resize((1280, 720))
        _image.save(self.cam_conf.image_dump)
        
        self.instance.stop_preview()
        
        print("Snapshot saved to temp_img.jpg")
        

if __name__ == "__main__":

    print("Warming up camera...")
    
    rotation = 270
    brightness = 69
    length = 1280
    width = 720
    framerate = 30
    
    config = None
    
    with open('/home/pi/Desktop/device_firmware/state_of_the_art/config.json') as f:
        config = json.load(f)
    
    IMAGE_DUMP = config["current_image"]
    
    cam_conf = CameraConfigure(rotation, brightness, length, width, framerate, IMAGE_DUMP)
    camera = Camera(cam_conf)
    camera.StartCamera()
    
    while True:
        
        camera.GetFrame()
    
    
    
