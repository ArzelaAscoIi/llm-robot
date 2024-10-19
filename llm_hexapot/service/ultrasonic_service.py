from llm_hexapot.freenove.Ultrasonic import Ultrasonic


class UltrasonicService:
    def __init__(self):
        self.ultrasonic = Ultrasonic()

    def get_distance(self) -> float:
        return self.ultrasonic.get_distance()
