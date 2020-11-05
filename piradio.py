#!/usr/bin/env python3
import time
import RPi.GPIO as GPIO
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

    base = 0
    while True:
        # update display 
        try:
            if mpc.is_playing():
              lcd.println("-- Playing --", LCD.LINE_1, 2) 
            else:
              lcd.println("[ STOPPED ]", LCD.LINE_1, 2)

            lcd.println("%s" % (str(mpc.get_station())), LCD.LINE_2) 
            lcd.println("--- Song ---", LCD.LINE_3, 2) 

            # Scroll Song Title if too long
            count = 0
            song = str(mpc.get_title())
            if song and len(song) > 20: 
                song = song + " | "
                if base >= len(song):
                    base = 0
                buffer=[""]*20
                for i in range(base, base+20):
                    if i >= len(song):
                        i = i - len(song)
                    try:
                      buffer[count] = song[i]
                    except:
                      pass
                    count+=1

                lcd.println("%s" % (str(''.join(buffer))), LCD.LINE_4) 
                base+=1
            else:
                lcd.println(song, LCD.LINE_4) 


            time.sleep(1)
        except Exception as e:
            print(e)
            lcd.println("Goodbye!", LCD.LINE_1, 2)
            GPIO.cleanup()

main()
