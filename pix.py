# import board
import neopixel
import time
import microcontroller
import digitalio


COLORS = ((255,0,0),(223,32,0),(191,64,0),(159,96,0),(127,127,0),(95,159,0),(64,191,0),(32,223,0), # red to green
          (0,255,0),(0,223,32),(0,191,64),(0,159,96),(0,127,127),(0,96,159),(0,64,191), # green to blue
          (0,0,255),(32,32,191),(64,64,127),(85,85,85), # blue to white
          (127,64,64),(191,32,32)) # white to red

BRIGHTNESS_MAX = 1.0
BRIGHTNESS_MIN = 0.1
BRIGHTNESS_OFF = 0.0
BRIGHTNESS_INCREASE_STEP = 0.1

PIXEL_AMOUNT = 8

DELAY_ON_OFF = 1.0
DELAY_SWITCH = 0.5
DELAY_POLLING = 0.2

class Pix:
    
    def __init__(self):
        # for some reason board.GPIOx wasn't found at runtime - autocomplete worked when importing and board.py is in lib directory
        self.button_color = self._init_button(microcontroller.pin.GPIO1)
        self.button_bright = self._init_button(microcontroller.pin.GPIO2)
        self.current_color_index = 0
        self.current_brightness = 0.1
        self.pixels = neopixel.NeoPixel(microcontroller.pin.GPIO0, PIXEL_AMOUNT, auto_write=False, pixel_order=neopixel.GRB)
        # self.pixels = neopixel.NeoPixel(board.D0, PIXEL_AMOUNT, auto_write=False, pixel_order=neopixel.RGBW)
        self.running = True
        self.start()
        
    def _init_button(self, pin : microcontroller.pin) -> digitalio.DigitalInOut:
        button = digitalio.DigitalInOut(pin)
        button.direction = digitalio.Direction.OUTPUT
        return button

    def next_color(self):
        self.current_color_index = self.current_color_index + 1 if len(COLORS)-1 > self.current_color_index else 0
        self.set_color_brightness()
            
    def set_color(self, color : (int, int, int)):
        print(f"changing colors to {color}")
#         self.pixels.fill(color)
        for i in range(PIXEL_AMOUNT):
            self.pixels[i]=color
            time.sleep(0.015)

    def next_brightness(self):
        self.current_brightness = self.current_brightness + BRIGHTNESS_INCREASE_STEP if self.current_brightness + BRIGHTNESS_INCREASE_STEP <= BRIGHTNESS_MAX else BRIGHTNESS_MIN
        self.set_color_brightness()
        
    def set_brightness(self, brightness : float):
        print(f"changing brightness to {round(brightness, 1)}")
        self.pixels.brightness = brightness

    def set_color_brightness(self):
        self.set_brightness(self.current_brightness)
        self.set_color(COLORS[self.current_color_index])
        self.pixels.show()

    def off(self):
        print("turning off the light")
        self.set_brightness(BRIGHTNESS_OFF)
        self.pixels.show()
        self.running = False
        
    def on(self):
        print(f"turning the light on again")
        self.set_brightness(self.current_brightness)
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
                    # Turning off the light when both buttons are pressed simultaneously
                    while self.button_color.value and self.button_bright.value and self.running:
                        self.off()
                        time.sleep(DELAY_ON_OFF)
                    # sets next defined color on all leds
                    while self.button_color.value and not self.button_bright.value:
                        self.next_color()
                        time.sleep(DELAY_SWITCH)
                    # increases brightness by step and if surpassing maximum begins at minimum
                    while self.button_bright.value and not self.button_color.value:
                        self.next_brightness()
                        time.sleep(DELAY_SWITCH)
                    time.sleep(DELAY_POLLING)
                # Waiting for button press in deactivated state - will turn on light with either button
                while (self.button_bright.value or self.button_color.value) and not self.running :
                    self.on()
                    time.sleep(DELAY_ON_OFF)
                time.sleep(DELAY_POLLING)
        finally:
            # Turning off the NeoPixels when script is stopped
            self.pixels.deinit()

if __name__ == "__main__":
    Pix()
