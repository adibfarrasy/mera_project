import io
import cv2
import base64
import numpy as np
from io import BytesIO
from PIL import Image as im
from scipy.ndimage import interpolation as inter


def encode_image_to_b64(image_array):
    try:
        _ , buffer_image = cv2.imencode('.jpg', image_array)
        image_encoded = base64.b64encode(buffer_image).decode('utf-8')
        status_encoded = True
    except:
        image_encoded = ''
        status_encoded = False
    return image_encoded , status_encoded

