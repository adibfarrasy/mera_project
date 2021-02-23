import os
import time
import json
import psutil 
import requests 
from datetime import datetime
from led import led_persist, led_off, blink, fade
from subprocess import PIPE, Popen
        
config = None
with open('/home/pi/Desktop/device_firmware/config.json') as f:
    config = json.load(f)
ID = config["id"]
URL_ALIVE = config["url_ctrl"]
PROCESS = ["/home/pi/Desktop/device_firmware/main.py", "/home/pi/Desktop/device_firmware/video_tracker.py"]


ai_alive = PROCESS[0]
video_alive =  PROCESS[1]

def get_cpu_status():
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
    output, _error = process.communicate()
    output = output.decode()
    cpu_temperature = float(output[output.index('=') + 1:output.rindex("'")])
    cpu_usage = psutil.cpu_percent()
    return cpu_temperature, cpu_usage
    
def get_memory_status():
    ram = psutil.virtual_memory()
    ram_total = ram.total / 2**20   #in MB
    #ram_used = ram.used / 2**20
    #ram_free = ram.free / 2**20
    ram_percent_used = ram.percent
    return ram_percent_used


def check_python_run():
    """[summary]

    Returns:
        [type]: [description]
    """    

    program_result = {}
    for i in PROCESS: 
        program_result[i] = False

    for proc in psutil.process_iter():    
        try:
            proc_identity = proc.as_dict()
            if proc_identity['cmdline'][1] in PROCESS: 
                program_result[proc_identity['cmdline'][1]] = True

        except:
            pass
    return program_result


def send_report(program_result, cpu_temp, cpu_used, ram_percent_used): 
    """[summary]

    Args:
        program_result ([type]): [description]
    """    
    tmp_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    body = {"device_id": ID,
            "timestamp": tmp_time,
            "ai_alive": int(program_result[ai_alive]),
            "video_player_alive": int(program_result[video_alive]),
            "cpu_usage" : float(cpu_used),
            "memory_usage" : float(ram_percent_used),
            "temperature" : float(cpu_temp)}
    
    head = {'content-type': 'application/json'}
    
    try: 
        r = requests.post(URL_ALIVE, data=json.dumps(body), headers = head)
        print ("===> monitoring: ", r.status_code)
        
    except Exception as e: 
        print ("-->> " , e)
        
def led_machine(state, dur):
    if state == 1:
        led_off()
        led_persist()
    elif state == 2:
        led_off()
        time.sleep(0.1)
        for i in range(dur):
            blink()
    elif state == 3:
        led_off()
        time.sleep(0.1)
        for i in range(dur):
            fade()
    else:
        led_off()
        
def main(): 

    print("Executing controller.py ...")
    while True:  
        duration = 10 
        led_state = 0
        program_result = check_python_run()
        cpu_temperature, cpu_usage = get_cpu_status()
        ram_percent_used = get_memory_status()
        
        send_report(program_result, cpu_temperature, cpu_usage, ram_percent_used)
        #print("main.py: ", program_result[ai_alive] ,", video_tracker.py: ",program_result[video_alive])

        if program_result[ai_alive] == False or program_result[video_alive] == False:
            #os.system("./rerun.sh")
            #print("=======")
            led_state = 3
            
        elif program_result[ai_alive] and program_result[video_alive]:
            led_state = 1
            
        led_machine(led_state, duration)
        #time.sleep(duration)
        
if __name__ == "__main__":
    main()


