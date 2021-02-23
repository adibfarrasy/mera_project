import json, datetime, base64, requests, time, ast
#import numpy as np
from PIL import Image
from pi_stream import cam_init, get_frame_from_stream

config = None
with open('/home/pi/Desktop/device_firmware/config.json') as f:
    config = json.load(f)
ID = config["id"]
URL_UPLOAD = config["url_analytics"]
IMAGE_DUMP = config["current_image"]
VIDEO_DUMP = config["current_ad"]

def package_img():
    with open(IMAGE_DUMP, "rb") as img_file:
        tmp_img = base64.b64encode(img_file.read())
        tmp_img = tmp_img.decode('utf-8')
    return tmp_img

def send_report(image_arg, adv_arg):
    t = datetime.datetime.utcnow()
    tmp_time = t.strftime("%Y-%m-%d %H:%M:%S")
    
    body = {"device_id": ID,
            "timestamp": tmp_time,
            "advertiser": adv_arg,
            "image": image_arg}
    head = {'content-type': 'application/json'}
    

    r = requests.post(URL_UPLOAD, data=json.dumps(body), headers=head)
    print("====> main: ", r.status_code)

    """
    with open('final_result.txt','w') as f:
        f.write('\n')
        json.dump(body,f)
    """
    
def main():
    print("Executing main.py ...")
    camera = cam_init()
    while True:
            img_ori = get_frame_from_stream(camera)
            img_ori.save(IMAGE_DUMP)
            img_packaged = package_img()
            
            with open(VIDEO_DUMP, 'r') as ad_file:
                ad_ori = ad_file.read()
                ad_ori = ast.literal_eval(ad_ori)
                ad = ad_ori["adv_content"]
                
            send_report(img_packaged, ad)

if __name__ == "__main__":
    main()
