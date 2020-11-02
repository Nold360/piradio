#!/usr/bin/env python3
from time import sleep
import musicpd
import sys

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

mpc = PiRadio()
print(mpc.is_playing())
print(mpc.list())

print(mpc.get_title())
print(mpc.get_station())
mpc.next()
mpc.next()

mpc.next()
sleep(3)
print(mpc.is_playing())
print(mpc.get_title())
print(mpc.get_station())

mpc.next(True)
sleep(3)
print(mpc.is_playing())
print(mpc.get_title())
print(mpc.get_station())
