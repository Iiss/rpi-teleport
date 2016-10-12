#!/bin/sh
# install.sh
# deploy teleport application to current directory & install it's dependencies

# step 0:
sudo apt-get update

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
touch ~/logs/cronlog

