from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from enum import Enum
from typing import Dict, Any
import tempfile
import os

# Define base URL
BASE_URL = "https://59f1-2a02-908-5b0-7f40-00-96dd.ngrok-free.app"

from llm_hexapot.service.servo_service import ServoService
from llm_hexapot.service.move_service import MoveService, MoveType, GaitMode, ActionMode
from llm_hexapot.service.led_service import LedService, LedMode
from llm_hexapot.service.ultrasonic_service import UltrasonicService
from llm_hexapot.service.buzzer_service import BuzzerService
from llm_hexapot.service.battery_service import BatteryService
from llm_hexapot.service.camera_service import CameraService

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
camera_service = CameraService()


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


class TurnRequest(BaseModel):
    direction: MoveType = Field(..., description="The direction to turn (TURN_LEFT or TURN_RIGHT)")
    iterations: int = Field(1, description="The number of times to repeat the turn (default is 1)")


# Define response models
class MessageResponse(BaseModel):
    message: str


class MoveResponse(BaseModel):
    message: str


@app.post("/servo/camera", response_model=MessageResponse)
async def set_camera_position(request: CameraPositionRequest) -> Dict[str, Any]:
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


@app.post("/move", response_model=MoveResponse)
async def move_robot(request: MoveRequest) -> Dict[str, Any]:
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


@app.post("/led", response_model=MessageResponse)
async def set_led(request: LedRequest) -> Dict[str, Any]:
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


@app.post("/buzzer", response_model=MessageResponse)
async def set_buzzer(request: BuzzerRequest) -> Dict[str, Any]:
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


@app.get("/camera/photo", response_class=FileResponse)
async def take_photo():
    """
    Take a photo using the hexapod's camera and return it.

    This endpoint triggers the camera to capture a photo and returns the image file.

    Returns:
    - A JPEG image file of the captured photo.

    Raises:
    - HTTPException: If there's an error capturing or saving the photo.
    """
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            photo_path = temp_file.name

            camera_service.capture_photo(photo_path)
            return FileResponse(photo_path, media_type="image/jpeg", filename="hexapod_photo.jpg")
    finally:
        # Clean up the temporary file
        if "photo_path" in locals():
            os.unlink(photo_path)


@app.post("/turn", response_model=MoveResponse)
async def turn_robot(request: TurnRequest) -> Dict[str, Any]:
    """
    Command the hexapod robot to turn left or right.

    This endpoint allows you to control the robot's turning movement by specifying
    the direction and number of iterations.

    Parameters:
    - direction (MoveType): The direction to turn. Must be either:
        - TURN_LEFT: Turn the robot left
        - TURN_RIGHT: Turn the robot right
    - iterations (int): The number of times to repeat the turn (default is 1)

    Returns:
    - A JSON object with a message describing the executed turn.

    Raises:
    - HTTPException (400): If the direction is not TURN_LEFT or TURN_RIGHT
    - HTTPException: If iterations is less than 1.
    """
    if request.direction not in [MoveType.TURN_LEFT, MoveType.TURN_RIGHT]:
        raise HTTPException(status_code=400, detail="Direction must be TURN_LEFT or TURN_RIGHT")

    move_service.turn(request.direction, request.iterations)
    return {"message": f"Robot turned {request.direction.value} for {request.iterations} iterations"}
