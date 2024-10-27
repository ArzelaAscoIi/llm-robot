from enum import Enum
from typing import Tuple
from llm_hexapot.freenove.Led import Led, Color


class LedMode(Enum):
    SOLID = "solid"
    BLINK = "blink"
    BREATHE = "breathe"


class LedService:
    def __init__(self) -> None:
        self.led: Led = Led()
        self.strip = self.led.strip  # Add reference to LED strip
        self.color: Tuple[int, int, int] = (255, 255, 255)  # Default to white
        self.brightness: int = 100  # 0-100
        self.mode: LedMode = LedMode.SOLID  # Add default mode

    def set_mode(self, mode: LedMode) -> None:
        self.mode = mode

    def set_color(self, r: int, g: int, b: int) -> None:
        self.color = (r, g, b)

    def set_brightness(self, brightness: int) -> None:
        self.brightness = max(0, min(100, brightness))

    def apply(self) -> None:
        # Convert RGB values to Color object and apply to strip
        color_obj = Color(self.color[0], self.color[1], self.color[2])
        self.led.colorWipe(self.strip, color_obj)

    def turn_off(self) -> None:
        # Helper method to turn off the LED strip
        self.led.colorWipe(self.strip, Color(0, 0, 0))
