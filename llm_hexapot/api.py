from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from enum import Enum

# Define base URL
BASE_URL = "https://5567-2a02-908-5b0-7f40-00-96dd.ngrok-free.app"

from llm_hexapot.service.servo_service import ServoService
from llm_hexapot.service.move_service import MoveService, MoveType, GaitMode, ActionMode
from llm_hexapot.service.led_service import LedService, LedMode
from llm_hexapot.service.ultrasonic_service import UltrasonicService
from llm_hexapot.service.buzzer_service import BuzzerService
from llm_hexapot.service.battery_service import BatteryService

app = FastAPI(
    title="Hexapod API",
    description="API for controlling the Hexapod robot. This specification outlines a set of functions to manipulate various aspects of a six-legged robot, including servo motors, movement, LED lights, camera positioning, buzzer, and more.",
    version="1.0.0",
    servers=[
        {"url": BASE_URL, "description": "Production server"},
    ],
)

# Initialize services
servo_service = ServoService()
move_service = MoveService()
led_service = LedService()
ultrasonic_service = UltrasonicService()
buzzer_service = BuzzerService()
battery_service = BatteryService()


# Define request models
class ServoAngleRequest(BaseModel):
    servo_id: int = Field(..., description="The unique identifier of the servo motor (1-18)")
    angle: int = Field(..., description="The desired angle for the servo, typically in the range of 0-180 degrees")


class CameraPositionRequest(BaseModel):
    x: int = Field(..., description="The horizontal position of the camera, typically in the range of 0-180 degrees")
    y: int = Field(..., description="The vertical position of the camera, typically in the range of 0-180 degrees")


class MoveRequest(BaseModel):
    move_type: MoveType = Field(
        ..., description="The type of movement to perform (e.g., FORWARD, BACKWARD, LEFT, RIGHT, UP, DOWN)"
    )
    iterations: int = Field(1, description="The number of times to repeat the movement (default is 1)")


class LedRequest(BaseModel):
    mode: LedMode = Field(..., description="The lighting mode to set (e.g., STATIC, BREATHING, RAINBOW)")
    r: int = Field(..., ge=0, le=255, description="Red color component (0-255)")
    g: int = Field(..., ge=0, le=255, description="Green color component (0-255)")
    b: int = Field(..., ge=0, le=255, description="Blue color component (0-255)")
    brightness: int = Field(..., ge=0, le=100, description="Overall brightness of the LEDs (0-100)")


class BuzzerRequest(BaseModel):
    duration_ms: int = Field(..., gt=0, description="The duration of the beep in milliseconds")


# Define endpoints
@app.post("/servo/angle")
async def set_servo_angle(request: ServoAngleRequest):
    """
    Set the angle of a specific servo motor.

    This endpoint allows you to control individual servo motors on the hexapod robot.
    You can specify the servo ID and the desired angle to position the servo.

    Parameters:
    - servo_id (int): The unique identifier of the servo motor (1-18).
    - angle (int): The desired angle for the servo, typically in the range of 0-180 degrees.

    The servo_id corresponds to the following:
    - 1-6: Coxa servos (hip joints)
    - 7-12: Femur servos (thigh joints)
    - 13-18: Tibia servos (knee joints)

    This function calls the ServoService to apply the requested angle to the specified servo.

    Returns:
    - A JSON object with a success message.

    Raises:
    - HTTPException: If the servo_id or angle is out of the valid range.
    """
    servo_service.set_angle(request.servo_id, request.angle)
    return {"message": "Servo angle set successfully"}


@app.post("/servo/camera")
async def set_camera_position(request: CameraPositionRequest):
    """
    Set the position of the camera mount servos.

    This endpoint controls the two servos responsible for the camera's pan and tilt movements.
    You can adjust the camera's horizontal (x) and vertical (y) positions.

    Parameters:
    - x (int): The horizontal position of the camera, typically in the range of 0-180 degrees.
    - y (int): The vertical position of the camera, typically in the range of 0-180 degrees.

    This function calls the ServoService to apply the requested positions to the camera mount servos.

    Returns:
    - A JSON object with a success message.

    Raises:
    - HTTPException: If the x or y values are out of the valid range.
    """
    servo_service.set_camera_position(request.x, request.y)
    return {"message": "Camera position set successfully"}


@app.post("/move")
async def move_robot(request: MoveRequest):
    """
    Command the hexapod robot to perform a specific movement.

    This endpoint allows you to control the robot's movement by specifying a move type and the number of iterations.

    Parameters:
    - move_type (MoveType): The type of movement to perform. Options include:
        - FORWARD: Move the robot forward
        - BACKWARD: Move the robot backward
        - LEFT: Turn the robot left
        - RIGHT: Turn the robot right
        - UP: Raise the robot's body
        - DOWN: Lower the robot's body
    - iterations (int): The number of times to repeat the movement (default is 1)

    This function sets the move type on the MoveService and then calls the move method with the specified iterations.

    Returns:
    - A JSON object with a message describing the executed movement.

    Raises:
    - HTTPException: If an invalid move type is provided or if iterations is less than 1.
    """
    move_service.move_type = request.move_type
    move_service.move(request.iterations)
    return {"message": f"Robot moved {request.move_type.value} for {request.iterations} iterations"}


@app.post("/led")
async def set_led(request: LedRequest):
    """
    Control the LED lights on the hexapod robot.

    This endpoint allows you to set the LED mode, color, and brightness of the robot's LED lights.

    Parameters:
    - mode (LedMode): The lighting mode to set. Options include:
        - STATIC: Constant color
        - BREATHING: Pulsing effect
        - RAINBOW: Cycling through colors
    - r (int): Red color component (0-255)
    - g (int): Green color component (0-255)
    - b (int): Blue color component (0-255)
    - brightness (int): Overall brightness of the LEDs (0-100)

    This function calls the LedService to set the mode, color, and brightness, then applies the changes.

    Returns:
    - A JSON object with a success message.

    Raises:
    - HTTPException: If invalid color values or brightness are provided.
    """
    led_service.set_mode(request.mode)
    led_service.set_color(request.r, request.g, request.b)
    led_service.set_brightness(request.brightness)
    led_service.apply()
    return {"message": "LED set successfully"}


@app.post("/buzzer")
async def set_buzzer(request: BuzzerRequest):
    """
    Activate the buzzer on the hexapod robot.

    This endpoint allows you to make the robot's buzzer beep for a specified duration.

    Parameters:
    - duration_ms (int): The duration of the beep in milliseconds.

    This function calls the BuzzerService to activate the buzzer for the specified duration.

    Returns:
    - A JSON object with a success message.

    Raises:
    - HTTPException: If the duration is negative or exceeds a maximum allowed value.
    """
    buzzer_service.beep(request.duration_ms)
    return {"message": "Buzzer set successfully"}
