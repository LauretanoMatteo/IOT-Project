from machine import Pin,PWM, I2C
import ssd1306
import time


class display_proj:
    def __init__(self,Pin_scl,Pin_sda):
        i2c = I2C(0, scl=Pin(Pin_scl), sda=Pin(Pin_sda))
        oled_width = 128
        oled_height = 64
        self.oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

    #cleaning display method
    def clear(self):
        self.oled.fill(0)

    #method to print the message on the display
    def write(self,message,posx,posy):
        self.oled.text(""+message,posx,posy)
        self.oled.show()

  

