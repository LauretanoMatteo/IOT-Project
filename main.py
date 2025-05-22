import network
import utime
import ntptime
import ujson
from display_G21 import *
from buzzer_G21 import *
from photoresistor_G21 import *
from engine_G21 import *
from emergency_state_G21 import *
from umqtt.simple import MQTTClient


#Method to manage the arrival of messages on the client
def subCallback(topic,msg):
    global opening_angle
    global opening_time
    global remote_emanation
    if topic == MQTT_EROGAZIONE:
        payload = ujson.loads(msg)
        opening_angle = payload ["Angolazione"]
        opening_time = payload ["Tempo"]
        remote_emanation = True

#parameters for managing the door opening inizialization
opening_angle = 90
opening_time = 4

#Initialization of variable to check if the dispensing has been requested from the dashboard
remote_emanation = False

##Initialization of variables for printing date and time. At startup, they have the value "Nessuna erogazione"
date = "Nessuna"
hour = "Erogazione"

MQTT_CLIENT_ID = "G21_ProgettoIoT"
MQTT_BROKER    = "broker.hivemq.com"
MQTT_USER      = ""
MQTT_PASSWORD  = ""
MQTT_TOPIC     = "unisa_iot/p01/G21Project"
MQTT_EROGAZIONE = b'unisa_iot/p01/G21Project_erogazione'
MQTT_EMERGENCY = b'unisa_iot/p01/G21Project_emergency'
MQTT_NOEMERGENCY = b'unisa_iot/p01/G21Project_noemergency'

print("Connecting to WiFi", end="")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('LazarWifi', 'MimmoBerardi')
while not sta_if.isconnected():
  print(".", end="")
  time.sleep(0.1)
print(" Connected!")

print("Connecting to MQTT server... ", end="")
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER)
client.set_callback(subCallback)
client.connect()
client.subscribe(MQTT_EROGAZIONE)

#server to retrieve the current time
ntptime.host = "ntp1.inrim.it"

print("Connected!")

#button inizialization
btn1=Pin(13,Pin.IN,Pin.PULL_UP)

# buzzer inizialization
buz = BUZZER(14)
buz.play(buzzer_G21.mute,500,512)

#display inizialization
display = display_proj(22,21)

#engine inizialization
engine = engine(23,50)

#photoresistor inizialization
photoresistor = LDR(34)

#led inizialization
led_emergency = Pin(4,Pin.OUT)
led_night = Pin(25,Pin.OUT)

#emergency state inizialization
emergency = emergency_state()

#infrared sensor inizialization
infrared_sens = Pin(2,Pin.IN,Pin.PULL_UP)
print(infrared_sens.value())
if infrared_sens.value() == 1:
    emergency.state_em = True

#management button pression interruption
btn1.irq(handler=engine.opening,trigger=Pin.IRQ_FALLING)

#management presence of objects in front of the infrared sensor interruption 
infrared_sens.irq(handler=emergency.change_state_em,trigger=Pin.IRQ_FALLING)

#EXECUSION ROUTINE
while True:

    #new message check
    client.check_msg()
    
   
    #night management
    if photoresistor.value() < 20:
        led_night.on()
        buz.night_mode(True)
    else:
        led_night.off()
        buz.night_mode(False)

    #last emanation printing on display
    display.write("Ultima ",10,0)
    display.write("erogazione: ",10,10)
    display.write(date,10,20)
    display.write(hour,10,30)

    #emanation management
    if (engine.opened and not emergency.state_em) or (remote_emanation and not emergency.state_em):
        display.clear()
        engine.dispense(buz,display,opening_angle,opening_time)
        time.sleep(2)
        display.clear()
        engine.opened=False
        remote_emanation = False
        ntptime.settime()
        date_hour = str(time.localtime()).replace("(",",").split(",")
        date = date_hour[3] + "/" + date_hour[2] + "/" + date_hour[1]
        hour = " " + str(int(date_hour[4])+2) + ":" + date_hour[5]
            
    #emergency state management
    while emergency.state_em:
        display.clear()
        em_message = "Riempire il contenitore"
        client.publish(MQTT_EMERGENCY,em_message)
        while infrared_sens.value() == 1:
            emergency.management(display,led_emergency,buz,engine)
        led_emergency.off()
        emergency.state_em = False
        noem_message = ""
        client.publish(MQTT_EMERGENCY,noem_message)
        
   
        
  