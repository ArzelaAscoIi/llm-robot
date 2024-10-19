from llm_hexapot.freenove.ADC import ADC


class BatteryService:
    def __init__(self):
        self.adc = ADC()

    def get_voltage(self) -> tuple[float, float]:
        return self.adc.batteryPower()

    def is_low_battery(self) -> bool:
        voltage = self.get_voltage()
        return voltage[0] < 5.5 or voltage[1] < 6
