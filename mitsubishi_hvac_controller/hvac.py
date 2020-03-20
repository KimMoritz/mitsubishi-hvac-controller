import hvac_ircontrol
from hvac_ircontrol.ir_sender import LogLevel
from hvac_ircontrol.mitsubishi import Mitsubishi, ISeeMode, AreaMode, PowerfulMode, FanMode, ClimateMode, \
    VanneHorizontalMode, VanneVerticalMode


class HVAC:

    def __init__(self):
        self.mitsubishi = Mitsubishi(22, LogLevel.ErrorsOnly)
        self.temps = {'16': 16, '17': 17, '18': 18, '19': 19, '20': 20, '21': 21, '22': 22, '23': 23}
        self.fan_modes = {'Auto': FanMode.Auto,
                     'Speed1': FanMode.Speed1,
                     'Speed2': FanMode.Speed2,
                     'Speed3': FanMode.Speed3}
        self.climate_modes = {'Hot': ClimateMode.Hot,
                         'Cold': ClimateMode.Cold,
                         'Auto': ClimateMode.Auto,
                         'Dry': ClimateMode.Dry}
        self.vanne_horizontal_modes = {'Left': VanneHorizontalMode.Left,
                                  'MiddleLeft': VanneHorizontalMode.MiddleLeft,
                                  'Middle': VanneHorizontalMode.Middle,
                                  'MiddleRight': VanneHorizontalMode.MiddleRight,
                                  'Right': VanneHorizontalMode.Right,
                                  'Swing': VanneHorizontalMode.Swing,
                                  'NotSet': VanneHorizontalMode.NotSet}
        self.vanne_vertical_modes = {'Auto': VanneVerticalMode.Auto,
                                'Bottom': VanneVerticalMode.Bottom,
                                'MiddleBottom': VanneVerticalMode.MiddleBottom,
                                'Middle': VanneVerticalMode.Middle,
                                'MiddleTop': VanneVerticalMode.MiddleTop,
                                'Top': VanneVerticalMode.Top}

    def set_heat(self, temp, fan_mode, climate_mode, vanne_horizontal_mode, vanne_vertical_mode):
        print("Setting HVAC to : " + str(temp) + str(fan_mode) + str(climate_mode) +
              str(vanne_horizontal_mode) + str(vanne_horizontal_mode))

        self.mitsubishi.send_command(
            climate_mode=int(climate_mode),
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

    def get_hvac_variables(self):
        variables = {'temps': self.temps,
                     'fan_modes': self.fan_modes,
                     'climate_modes': self.climate_modes,
                     'vanne_horizontal_modes': self.vanne_horizontal_modes,
                     'vanne_vertical_modes': self.vanne_vertical_modes}
        return variables
