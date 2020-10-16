from mitsubishi_hvac_controller.hvac import HVAC
from hvac_ircontrol.mitsubishi import Mitsubishi, ISeeMode, AreaMode, PowerfulMode, FanMode, ClimateMode, \
    VanneHorizontalMode, VanneVerticalMode
hvac = HVAC()
req_form_variables = {'temp': 21,
                          'fan_mode': FanMode.Speed1,
                          'climate_mode': ClimateMode.Hot,
                          'vanne_horizontal_mode': VanneHorizontalMode.Middle,
                          'vanne_vertical_mode': VanneVerticalMode.MiddleBottom}
hvac.set_heat(**req_form_variables)
