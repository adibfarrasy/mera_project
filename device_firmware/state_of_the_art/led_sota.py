try:
    import board, neopixel
    import monitor_sota.py

except Exception:
    print("WARNING: Some modules are missing {}".format(Exception))

class MetaClass(type):
    
    _instance = {}
    
    def __call__(cls, *args, **kwargs):
        
        """ Singleton Design Pattern """
        
        if cls not in cls._instance:
            cls._instance[cls] = super(MetaClass, cls).__call__(*args, **kwargs)
            return cls._instance[cls]
        
class MetaClassLED(type):
    
    _instance = {}
    
    def __call__(cls, *args, **kwargs):
        
        """ Singleton Design Pattern """
        
        if cls not in cls._instance:
            cls._instance[cls] = super(MetaClassLED, cls).__call__(*args, **kwargs)
            return cls._instance[cls]
        
class LEDConfigure(metaclass=MetaClassLED):
    
    def __init__(self, pixel_pin, num_pixels, color, off, duration):
        
        """ Configure LED """
        
        self.pixel_pin = pixel_pin
        self.num_pixels = num_pixels
        self.color = color
        self.off = off
        self.duration = duration
    

class LED():
    
    def __init__(self, led_conf):
        
        """
        :param led_conf: Object of class LEDConfigure
        """
        
        self.led_conf = led_conf
        self._pixels = neopixel.NeoPixel(self.led_conf.pixel_pin, self.led_conf.num_pixels, brightness=0.3, auto_write=False,
                               pixel_order=(1, 0, 2, 3))

    def __enter__(self):
        
        print("__enter__")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        
        self.LEDOff()
        print("__exit__")
        
    def Fade(self):
        
        for i in range(100):
            _FADE_IN = (i, i, i, 0)
            self._pixels.fill(_FADE_IN)
            time.sleep(1/500)
            self._pixels.show()
            
        time.sleep(0.1)
        
        for k in range(100):
            _FADE_OUT = (100-k, 100-k, 100-k, 0)
            self._pixels.fill(_FADE_OUT)
            time.sleep(1/500)
            self._pixels.show()
            
        time.sleep(1)

    def Blink(self):
        
        self._pixels.fill(self.led_conf.color)
        time.sleep(0.5)
        self._pixels.show()
        self._pixels.fill(self.led_conf.off)
        time.sleep(0.5)
        self._pixels.show()
    
    def LEDOff(self):
        
        self._pixels.fill(self.led_conf.off)
        self._pixels.show()
    
    def LEDPersist(self):
        
        self._pixels.fill(self.led_conf.color)
        self._pixels.show()
    
    def LEDControl(self, state):
        
        """
        :param state: var of class function Monitor.GetState()
        """
        
        self.state = state
        
        if self.state == 1:
            self.LEDOff()
            self.LEDPersist()
            
        elif self.state == 2:
            self.LEDOff()
            time.sleep(0.1)
            for i in range(self.led_conf.duration + 1):
                self.Blink()
                
        elif self.state == 3:
            self.LEDOff()
            time.sleep(0.1)
            for i in range(self.led_conf.duration + 1):
                self.Fade()
                
        else:
            self.LEDOff()

if __name__ == "__main__":
    
    print("Warming up LED monitoring program...")
    
    WHITE = (100, 100, 100, 0)
    OFF = (0, 0, 0, 0)
    pixel_pin = board.D18
    num_pixels = 1
    state = 0
    duration = 10
    
    led_conf = LEDConfigure(pixel_pin, num_pixels, WHITE, OFF, duration)
    led = LED(led_conf)
    led_state = monitor_sota.GetState()
    led.LEDControl(led_state)