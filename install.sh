#!/bin/sh
# install.sh
# deploy teleport application to current directory & install it's dependencies

# step 0:
sudo apt-get update

# step 1: install pip & virtualenv
sudo apt-get install python-pip
sudo pip install virtualenv

# step 2: install python-dev
sudo apt-get install python-dev

# step 3: install MOC player
sudo apt-get install moc

# step 4: clone repository
git clone https://github.com/Iiss/rpi-teleport.git

# step 5: complete installation
cd rpi-teleport
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

