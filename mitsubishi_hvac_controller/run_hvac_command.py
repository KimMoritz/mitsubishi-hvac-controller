from hvac_ircontrol.mitsubishi import Mitsubishi, ISeeMode, AreaMode, PowerfulMode, FanMode, ClimateMode, \
    VanneHorizontalMode, VanneVerticalMode
hvac = HVAC()
mitsubishi = Mitsubishi(22, LogLevel.ErrorsOnly)
self.mitsubishi.send_command(
            climate_mode=ClimateMode.Hot,
            temperature=21,
            fan_mode=FanMode.Speed1,
            vanne_vertical_mode=VanneVerticalMode.MiddleBottom,
            vanne_horizontal_mode=VanneHorizontalMode.Middle,
            isee_mode=ISeeMode.ISeeOff,
            area_mode=AreaMode.Full,
            powerful=PowerfulMode.PowerfulOff)
hvac.set_heat(**req_form_variables)
