from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum

from llm_hexapot.service.servo_service import ServoService
from llm_hexapot.service.move_service import MoveService, MoveType, GaitMode, ActionMode
from llm_hexapot.service.led_service import LedService, LedMode
from llm_hexapot.service.ultrasonic_service import UltrasonicService
from llm_hexapot.service.buzzer_service import BuzzerService
from llm_hexapot.service.battery_service import BatteryService

app = FastAPI()

# Initialize services
servo_service = ServoService()
move_service = MoveService()
led_service = LedService()
ultrasonic_service = UltrasonicService()
buzzer_service = BuzzerService()
battery_service = BatteryService()


# Define request models
class ServoAngleRequest(BaseModel):
    servo_id: int
    angle: int


class CameraPositionRequest(BaseModel):
    x: int
    y: int


class MoveRequest(BaseModel):
    move_type: MoveType
    iterations: int = 1


class LedRequest(BaseModel):
    mode: LedMode
    r: int
    g: int
    b: int
    brightness: int


class BuzzerRequest(BaseModel):
    duration_ms: int


# Define endpoints
@app.post("/servo/angle")
async def set_servo_angle(request: ServoAngleRequest):
    servo_service.set_angle(request.servo_id, request.angle)
    return {"message": "Servo angle set successfully"}


@app.post("/servo/camera")
async def set_camera_position(request: CameraPositionRequest):
    servo_service.set_camera_position(request.x, request.y)
    return {"message": "Camera position set successfully"}


@app.post("/move")
async def move_robot(request: MoveRequest):
    move_service.move_type = request.move_type
    move_service.move(request.iterations)
    return {"message": f"Robot moved {request.move_type.value} for {request.iterations} iterations"}


@app.post("/led")
async def set_led(request: LedRequest):
    led_service.set_mode(request.mode)
    led_service.set_color(request.r, request.g, request.b)
    led_service.set_brightness(request.brightness)
    led_service.apply()
    return {"message": "LED set successfully"}


@app.post("/buzzer")
async def set_buzzer(request: BuzzerRequest):
    buzzer_service.beep(request.duration_ms)
    return {"message": "Buzzer set successfully"}
