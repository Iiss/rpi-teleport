#!/bin/sh
# install.sh
# deploy teleport application to current directory & install it's dependencies

# step 0:
#sudo apt-get update

# step 1: install pip & virtualenv
sudo apt-get -y install python-pip
sudo pip install virtualenv

# step 2: install python-dev
sudo apt-get -y install python-dev

# step 3: install MOC player
sudo apt-get -y install moc

# step 5: complete installation
virtualenv venv
sudo venv/bin/pip install -r requirements.txt
mkdir ~/logs
touch ~/logs/cronlog
echo 'for setup usb soundcard enter "sudo nano /etc/modprobe.d/alsa-base.conf"'
echo '"alsamixer" to setup volume'
echo '"sudo alsactl store" to save sound settings'
echo 'in /etc/rc.local add "sh launcher.sh >/home/pi/logs/cronlog 2>&1" for correct autorun'

