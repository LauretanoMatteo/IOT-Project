from buzzer_G21 import *
from display_G21 import *
from engine_G21 import *


class emergency_state:
    def __init__(self):
        self.state_em = False
        self.start = 0
    
    #emergency state management
    def management(self,display,led,buzzer,engine):
        engine.setAngle(90)
        engine.opened = False
        display.write("Riempire ",10,0)
        display.write("Dispenser ",10,10)
        self.blinking(led)
        buzzer.play(buzzer_G21.emergency,500,512) 
        display.clear()

    #led blinking
    def blinking(self,led):
        count = 4
        while count>=0:
            led.value(not led.value())
            time.sleep(1)
            count-= 1

    #change of state_em value
    def change_state_em(self,infrared_sens) :
        current=time.ticks_ms()#inizia a contare 
        delta=time.ticks_diff(current,self.start)
        if delta<50:
            return 
        print("MUUU")
        self.start=current
        self.state_em = not self.state_em
