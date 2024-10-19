from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from llm_hexapot.freenove.Control import Control

app = FastAPI()
control = Control()


class MoveCommand(BaseModel):
    gait: str
    x: int
    y: int
    speed: int
    angle: int


class PositionCommand(BaseModel):
    x: int
    y: int
    z: int


class AttitudeCommand(BaseModel):
    roll: int
    pitch: int
    yaw: int


class CalibrationCommand(BaseModel):
    leg: str
    x: int
    y: int
    z: int


@app.post("/move")
async def move(command: MoveCommand):
    try:
        control.run(
            [
                "CMD_MOVE",
                command.gait,
                str(command.x),
                str(command.y),
                str(command.speed),
                str(command.angle),
            ]
        )
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/position")
async def position(command: PositionCommand):
    try:
        control.posittion(command.x, command.y, command.z)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/attitude")
async def attitude(command: AttitudeCommand):
    try:
        point = control.postureBalance(command.roll, command.pitch, command.yaw)
        control.coordinateTransformation(point)
        control.setLegAngle()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/calibrate")
async def calibrate(command: CalibrationCommand):
    try:
        control.order = [
            "CMD_CALIBRATION",
            command.leg,
            str(command.x),
            str(command.y),
            str(command.z),
        ]
        control.condition()  # This will process the calibration command
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/balance")
async def balance():
    try:
        control.order = ["CMD_BALANCE", "1"]
        control.condition()  # This will start the balance mode
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/angles")
async def get_angles():
    try:
        angles = control.getAngles()
        return {"angles": angles}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/relax")
async def relax():
    try:
        control.relax(True)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
