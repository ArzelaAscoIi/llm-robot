from enum import Enum
from typing import List, Dict
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
        tilt_command: Dict[TiltDirection, str] = {
            TiltDirection.FORWARD: COMMAND.CMD_ATTITUDE,
            TiltDirection.BACKWARD: COMMAND.CMD_ATTITUDE,
            TiltDirection.LEFT: COMMAND.CMD_ATTITUDE,
            TiltDirection.RIGHT: COMMAND.CMD_ATTITUDE,
        }

        if direction in [TiltDirection.BACKWARD, TiltDirection.RIGHT]:
            angle = -angle

        data: List[str] = [tilt_command[direction], str(angle)]
        self.control.run(data)
