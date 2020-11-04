#!/bin/bash


echo "Pulling Updates from Git..."
git pull

echo "Checking Configuration..."
# Link Stations to mpd playlists
if ! [ -L /var/lib/mpd/playlists ] ; then
  rmdir /var/lib/mpd/playlists
  ln -s $(pwd)/stations /var/lib/mpd/playlists
fi

# Link mpd.conf
if ! [ -L /etc/mpd.conf ] ; then
  rm -f /etc/mpd.conf
  ln -s $(pwd)/mpd.conf /etc/mpd.conf
fi

# Link piradio service
if ! [ -L /etc/systemd/system/piradio.service ] ; then
  rm -f /etc/systemd/system/piradio.service
  ln -s $(pwd)/piradio.service /etc/systemd/system/piradio.service
fi

#echo "Restarting Services..."
#systemctl daemon-reload
#systemctl restart mpd

exit 0
