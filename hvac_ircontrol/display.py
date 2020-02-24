from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

class Display:
    i2c = busio.I2C(SCL, SDA)
    disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
    width = disp.width
    height = disp.height
    padding = -2
    top = padding
    bottom = height - padding
    x = 0
    font = ImageFont.load_default()

    def __init__(self):
        disp = self.disp
        disp.fill(0)
        disp.show()
        image = Image.new('1', (self.width, self.height))
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

    def turn_off(self):
        disp = self.disp
        disp.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
        image = Image.new('1', (self.width, self.height))
        disp.image(image)
        disp.show()

    def show_settings(self, temp, speed):
            image = Image.new('1', (self.width, self.height))
            draw = ImageDraw.Draw(image)
            draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
            draw.text((self.x, self.top+0), "Temperatur: " + str(temp) + " °C, " + speed, font=self.font, fill=255)
            self.disp.image(image)
            self.disp.show()
