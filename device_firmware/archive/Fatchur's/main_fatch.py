import cv2
import pika
import json
import numpy as np
from time import sleep
import tensorflow as tf
from datetime import datetime
from detector_utils import nms
from detector_utils import crop_image
from image_utils import encode_image_to_b64
from detector_utils import draw_rectangle
from pi_stream import cam_init, stream

import requests

config = None
with open('config.json') as f:
    config = json.load(f)
ID = config["id"]
MODEL_PATH = config["model_path"]
#VIDEO_URL = config["video_url"]
URL_UPLOAD = config["url_upload"]

interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

#cap = cv2.VideoCapture(VIDEO_URL)
people_num = 0
current_hour = datetime.utcnow().hour

#connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
#channel = connection.channel()
#channel.queue_declare(queue='img')


def upload(body): 
    r = requests.post(URL_UPLOAD, json=body)
    print("====> main: ", r.status_code)

def prepare_body(cropped_list, bboxes): 
    """[summary]

    Arguments:
        cropped_list {[type]} -- [description]
        bboxes {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    global current_hour, people_num 
    tmp_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')   
    hour =  datetime.utcnow().hour
    if current_hour != hour: 
        frame_num = 0
        current_hour = hour

    body = {"device_id": ID, "timestamp": tmp_time, "data": []}

    for i in cropped_list: 
        tmp = encode_image_to_b64(i)[0]
        body["data"].append({"body": tmp, "head_detected": False, "people_num": people_num})
        people_num += 1     
    
    #body = {"img": body}
    #return json.dumps(body)
    return body 


while(True):
    camera, raw_image = cam_init()
    for frame in stream(camera, raw_image):
        img_ori = cv2.resize(frame, (416, 416))
        img = img_ori.reshape((1, 416, 416, 3)).astype(np.float32) / 255.
        interpreter.set_tensor(input_details[0]['index'], img)
        interpreter.invoke()
        output_data = interpreter.get_tensor(output_details[0]['index'])
        bboxes = nms(output_data, 
                        confidence_threshold=0.60, 
                        overlap_threshold=0.3)
    
        if len(bboxes) > 0:
            cropped_list = crop_image(img_ori, bboxes)
            body = prepare_body(cropped_list, bboxes)
            """
            channel.basic_publish(exchange='', 
                                    routing_key='img', 
                                    body=body)
            """
        upload(body)
        
        #sleep(0.3)
        
