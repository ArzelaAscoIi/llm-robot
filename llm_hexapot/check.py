# from llm_hexapot.freenove.test.ultrasonic import test_Ultrasonic
# from llm_hexapot.freenove.test.servo import test_Servo
# from llm_hexapot.freenove.test.adc import test_Adc
# from llm_hexapot.freenove.test.buzzer import test_Buzzer


from llm_hexapot.freenove.Led import *

led = Led()


def test_Led():
    if led.Ledsupported == 1:
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
    else:
        try:
            print("\nRaspberry PI 5 is currently being used, which is unsupported hardware.")
        except KeyboardInterrupt:
            print("\nEnd of program")


from llm_hexapot.freenove.Buzzer import *

buzzer = Buzzer()


def test_Buzzer():
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


from llm_hexapot.freenove.ADC import *

adc = ADC()


def test_Adc():
    try:
        while True:
            Power = adc.batteryPower()
            print("The battery voltage is " + str(Power) + "\n")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nEnd of program")


from llm_hexapot.freenove.Servo import *

servo = Servo()


def test_Servo():
    try:
        for i in range(50):
            servo.setServoAngle(15, 90 + i)
            servo.setServoAngle(12, 90 + i)
            servo.setServoAngle(9, 90 + i)
            servo.setServoAngle(16, 90 + i)
            servo.setServoAngle(19, 90 + i)
            servo.setServoAngle(22, 90 + i)
            time.sleep(0.01)
        for i in range(60):
            servo.setServoAngle(14, 90 + i)
            servo.setServoAngle(11, 90 + i)
            servo.setServoAngle(8, 90 + i)
            servo.setServoAngle(17, 90 - i)
            servo.setServoAngle(20, 90 - i)
            servo.setServoAngle(23, 90 - i)
            time.sleep(0.01)
        for i in range(120):
            servo.setServoAngle(13, i)
            servo.setServoAngle(10, i)
            servo.setServoAngle(31, i)
            servo.setServoAngle(18, 180 - i)
            servo.setServoAngle(21, 180 - i)
            servo.setServoAngle(27, 180 - i)
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("\nEnd of program")


from llm_hexapot.freenove.Ultrasonic import *

ultrasonic = Ultrasonic()


def test_Ultrasonic():
    try:
        while True:
            data = ultrasonic.get_distance()  # Get the value
            print("Obstacle distance is " + str(data) + "CM")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nEnd of program")


def main():
    print("Program is starting ... ")

    # test_Led()
    # test_Buzzer()
    # test_Adc()
    test_Servo()
    # test_Ultrasonic()

    # if len(sys.argv) < 2:
    #     print("Parameter error: Please assign the device")
    #     exit()
    # if sys.argv[1] == "Led":
    #     test_Led()
    # elif sys.argv[1] == "Ultrasonic":
    #     test_Ultrasonic()
    # elif sys.argv[1] == "Servo":
    #     test_Servo()
    # elif sys.argv[1] == "ADC":
    #     test_Adc()
    # elif sys.argv[1] == "Buzzer":
    #     test_Buzzer()


if __name__ == "__main__":
    main()
