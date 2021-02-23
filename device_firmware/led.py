import time
import board
import neopixel

pixel_pin = board.D18
num_pixels = 1

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3, auto_write=False,
                           pixel_order=(1, 0, 2, 3))


def fade():
    for i in range(100):
        FADE_IN = (i, i, i, 0)
        pixels.fill(FADE_IN)
        time.sleep(1/500)
        pixels.show()
    time.sleep(0.1)
    for k in range(100):
        FADE_OUT = (100-k, 100-k, 100-k, 0)
        pixels.fill(FADE_OUT)
        time.sleep(1/500)
        pixels.show()
    time.sleep(1)

def blink():
    pixels.fill(WHITE)
    time.sleep(0.5)
    pixels.show()
    pixels.fill(OFF)
    time.sleep(0.5)
    pixels.show()
    
def led_off():
    pixels.fill(OFF)
    pixels.show()
    
def led_persist():
    pixels.fill(WHITE)
    pixels.show()
    
WHITE = (100, 100, 100, 0)
OFF = (0, 0, 0, 0)
