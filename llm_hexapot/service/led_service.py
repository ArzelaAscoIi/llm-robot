from enum import Enum
from typing import List
from llm_hexapot.freenove.Led import Led, Color


class LedMode(Enum):
    SOLID = "solid"
    BLINK = "blink"
    BREATHE = "breathe"


class LedService:
    def __init__(self):
        self.led = Led()
        self.strip = self.led.strip  # Add reference to LED strip
        self.color = (255, 255, 255)  # Default to white
        self.brightness = 100  # 0-100

    def set_mode(self, mode: LedMode):
        self.mode = mode

    def set_color(self, r: int, g: int, b: int):
        self.color = (r, g, b)

    def set_brightness(self, brightness: int):
        self.brightness = max(0, min(100, brightness))

    def apply(self):
        # Convert RGB values to Color object and apply to strip
        color_obj = Color(self.color[0], self.color[1], self.color[2])
        self.led.colorWipe(self.strip, color_obj)

    def turn_off(self):
        # Helper method to turn off the LED strip
        self.led.colorWipe(self.strip, Color(0, 0, 0))
