#!/usr/bin/env python3
# Handles MPD Communication
import musicpd

class MPC:
    client = None
    current_playlist = None

    def __init__(self):
       self.client = musicpd.MPDClient()
       self.connect()

    def connect(self):
       return self.client.connect()

    def update(self):
       return self.client.update()

    def next(self, channel=0, reverse=False):
       # get all playlist names
       try: 
           pl = self.list()
           if not pl:
              return False
       except:
           return False

       if not self.current_playlist:
           self.load(pl[0])
           return self.play()  

       if not reverse:
           num = pl.index(self.current_playlist)+1
       else:
           num = pl.index(self.current_playlist)-1
          
       if num >= len(pl):
           return self.load(pl[0])
       elif num < 0:
           return self.load(pl[len(pl)-1])
       else:
           return self.load(pl[num])

    def prev(self, channel=0):
         return self.next(reverse=True)

    def status(self):
       return self.client.status()

    def state(self):
       try:
         return self.status()['state']
       except:
         return None

    def is_playing(self):
        try:
            if 'play' in self.state():
               return True
        except: pass   
        return False
    
    def start_stop(self, channel=0):
        if self.is_playing():
            print("Stopping")
            return self.stop()
        else:
            print("Starting")
            return self.play()

    def play(self):
        return self.client.play()

    def stop(self):
        return self.client.stop()

    def load(self, playlist):
        try: 
            self.client.clear()
            self.client.load(playlist)
            print("Loading: " + playlist)
            self.current_playlist = playlist
            return self.play()
        except:
            return False

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
