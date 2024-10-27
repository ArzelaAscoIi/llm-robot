from llm_hexapot.freenove.Servo import Servo


class ServoService:
    def __init__(self):
        self.servo = Servo()

    def set_angle(self, servo_id: int, angle: int):
        self.servo.setServoAngle(servo_id, angle)

    def set_camera_position(self, x: int, y: int):
        x = max(50, min(180, x))
        y = max(0, min(180, y))
        self.set_angle(0, x)
        self.set_angle(1, y)
