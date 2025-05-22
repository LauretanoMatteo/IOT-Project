from machine import Pin,PWM, I2C
from buzzer_G21 import *
import time
from display_G21 import *
import buzzer_G21

class engine:
    def __init__(self,pin_pwm0,freq_pwm0):
        self.pwm0=PWM(Pin(pin_pwm0),freq=freq_pwm0)
        self.start = 0
        self.opened = False

    #set opening door angle
    def setAngle(self,angle):
        duty_min=26 #0
        duty_max=123 #180
        self.pwm0.duty(int(duty_min+(angle/180)*(duty_max-duty_min)))

    #emanation function
    def dispense(self,buzzer,display,opening_angle,opening_time):
        self.setAngle(90-opening_angle)
        count=opening_time
        while count!=0:
            display.clear()
            display.write("Mancano: "+str(count)+"s",8,10)
            count=count-1
            time.sleep(1)       
        self.setAngle(90)
        display.clear()
        display.write("Fine erogazione",8,10)
        buzzer.play(buzzer_G21.song,500,512)
    
    #opening management function
    def opening(self,btn1):
        current=time.ticks_ms()#inizia a contare 
        delta=time.ticks_diff(current,self.start)
        if delta<100:
            return 
        
        self.start=current
        self.opened=not self.opened
        
