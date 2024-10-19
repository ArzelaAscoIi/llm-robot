from enum import Enum
from typing import List
from llm_hexapot.freenove.Led import Led


class LedMode(Enum):
    SOLID = "solid"
    BLINK = "blink"
    BREATHE = "breathe"


class LedService:
    def __init__(self):
        self.led = Led()
        self.mode = LedMode.SOLID
        self.color = (255, 255, 255)  # Default to white
        self.brightness = 100  # 0-100

    def set_mode(self, mode: LedMode):
        self.mode = mode

    def set_color(self, r: int, g: int, b: int):
        self.color = (r, g, b)

    def set_brightness(self, brightness: int):
        self.brightness = max(0, min(100, brightness))

    def apply(self):
        # Convert the LedService parameters to the format expected by the Led class
        data: List[str] = [
            "CMD_LED",
            self.mode.value,
            f"{self.color[0]},{self.color[1]},{self.color[2]}",
            str(self.brightness),
        ]
        self.led.light(data)
