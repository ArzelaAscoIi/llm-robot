from enum import Enum
from typing import List, Dict
from llm_hexapot.freenove.Control import Control
from llm_hexapot.freenove.Command import COMMAND
import time


class GaitMode(Enum):
    MODE_1 = "1"
    MODE_2 = "2"


class ActionMode(Enum):
    ANGLELESS_TURN = "0"
    ACTION_1 = "10"


class MoveType(Enum):
    FORWARD = "forward"
    BACKWARD = "backward"
    LEFT = "left"
    RIGHT = "right"


class TiltDirection(Enum):
    FORWARD = "forward"
    BACKWARD = "backward"
    LEFT = "left"
    RIGHT = "right"


class MoveService:
    def __init__(self) -> None:
        self.control: Control = Control()
        self.move_type: MoveType = MoveType.FORWARD
        self.gait_mode: GaitMode = GaitMode.MODE_1
        self.action_mode: ActionMode = ActionMode.ANGLELESS_TURN
        self.speed: int = 35
        self.delay: int = 10

    def move(self, iterations: int = 1) -> None:
        x: int = 0
        y: int = 0
        if self.move_type == MoveType.FORWARD:
            y = self.speed
        elif self.move_type == MoveType.BACKWARD:
            y = -self.speed
        elif self.move_type == MoveType.LEFT:
            x = -self.speed
        elif self.move_type == MoveType.RIGHT:
            x = self.speed

        for _ in range(iterations):
            data: List[str] = [
                COMMAND.CMD_MOVE,
                self.gait_mode.value,
                str(x),
                str(y),
                str(self.delay),
                self.action_mode.value,
            ]
            self.control.run(data)

    def tilt(self, direction: TiltDirection, angle: int) -> None:
        if direction in [TiltDirection.FORWARD, TiltDirection.BACKWARD]:
            pitch = angle if direction == TiltDirection.FORWARD else -angle
            roll = 0
        else:  # LEFT or RIGHT
            pitch = 0
            roll = angle if direction == TiltDirection.LEFT else -angle

        data: List[str] = [
            COMMAND.CMD_ATTITUDE,
            str(pitch),  # pitch
            str(roll),  # roll
            "0",  # yaw (we're not changing yaw in this method)
            "5",  # time (in seconds) to complete the movement
            "0",  # reserved parameter, set to 0
        ]
        self.control.run(data)

    def demonstrate_all_moves(self, iterations_per_move: int = 2, delay_between_moves: float = 1.0) -> None:
        """
        Demonstrates all available move types.

        :param iterations_per_move: Number of iterations for each move type
        :param delay_between_moves: Delay in seconds between different move types
        """
        original_move_type = self.move_type
        original_speed = self.speed

        # Temporarily increase speed for more noticeable movements
        self.speed = 50

        for move_type in MoveType:
            print(f"Demonstrating {move_type.value}")
            self.move_type = move_type
            self.move(iterations=iterations_per_move)
            time.sleep(delay_between_moves)

        # Demonstrate tilting
        for tilt_direction in TiltDirection:
            print(f"Demonstrating tilt {tilt_direction.value}")
            self.tilt(direction=tilt_direction, angle=20)
            time.sleep(delay_between_moves)
            # Return to neutral position
            self.tilt(direction=tilt_direction, angle=0)
            time.sleep(delay_between_moves)

        # Reset to original settings
        self.move_type = original_move_type
        self.speed = original_speed
        print("Demonstration completed")


# Usage example:
if __name__ == "__main__":
    move_service = MoveService()
    move_service.demonstrate_all_moves()
