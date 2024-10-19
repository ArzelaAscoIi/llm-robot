from llm_hexapot.freenove.test import test_Led
# from llm_hexapot.freenove.test.ultrasonic import test_Ultrasonic
# from llm_hexapot.freenove.test.servo import test_Servo
# from llm_hexapot.freenove.test.adc import test_Adc
# from llm_hexapot.freenove.test.buzzer import test_Buzzer


def main():
    print("Program is starting ... ")
    import sys
    test_Led()

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
