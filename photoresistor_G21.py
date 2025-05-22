from machine import Pin,ADC

class LDR:
    #This class read a value from a light dependent resistor
    
    def __init__(self, pin, min_value = 0, max_value =100):
        if min_value>=max_value:
            raise Exception('Min value is greater or equal to max value')
        self.adc = ADC(Pin(pin))
        self.min_value = min_value
        self.max_value = max_value

    #reading value   
    def read(self):
        return self.adc.read()    
    
    #return value in the correct range
    def value(self):
        return (self.max_value - self.min_value) * self.read() /4095
    
