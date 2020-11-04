#!/usr/bin/env python3
import time
import RPi.GPIO as GPIO
import musicpd
from sys import exit

# local classes
from lcd import LCD
from mpc import MPC

BT_RIGHT = 16
BT_LEFT  = 21
BT_ENTER = 20

def main():
    GPIO.setmode(GPIO.BCM)
    mpc = MPC()
    lcd = LCD()
    
    try:
      GPIO.setup(BT_RIGHT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
      GPIO.setup(BT_LEFT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
      GPIO.setup(BT_ENTER, GPIO.IN, pull_up_down=GPIO.PUD_UP)

      GPIO.add_event_detect(BT_RIGHT, GPIO.FALLING, callback=mpc.next, bouncetime=300)
      GPIO.add_event_detect(BT_LEFT, GPIO.FALLING, callback=mpc.prev, bouncetime=300)
      GPIO.add_event_detect(BT_ENTER, GPIO.FALLING, callback=mpc.start_stop, bouncetime=300)
    except Exception as e:
      print(e)
      GPIO.cleanup()
      exit(1)


    if not mpc.is_playing():
      mpc.next()

    while True:
        # update display 
        try: 
            if mpc.is_playing():
              lcd.println("-- Playing --", LCD.LINE_1, 2) 
            else:
              lcd.println("[ STOPPED ]", LCD.LINE_1, 2)

            lcd.println("%s" % (str(mpc.get_station())), LCD.LINE_2) 
            lcd.println("--- Song ---", LCD.LINE_3, 2) 
            lcd.println("%s" % (str(mpc.get_title())), LCD.LINE_4) 
            #lcd.println("%s" % ("PiRadio v0.1"), LCD.LINE_4) 
            time.sleep(3)
        except Exception as e:
            print(e)
            lcd.println("Goodbye!", LCD.LINE_1)
            GPIO.cleanup()

main()
