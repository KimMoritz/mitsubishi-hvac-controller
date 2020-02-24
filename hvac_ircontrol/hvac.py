from hvac_ircontrol.ir_sender import LogLevel
from hvac_ircontrol.mitsubishi import Mitsubishi, ClimateMode, FanMode, VanneVerticalMode, VanneHorizontalMode, \
    ISeeMode, AreaMode, PowerfulMode


class HVAC:

    def __init__(self):
        self.mitsubishi = Mitsubishi(22, LogLevel.ErrorsOnly)

    def set_heat(self, temp, fan_mode, climate_mode, vanne_horizontal_mode, vanne_vertical_mode):
        print("Setting heating to {} degrees Celsius, Speed1, Vertical Bottom, Horizontal Middle.".format(temp))
        print(str(temp) + str(fan_mode) + str(climate_mode) + str(vanne_horizontal_mode) + str(vanne_horizontal_mode))

        self.mitsubishi.send_command(
            climate_mode=climate_mode,
            temperature=temp,
            fan_mode=fan_mode,
            vanne_vertical_mode=vanne_vertical_mode,
            vanne_horizontal_mode=vanne_horizontal_mode,
            isee_mode=ISeeMode.ISeeOff,
            area_mode=AreaMode.Full,
            powerful=PowerfulMode.PowerfulOff)

    def turn_off(self):
        print("Turning off")
        self.mitsubishi.power_off()
