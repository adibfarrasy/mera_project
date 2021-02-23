import os
import time
import json
import psutil 
import requests 
from datetime import datetime
from led import led_persist, led_off, blink, fade
from subprocess import PIPE, Popen
        
#PROCESS = ["main.py", "video_player.py", "uploader.py"]
PROCESS = ["main.py", "video_tracker.py"]


ai_alive = PROCESS[0]
video_player_alive =  PROCESS[1]
#uploader_alive = PROCESS[2]

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
    ram_used = ram.used / 2**20
    #ram_free = ram.free / 2**20
    #ram_percent_used = ram.percent
    return round(ram_used), round(ram_total)


def check_python_run():
    """[summary]

    Returns:
        [type]: [description]
    """    
    rabbitmq_memory = 0.0
    rabbitmq_detected = False
    program_result = {}
    for i in PROCESS: 
        program_result[i] = False

    for proc in psutil.process_iter():    
        try:
            proc_identity = proc.as_dict()
            if proc_identity['cmdline'][1] in PROCESS: 
                program_result[proc_identity['cmdline'][1]] = True

            elif proc_identity['cmdline'][2] == "rabbitmq": 
                rabbitmq_detected = True
                rabbitmq_memory = proc_identity['memory_percent']
        except:
            pass
    return program_result, rabbitmq_detected, rabbitmq_memory


def create_report(program_result, cpu_temp, cpu_used, ram_used, ram_tot): 
    """[summary]

    Args:
        program_result ([type]): [description]
    """    
    tmp_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    body = {#"device_id": ID,
            "timestamp": tmp_time,
            "temperature" : str(cpu_temp),
            "ai_alive": int(program_result[ai_alive]),
            "video_player_alive": int(program_result[video_player_alive]),
            #"uploader_alive" : int(program_result[uploader_alive]),
            "cpu_usage" : str(cpu_used),
            "memory_usage" : str(ram_used) + ' / ' + str(ram_tot)
            }
            
    with open('test_log.txt', 'a') as outfile:
        outfile.write('\n')
        json.dump(body, outfile)
        
def led_machine(state, dur):
    if state == 1:
        led_off()
        time.sleep(1)
        led_persist()
    elif state == 2:
        led_off()
        time.sleep(1)
        for i in range(dur):
            blink()
    elif state == 3:
        led_off()
        time.sleep(1)
        for i in range(dur):
            fade()
    else:
        led_off()
        
def main(): 
    """[summary]
    """   
    while True:  
        duration = 1800
        led_state = 0
        program_result, rabbitmq_detected, rabbitmq_memory = check_python_run()
        cpu_temperature, cpu_usage = get_cpu_status()
        ram_used, ram_total = get_memory_status()
        
        create_report(program_result, cpu_temperature, cpu_usage, ram_used, ram_total)

        if program_result[ai_alive] == False or program_result[video_player_alive] == False:
            #or program_result[uploader_alive] == False:
            #os.system("./rerun.sh")
            print("error")
            led_state = 3
            
        elif program_result[ai_alive] == True and program_result[video_player_alive] == True:
             #and program_result[uploader_alive] == True:
            print("all systems go")
            led_state = 1
            
        led_machine(led_state, duration)
        time.sleep(duration)
        
if __name__ == "__main__":
    main()



