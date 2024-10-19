import time
from typing import NoReturn
from Led import Led, Color
from Ultrasonic import Ultrasonic
from Servo import Servo
from ADC import ADC
from Buzzer import Buzzer
from Control import Control  # Assuming Control is needed, though not used in the provided code

led = Led()
ultrasonic = Ultrasonic()
servo = Servo()
adc = ADC()
buzzer = Buzzer()


def test_Led() -> None:
    try:
        # Red wipe
        print("\nRed wipe")
        led.colorWipe(led.strip, Color(255, 0, 0))
        time.sleep(1)

        # Green wipe
        print("\nGreen wipe")
        led.colorWipe(led.strip, Color(0, 255, 0))
        time.sleep(1)

        # Blue wipe
        print("\nBlue wipe")
        led.colorWipe(led.strip, Color(0, 0, 255))
        time.sleep(1)

        # White wipe
        print("\nWhite wipe")
        led.colorWipe(led.strip, Color(255, 255, 255))
        time.sleep(1)

        led.colorWipe(led.strip, Color(0, 0, 0))  # turn off the light
        print("\nEnd of program")
    except KeyboardInterrupt:
        led.colorWipe(led.strip, Color(0, 0, 0))  # turn off the light
        print("\nEnd of program")


def test_Ultrasonic() -> NoReturn:
    try:
        while True:
            data: float = ultrasonic.getDistance()  # Get the value
            print(f"Obstacle distance is {data} CM")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nEnd of program")


def test_Servo() -> None:
    try:
        for i in range(50):
            servo.setServoAngle(15, 90 + i)
            servo.setServoAngle(12, 90 + i)
            servo.setServoAngle(9, 90 + i)
            servo.setServoAngle(16, 90 + i)
            servo.setServoAngle(19, 90 + i)
            servo.setServoAngle(22, 90 + i)
            time.sleep(0.005)
        for i in range(60):
            servo.setServoAngle(14, 90 + i)
            servo.setServoAngle(11, 90 + i)
            servo.setServoAngle(8, 90 + i)
            servo.setServoAngle(17, 90 - i)
            servo.setServoAngle(20, 90 - i)
            servo.setServoAngle(23, 90 - i)
            time.sleep(0.005)
        for i in range(120):
            servo.setServoAngle(13, i)
            servo.setServoAngle(10, i)
            servo.setServoAngle(31, i)
            servo.setServoAngle(18, 180 - i)
            servo.setServoAngle(21, 180 - i)
            servo.setServoAngle(27, 180 - i)
            time.sleep(0.005)
        print("\nEnd of program")
    except KeyboardInterrupt:
        print("\nEnd of program")


def test_Adc() -> NoReturn:
    try:
        while True:
            power: float = adc.batteryPower()
            print(f"The battery voltage is {power}\n")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nEnd of program")


def test_Buzzer() -> None:
    try:
        buzzer.run("1")
        time.sleep(1)
        print("1S")
        time.sleep(1)
        print("2S")
        time.sleep(1)
        print("3S")
        buzzer.run("0")
        print("\nEnd of program")
    except KeyboardInterrupt:
        buzzer.run("0")
        print("\nEnd of program")


import threading
from Control import *


# Main program logic follows:
def aa() -> NoReturn:
    while True:
        test_Led()
        # power = adc.batteryPower()
        # print(f"The battery voltage is {power}\n")
        data: float = ultrasonic.getDistance()  # Get the value
        print(f"Obstacle distance is {data} CM")


def bb() -> NoReturn:
    while True:
        for i in range(30, 150, 1):
            servo.setServoAngle(1, i)
            time.sleep(0.05)
        for i in range(150, 30, -1):
            servo.setServoAngle(1, i)
            time.sleep(0.05)
        for i in range(90, 150, 1):
            servo.setServoAngle(0, i)
            time.sleep(0.05)
        for i in range(150, 90, -1):
            servo.setServoAngle(0, i)
            time.sleep(0.05)
