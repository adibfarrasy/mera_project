try:
    import os, json, time
    
except Exception:
    print("WARNING: Some modules are missing {}".format(Exception))

def input_device_id():
    #load json and copy the content
    a_file = open('/home/pi/Desktop/device_firmware/state_of_the_art/config.json', "r")
    json_object = json.load(a_file)
    a_file.close()
    
    #change the value
    if json_object["id"] == 0:
        json_object["id"] = int(input("Enter new device ID: "))
        
        #load json, edit content
        a_file = open('/home/pi/Desktop/device_firmware/state_of_the_art/config.json', "w")
        a_file.write('\n')
        json.dump(json_object, a_file)
        a_file.close()
        
        print("New device ID is " + str(json_object["id"]))
        
    else:
        print("Device ID is: " + str(json_object["id"]))
        
    time.sleep(1)
        
def run_mera():
    print("Initializing Mera programs...")
    time.sleep(60)
    os.system("/home/pi/Desktop/device_firmware/state_of_the_art/run.sh")
        
if __name__ == "__main__":
        input_device_id()
        run_mera()
    