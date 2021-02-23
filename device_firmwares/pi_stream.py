from picamera.array import PiRGBArray
from picamera import PiCamera
import time, io
from PIL import Image

def cam_init():
# initialize the camera and grab a reference to the raw camera capture
    camera = PiCamera()
    camera.rotation = 270
    camera.brightness = 60
    res_length = 1280
    res_width = 720
    camera.resolution = (res_length, res_width)
    camera.framerate = 10
    raw_capture = PiRGBArray(camera, size=(res_length, res_width))
# allow the camera to warmup
    time.sleep(0.1)
    return camera

def get_frame_from_stream(camera):
# get temporary frames from stream
    stream = io.BytesIO()
    camera.start_preview()
    time.sleep(1)
    camera.capture(stream, format='jpeg')
    image = Image.open(stream)
    image = image.resize((1280,720))
    return image