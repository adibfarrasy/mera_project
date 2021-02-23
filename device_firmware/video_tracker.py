import os, time, json, requests, datetime
from subprocess import run

config = None
with open('/home/pi/Desktop/device_firmware/config.json') as f:
    config = json.load(f)
ID = config["id"]
VIDEO_DIR = config["video_dir"]
URL_CONTENT = config["url_adv"]
VIDEO_DUMP = config["current_ad"]
        
def get_video_data():
    output = run(["vlc-ctrl", "info"], capture_output=True).stdout
    output_delim = str(output).split('\\n')
    output_split = []
    for i in output_delim:
        out = i.split(': ')[-1]
        output_split.append(out)
    video_data_name = output_split[4].split('/')[-1]
    video_data_duration = int(output_split[3])
    return video_data_name, video_data_duration

def send_report(video_data_name_arg):
    content_name = video_data_name_arg.split('.')[0]
    
    t = datetime.datetime.utcnow()
    t_corrected = t - datetime.timedelta(seconds=5)
    tmp_time = t_corrected.strftime("%Y-%m-%d %H:%M:%S")
    
    body = {"device_id": ID,
            "adv_content": content_name,
            "timestamp":tmp_time}
    head = {'content-type': 'application/json'}
    
    with open(VIDEO_DUMP, 'w') as outfile:
        #outfile.write('\n')
        json.dump(body, outfile)
        
    try:
        r = requests.post(URL_CONTENT, data=json.dumps(body), headers=head)
        print("===>advertisement: ", r.status_code)
        
    except Exception as e: 
        print ("-->> " , e)

def main():
    print("Executing video_tracker.py ...")
    while True:
        video_data_name, video_data_duration = get_video_data()
        send_report(video_data_name)
        time.sleep(video_data_duration)
        #print(video_data_name, video_data_duration)
    
if __name__ == "__main__":
            main()