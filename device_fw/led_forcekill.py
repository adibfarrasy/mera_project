import time
import board
import neopixel

pixel_pin = board.D18
num_pixels = 1

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3, auto_write=False,
                           pixel_order=(1, 0, 2, 3))

if __name__ == "__main__":
    pixels.fill((0, 0, 0, 0))
    pixels.show()
    time.sleep(0.2)
    pixels.fill((255, 0, 0, 0))
    pixels.show()
    time.sleep(0.2)
    pixels.fill((0, 255, 0, 0))
    pixels.show()
    time.sleep(0.2)
    pixels.fill((0, 0, 255, 0))
    pixels.show()
    time.sleep(0.2)
    pixels.fill((255, 0, 0, 0))
    pixels.show()
    time.sleep(0.2)
    pixels.fill((0, 255, 0, 0))
    pixels.show()
    time.sleep(0.2)
    pixels.fill((0, 0, 255, 0))
    pixels.show()
    time.sleep(0.2)
    pixels.fill((255, 0, 0, 0))
    pixels.show()
    time.sleep(0.2)
    pixels.fill((0, 255, 0, 0))
    pixels.show()
    time.sleep(0.2)
    pixels.fill((0, 0, 255, 0))
    pixels.show()
    time.sleep(0.2)
    pixels.fill((255, 0, 0, 0))
    pixels.show()
    time.sleep(0.2)
    pixels.fill((0, 255, 0, 0))
    pixels.show()
    time.sleep(0.2)
    pixels.fill((0, 0, 255, 0))
    pixels.show()
    time.sleep(0.2)
    pixels.fill((0, 0, 0, 0))
    pixels.show()
    time.sleep(0.2)