from llm_hexapot.freenove.Buzzer import Buzzer


class BuzzerService:
    def __init__(self):
        self.buzzer = Buzzer()

    def beep(self, duration_ms: int):
        self.buzzer.run("1")
        # You might need to implement a non-blocking delay here
        # For now, we'll use a simple time.sleep
        import time

        time.sleep(duration_ms / 1000)
        self.buzzer.run("0")

    def play_pattern(self, pattern: list[tuple[bool, int]]):
        for state, duration in pattern:
            self.buzzer.run("1" if state else "0")
            import time

            time.sleep(duration / 1000)
