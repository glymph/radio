#!/usr/bin/python
# Radio script for Raspberry Pi with Adafruit 16x2 LCD
import time
import Adafruit_CharLCD as LCD
from subprocess import *

 
#  
 
def run_cmd(cmd):
        p = Popen(cmd, shell=True, stdout=PIPE)
        output = p.communicate()[0]
        return output
 
# Initialize the LCD using the pins
lcd = LCD.Adafruit_CharLCDPlate()

# create some custom characters
# pause symbol
lcd.create_char(1, [8, 12, 14, 15, 14, 12, 8, 0])
playsymbol = "\x01"
# play symbol
lcd.create_char(2, [27,27,27,27,27,27,27,0])
pausesymbol = "\x02"

# set backlight colour to cyan
lcd.set_color(0.0, 1.0, 1.0)

lcd.clear()

# Make list of button value, text, and backlight color.
buttons = ( (LCD.SELECT, 'Select', (1,1,1)),
            (LCD.LEFT,   'Left'  , (1,0,0)),
            (LCD.UP,     'Up'    , (0,0,1)),
            (LCD.DOWN,   'Down'  , (0,1,0)),
            (LCD.RIGHT,  'Right' , (1,0,1)) )

radio1url = run_cmd("curl -s  'http://www.radiofeeds.co.uk/bbcradio1.pls' | grep File1 | cut -d'=' -f2 | tr -d '\n'")
radio2url = run_cmd("curl -s  'http://www.radiofeeds.co.uk/bbcradio2.pls' | grep File1 | cut -d'=' -f2 | tr -d '\n'")

stations = ( ('0', 'Radio 1', radio1url),
             ('1', 'Radio 2', radio2url),
             ('2', 'Magic Soul', 'http://icy-e-bz-04-cr.sharp-stream.com:8000/magicsoul.mp3'),
             ('3', 'Jazz FM', 'http://adsi-e-02-boh.sharp-stream.com:8000/jazzfmmobile.mp3'),
             ('4', 'Absolute 80s', 'http://icy-e-bab-04-cr.sharp-stream.com:8000/absolute80s.mp3'),
             ('5', 'Jungletrain', 'http://stream2.jungletrain.net:8000/'),
             ('6', 'Barricade radio', 'http://uk2.internet-radio.com:8066/') )

currentstation = 0
cmd = "mpc clear && mpc add '" + stations [currentstation] [2] + "' && mpc play"
run_cmd(cmd)
state="playing"
printstate = playsymbol
info1 = stations [currentstation] [1]
cmd = "amixer sget PCM | grep 'Left: Playback' | cut -d' ' -f7"
info2 = printstate + " " + run_cmd(cmd)
info=info1 + "\n" + info2
lcd.message(info)

while True:
    # Loop through each button and check if it is pressed.
    for button in buttons:
        if lcd.is_pressed(button[0]):
            # Button is pressed, change the message and backlight.
            lcd.clear()
            if button[1]=='Up':
                run_cmd("amixer sset PCM 10%+")
            if button[1]=='Down':
                run_cmd("amixer sset PCM 10%-")
            if button[1]=='Left':
                currentstation -= 1
                currentstation %= 7
                cmd = "mpc clear && mpc add '" + stations [currentstation] [2] + "' "
                run_cmd(cmd)
                if state == "playing":
                    run_cmd("mpc play")
            if button[1]=='Right':
                currentstation += 1
                currentstation %= 7
                cmd = "mpc clear && mpc add '" + stations [currentstation] [2] + "' "
                run_cmd(cmd)
                if state == "playing":
                    run_cmd("mpc play")
            if button[1]=='Select':
                if state=="playing":
                    run_cmd('mpc stop')
                    state = "stopped"
                    printstate = pausesymbol
                else:
                    run_cmd('mpc play')
                    state = "playing"
                    printstate = playsymbol
            time.sleep(1)
            info1 = stations [currentstation] [1] 
            cmd = "amixer sget PCM | grep 'Left: Playback' | cut -d' ' -f7"
            info2 = printstate + " " + run_cmd(cmd)
            info=info1 + "\n" + info2
            lcd.message(info)
