try:
    import os, time, json, psutil, requests
    from datetime import datetime
    from subprocess import PIPE, Popen

except Exception:
    print("WARNING: Some modules are missing {}".format(Exception))


class MetaClass(type):
    
    _instance = {}
    
    def __call__(cls, *args, **kwargs):
        
        """ Singleton Design Pattern """
        
        if cls not in cls._instance:
            cls._instance[cls] = super(MetaClass, cls).__call__(*args, **kwargs)
            return cls._instance[cls]


class MonitorConfigure(metaclass=MetaClass):
    
    def __init__(self, device_id, url, process):
        
        """ Configure Monitor """
        
        self.device_id = device_id
        self.url = url
        self.process = process
    
class Monitor():
    
    def __init__(self, ctrl_conf):
        
        """
        :param ctrl_conf: Object of class MonitorConfigure
        """
        
        self.ctrl_conf = ctrl_conf
        
    def __enter__(self):
        
        print("__enter__")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        
        print("__exit__")

    def GetCpuStatus(self):
        
        _process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
        _output, _error = _process.communicate()
        _output = _output.decode()
        self._cpu_temperature = float(_output[_output.index('=') + 1:_output.rindex("'")])
        self._cpu_usage = psutil.cpu_percent()
        return self._cpu_temperature, self._cpu_usage
    
    def GetMemoryStatus(self):
        
        _ram = psutil.virtual_memory()
        self._ram_total = _ram.total / 2**20   #in MB
        #self._ram_used = _ram.used / 2**20
        #self._ram_free = _ram.free / 2**20
        self._ram_percent_used = _ram.percent
        return self._ram_percent_used

    def CheckPythonRun(self):

        self._program_result = {}
    
        for i in self.ctrl_conf.process: 
            self._program_result[i] = False

        for _proc in psutil.process_iter():    
            try:
                _proc_identity = _proc.as_dict()
                if _proc_identity['cmdline'][1] in self.ctrl_conf.process: 
                    self._program_result[_proc_identity['cmdline'][1]] = True

            except:
                pass
        
        return self._program_result

    def SendReport(self):
        
        _tmp_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        
        body = {"device_id": self.ctrl_conf.device_id,
            "timestamp": _tmp_time,
            "camera_alive": int(self._program_result[self.ctrl_conf.process[0]]),
            "video_player_alive": int(self._program_result[self.ctrl_conf.process[1]]),
            "cpu_usage" : float(self._cpu_usage),
            "memory_usage" : float(self._ram_percent_used),
            "temperature" : float(self._cpu_temperature)}
    
        head = {'content-type': 'application/json'}
        
        try: 
            _r = requests.post(self.ctrl_conf.url, data=json.dumps(body), headers = head)
            print ("===> monitoring: ", _r.status_code)
        
        except Exception as e: 
            print ("-->> " , e)
            
        time.sleep(10*60)
    
    def GetState(self):
        
        if self._program_result[self.ctrl_conf.process[0]] == False or self._program_result[self.ctrl_conf.process[1]] == False:
            #os.system("./rerun.sh")
            #print("=======")
            state = 3
            
        elif self._program_result[self.ctrl_conf.process[0]] and self._program_result[self.ctrl_conf.process[1]]:
            state = 1
        
        return state
        
        
if __name__ == "__main__":
    
    print("Warming up monitoring program...")
    
    config = None
    
    with open('/home/pi/Desktop/device_firmware/state_of_the_art/config.json') as f:
        config = json.load(f)
        
    ID = config["id"]
    URL_ALIVE = config["url_ctrl"]
    PROCESS = ["/home/pi/Desktop/device_firmware/state_of_the_art/camera_sota.py",
               "/home/pi/Desktop/device_firmware/state_of_the_art/video_tracker_sota.py"]
    
    ctrl_conf = MonitorConfigure(ID, URL_ALIVE, PROCESS)
    monitor = Monitor(ctrl_conf)
    
    while True:
        
        monitor.GetCpuStatus()
        monitor.GetMemoryStatus()
        monitor.CheckPythonRun()
        monitor.GetState()
        monitor.SendReport()
        
        
        
    


