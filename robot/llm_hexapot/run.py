import time
from typing import Tuple

from llm_hexapot.service.move_service import MoveService, MoveType
from llm_hexapot.service.led_service import LedService, LedMode
from llm_hexapot.service.buzzer_service import BuzzerService
from llm_hexapot.service.battery_service import BatteryService
from llm_hexapot.service.ultrasonic_service import UltrasonicService
from llm_hexapot.service.servo_service import ServoService


class HexapodController:
    def __init__(self) -> None:
        self.move_service: MoveService = MoveService()
        self.led_service: LedService = LedService()
        self.buzzer_service: BuzzerService = BuzzerService()
        self.battery_service: BatteryService = BatteryService()
        self.ultrasonic_service: UltrasonicService = UltrasonicService()
        self.servo_service: ServoService = ServoService()

    def run_demo(self) -> None:
        print("Starting Hexapod Demo")

        # Check battery
        voltage: Tuple[float, float] = self.battery_service.get_voltage()
        print(f"Battery voltage: {voltage[0]}V, {voltage[1]}V")
        if self.battery_service.is_low_battery():
            print("Warning: Low battery!")
            self.buzzer_service.play_pattern([(True, 200), (False, 100)] * 3)

        # Set LED color
        self.led_service.set_color(255, 0, 0)  # Red
        self.led_service.set_mode(LedMode.BREATHE)
        self.led_service.apply()

        # Move forward
        print("Moving forward")
        self.move_service.move_type = MoveType.FORWARD
        self.move_service.move(iterations=5)

        # Check distance
        distance = self.ultrasonic_service.get_distance()
        print(f"Distance to nearest object: {distance:.2f} cm")

        # Turn camera
        print("Moving camera")
        self.servo_service.set_camera_position(90, 45)
        time.sleep(1)
        self.servo_service.set_camera_position(70, 30)

        # Move backward
        print("Moving backward")
        self.move_service.move_type = MoveType.BACKWARD
        self.move_service.move(iterations=5)

        # Change LED color
        self.led_service.set_color(0, 255, 0)  # Green
        self.led_service.set_mode(LedMode.BLINK)
        self.led_service.apply()

        # Turn left
        print("Turning left")
        self.move_service.move_type = MoveType.LEFT
        self.move_service.move(iterations=3)

        # Turn right
        print("Turning right")
        self.move_service.move_type = MoveType.RIGHT
        self.move_service.move(iterations=3)

        # Final beep
        self.buzzer_service.beep(500)

        print("Demo completed")


if __name__ == "__main__":
    controller: HexapodController = HexapodController()
    controller.run_demo()
