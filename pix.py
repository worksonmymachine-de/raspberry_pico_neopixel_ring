import neopixel
import time
import microcontroller
import digitalio

RED = (255,0,0)
RED2 = (127,127,0)
GREEN = (0,255,0)
GREEN2 = (0,127,127)
BLUE = (0,0,255)
BLUE2 = (127,0,127)
WHITE = (85,85,85)
WHITE2 = (127,127,127)
WHITE3 = (255,255,255)
COLORS = (RED, RED2, GREEN, GREEN2, BLUE, BLUE2, WHITE, WHITE2, WHITE3)

BRIGHTNESS_MAX = 1.0
BRIGHTNESS_MIN = 0.0
BRIGHTNESS_INCREASE_STEP = 0.1

PIXEL_AMOUNT = 8

class Pix:
    
    def __init__(self):
        self.button_color = digitalio.DigitalInOut(microcontroller.pin.GPIO1)
        self.button_color.direction = digitalio.Direction.OUTPUT
        self.button_bright = digitalio.DigitalInOut(microcontroller.pin.GPIO2)
        self.button_bright.direction = digitalio.Direction.OUTPUT
        self.pixels = neopixel.NeoPixel(microcontroller.pin.GPIO0, PIXEL_AMOUNT, auto_write=False)
        self.current_color_index = 0
        self.current_brightness = 0.1
        self.running = True
        self.start()

    def next_color(self):
        self.current_color_index = self.current_color_index + 1 if len(COLORS)-1 > self.current_color_index else 0
        self.set_color(COLORS[self.current_color_index])
        self.pixels.show()
            
    def set_color(self, color : (int, int, int)):
        print(f"changing colors to {color}")
        self.pixels.fill(color)

    def next_brightness(self):
        self.current_brightness = self.current_brightness + BRIGHTNESS_INCREASE_STEP if self.current_brightness + BRIGHTNESS_INCREASE_STEP <= BRIGHTNESS_MAX else BRIGHTNESS_MIN
        self.set_brightness(self.current_brightness)
        self.pixels.show()
        
    def set_brightness(self, brightness : float):
        print(f"changing brightness to {round(brightness, 1)}")
        self.pixels.brightness = brightness

    def off(self):
        print("turning off the light (brightness to 0.0) - you can turn it on again by pressing any button")
        self.pixels.brightness = BRIGHTNESS_MIN
        self.pixels.show()
        self.running = False
        
    def on(self):
        print(f"turning the light on again (brightness back to {self.current_brightness})")
        self.pixels.brightness = self.current_brightness
        self.pixels.show()
        self.running = True
        
    def init(self):
        self.set_brightness(self.current_brightness)
        self.set_color(COLORS[self.current_color_index])
        self.pixels.show()

    def start(self):
        print("Start")
        self.init()
        try:
            while True:
                while self.running:
                    if self.button_color.value and self.button_bright.value:
                        self.off()
                        time.sleep(1)
                    if self.button_color.value and not self.button_bright.value:
                        self.next_color()
                        self.pixels.show()
                        time.sleep(0.2)
                    if self.button_bright.value and not self.button_color.value:
                        self.next_brightness()
                        self.pixels.show()
                        time.sleep(0.2)
                    time.sleep(0.1)
                if self.button_bright.value or self.button_color.value:
                    self.on()
                    time.sleep(0.3)
        finally:
            self.pixels.deinit()

if __name__ == "__main__":
    Pix()
