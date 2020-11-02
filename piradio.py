#!/usr/bin/env python3
import time
import RPi.GPIO as GPIO
import musicpd
import keyboard
#import sys

class Buttons:
    # Raspberry GPIO Pins
    BT_RIGHT = 16
    BT_LEFT  = 20
    BT_ENTER = 21

class PiRadio:
    client = None
    current_playlist = None

    def __init__(self):
       self.client = musicpd.MPDClient()
       self.connect()

    def connect(self):
       return self.client.connect()

    def update(self):
       return self.client.update()

    def next(self, reverse=False):
       # get all playlist names
       pl = self.list()

       if not self.current_playlist:
           self.load(pl[0])
           return self.play()

       if not reverse:
           num = pl.index(self.current_playlist)+1
       else:
           num = pl.index(self.current_playlist)-1
          
       if num > len(pl) or num < 0:
           return self.load(pl[0])
       else:
           return self.load(pl[num])


    def status(self):
       return self.client.status()

    def state(self):
       return self.status()['state']

    def is_playing(self):
        if not 'play' in self.state():
           return False
        return True

    def play(self):
        return self.client.play()

    def stop(self):
        return self.client.stop()

    def load(self, playlist):
        self.client.clear()
        self.client.load(playlist)
        print("Loading: " + playlist)
        self.current_playlist = playlist
        return self.play()

    def list(self):
        return [d['playlist'] for d in self.client.listplaylists()]

    def get_title(self):
        try:
            return self.client.currentsong()['title']
        except:
            return None

    def get_station(self):
        try:
            return self.client.currentsong()['name']
        except:
            return None

class LCD:
    # Define GPIO to LCD mapping
    LCD_RS = 7
    LCD_E  = 8
    LCD_D4 = 25
    LCD_D5 = 24
    LCD_D6 = 23
    LCD_D7 = 18

    # Define some device constants
    LCD_WIDTH = 20    # Maximum characters per line
    LCD_CHR = True
    LCD_CMD = False

    LINE_1 = 0x80 # LCD RAM address for the 1st line
    LINE_2 = 0xC0 # LCD RAM address for the 2nd line
    LINE_3 = 0x94 # LCD RAM address for the 3rd line
    LINE_4 = 0xD4 # LCD RAM address for the 4th line

    # Timing constants
    E_PULSE = 0.0005
    E_DELAY = 0.0005

    def __init__(self):
      GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
      GPIO.setup(self.LCD_E, GPIO.OUT)  # E
      GPIO.setup(self.LCD_RS, GPIO.OUT) # RS
      GPIO.setup(self.LCD_D4, GPIO.OUT) # DB4
      GPIO.setup(self.LCD_D5, GPIO.OUT) # DB5
      GPIO.setup(self.LCD_D6, GPIO.OUT) # DB6
      GPIO.setup(self.LCD_D7, GPIO.OUT) # DB7

      # Initialise display
      self.lcd_init()

    def lcd_init(self):
      # Initialise display
      self.lcd_byte(0x33,self.LCD_CMD) # 110011 Initialise
      self.lcd_byte(0x32,self.LCD_CMD) # 110010 Initialise
      self.lcd_byte(0x06,self.LCD_CMD) # 000110 Cursor move direction
      self.lcd_byte(0x0C,self.LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
      self.lcd_byte(0x28,self.LCD_CMD) # 101000 Data length, number of lines, font size
      self.lcd_byte(0x01,self.LCD_CMD) # 000001 Clear display
      time.sleep(self.E_DELAY)

    def lcd_byte(self, bits, mode):
      # Send byte to data pins
      # bits = data
      # mode = True  for character
      #        False for command

      GPIO.output(self.LCD_RS, mode) # RS

      # High bits
      GPIO.output(self.LCD_D4, False)
      GPIO.output(self.LCD_D5, False)
      GPIO.output(self.LCD_D6, False)
      GPIO.output(self.LCD_D7, False)
      if bits&0x10==0x10:
    	GPIO.output(self.LCD_D4, True)
      if bits&0x20==0x20:
    	GPIO.output(self.LCD_D5, True)
      if bits&0x40==0x40:
    	GPIO.output(self.LCD_D6, True)
      if bits&0x80==0x80:
    	GPIO.output(self.LCD_D7, True)

      # Toggle 'Enable' pin
      self.lcd_toggle_enable()

      # Low bits
      GPIO.output(self.LCD_D4, False)
      GPIO.output(self.LCD_D5, False)
      GPIO.output(self.LCD_D6, False)
      GPIO.output(self.LCD_D7, False)
      if bits&0x01==0x01:
    	GPIO.output(self.LCD_D4, True)
      if bits&0x02==0x02:
    	GPIO.output(self.LCD_D5, True)
      if bits&0x04==0x04:
    	GPIO.output(self.LCD_D6, True)
      if bits&0x08==0x08:
    	GPIO.output(self.LCD_D7, True)

      # Toggle 'Enable' pin
      self.lcd_toggle_enable()

    def lcd_toggle_enable(self):
      # Toggle enable
      time.sleep(self.E_DELAY)
      GPIO.output(self.LCD_E, True)
      time.sleep(self.E_PULSE)
      GPIO.output(self.LCD_E, False)
      time.sleep(self.E_DELAY)

    # Send string to display
    # style=1 Left justified
    # style=2 Centred
    # style=3 Right justified
    def println(self, message, line, style=1):
      if style==1:
    	message = message.ljust(self.LCD_WIDTH," ")
      elif style==2:
    	message = message.center(self.LCD_WIDTH," ")
      elif style==3:
    	message = message.rjust(self.LCD_WIDTH," ")

      self.lcd_byte(line, self.LCD_CMD)

      for i in range(self.LCD_WIDTH):
    	self.lcd_byte(ord(message[i]),self.LCD_CHR)


mpc = PiRadio()
def on_press(key):
  if key == Key.left:
    mpc.next(False)
  elif key == Key.right:
    mpc.next()
  elif key == Key.enter:
    print('enter')
  elif key == Key.esc:
    exit(0)

def main():
    pl_num = 0

    # Keyboard Listener
    listener = Listener(on_press=on_press)
    listener.start()

    lcd = LCD()

    if not mpc.is_playing():
      mpc.next()

    while True:
      try:
         # update display 
         lcd.println("[%s] Station:" % (str(mpc.state())), LCD.LINE_1) 
         lcd.println("%s" % (str(mpc.get_station())), LCD.LINE_1) 
         lcd.println("%s" % (str(mpc.get_title())), LCD.LINE_1) 
         lcd.println("%s" % ("PiRadio v0.1"), LCD.LINE_1) 
         pass
         time.sleep(3)
      except KeyboardInterrupt:
         pass
      finally:
    	lcd.lcd_byte(0x01, LCD.LCD_CMD)
    	lcd.println("Goodbye!",LCD.LINE_1,2)
    	GPIO.cleanup()

