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

DELAY_ON_OFF = 1.0
DELAY_SWITCH = 0.3
DELAY_POLLING = 0.2

class Pix:
    
    def __init__(self):
        self.button_color = digitalio.DigitalInOut(microcontroller.pin.GPIO1)
        self.button_color.direction = digitalio.Direction.OUTPUT
        self.button_bright = digitalio.DigitalInOut(microcontroller.pin.GPIO2)
        self.button_bright.direction = digitalio.Direction.OUTPUT
        self.current_color_index = 0
        self.current_brightness = 0.1
        self.pixels = self.init_pixels()
        self.running = True
        self.start()

    def init_pixels(self):
        return neopixel.NeoPixel(microcontroller.pin.GPIO0, PIXEL_AMOUNT, auto_write=False)

    def next_color(self):
        self.current_color_index = self.current_color_index + 1 if len(COLORS)-1 > self.current_color_index else 0
        self.set_color(COLORS[self.current_color_index])
            
    def set_color(self, color : (int, int, int)):
        print(f"changing colors to {color}")
        self.pixels.fill(color)
        self.pixels.show()

    def next_brightness(self):
        self.current_brightness = self.current_brightness + BRIGHTNESS_INCREASE_STEP if self.current_brightness + BRIGHTNESS_INCREASE_STEP <= BRIGHTNESS_MAX else BRIGHTNESS_MIN
        self.set_brightness(self.current_brightness)
        
    def set_brightness(self, brightness : float):
        print(f"changing brightness to {round(brightness, 1)}")
        self.pixels.brightness = brightness
        self.pixels.show()

    def off(self):
        print("turning off the light")
        self.set_brightness(BRIGHTNESS_MIN)
        self.running = False
        
    def on(self):
        print(f"turning the light on again")
        self.set_brightness(self.current_brightness)
        self.set_color(COLORS[self.current_color_index])
        self.running = True
        
    def init(self):
        self.pixels.brightness = self.current_brightness
        self.pixels.fill(COLORS[self.current_color_index])
        self.pixels.show()

    def start(self):
        print("Start")
        self.init()
        try:
            while True:
                while self.running:
                    # Turning off the light when both buttons are pressed simultaneously -> jumps into outer loop
                    if self.button_color.value and self.button_bright.value:
                        self.off()
                        time.sleep(DELAY_ON_OFF)
                    # sets next defined color on all leds
                    if self.button_color.value and not self.button_bright.value:
                        self.next_color()
                        time.sleep(DELAY_SWITCH)
                    # increases brightness by step and if surpassing maximum begins at minimum
                    if self.button_bright.value and not self.button_color.value:
                        self.next_brightness()
                        time.sleep(DELAY_SWITCH)
                    time.sleep(DELAY_POLLING)
                # Waiting for button press in deactivated state - will turn on light with either button
                if self.button_bright.value or self.button_color.value:
                    self.on()
                    time.sleep(DELAY_ON_OFF)
                time.sleep(DELAY_POLLING)
        finally:
            # Turning off the NeoPixels when script is stopped
            self.pixels.deinit()

if __name__ == "__main__":
    Pix()
