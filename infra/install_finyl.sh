#!/bin/bash

echo "Building finyl!"

echo "Adding environment variables"
export FINYL_ENV=FINYL_PI

echo "installing necessary software"
sudo apt update
sudo apt install -y nala

sudo nala install -y \
    python3-pip \
    i2c-tools \
    libi2c-dev \
    ffmpeg \
    python3-pyaudio \
    python3-dev \
    libasound2-dev

echo "Please configure raspi-config, and enable i2c and audio source"

echo "Installing finyl!"
pip install finyl-0.2.1.tar.gz --break-system-packages

echo "Add permission to finyl files"
sudo chmod 777 /var/