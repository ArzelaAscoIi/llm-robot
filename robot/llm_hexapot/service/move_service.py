from enum import Enum
from typing import List
from llm_hexapot.freenove.Control import Control
from llm_hexapot.freenove.Command import COMMAND


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
    TURN_LEFT = "turn_left"
    TURN_RIGHT = "turn_right"


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

    def turn(self, direction: MoveType, iterations: int = 1) -> None:
        """Execute a turning movement in the specified direction.

        Args:
            direction: MoveType.TURN_LEFT or MoveType.TURN_RIGHT
            iterations: Number of movement cycles
        """
        if direction not in [MoveType.TURN_LEFT, MoveType.TURN_RIGHT]:
            raise ValueError("Direction must be TURN_LEFT or TURN_RIGHT")

        self.move_type = direction
        x = self.speed if direction == MoveType.TURN_RIGHT else -self.speed

        for _ in range(iterations):
            data: List[str] = [
                COMMAND.CMD_MOVE,
                self.gait_mode.value,
                str(x),
                "0",  # y is always 0 for turning
                str(self.delay),
                self.action_mode.value,
            ]
            self.control.run(data)
