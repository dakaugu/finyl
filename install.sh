#!/bin/bash

echo "Installing finyl!"

echo "Adding environment variables"
export FINYL_ENV=FINYL_PI

echo "installing necessary software"
essential_pckgs=(
  build-essential
  zlib1g-dev
  libncurses5-dev
  libgdbm-dev
  libnss3-dev
  libssl-dev
  libreadline-dev
  libffi-dev
  libsqlite3-dev
  wget
  libbz2-dev
  python3.11
  python3-dev
  libpython3.11-dev
  python3-pip
  raspi-config
  i2c-tools
  libi2c-dev
  python3-smbus
)
sudo apt install -y "${essential_pckgs[@]}"


sudo ln -s /usr/bin/python3 /usr/bin/python

echo "Installing necessary audio dependencies"
sudo apt install -y 
    ffmpeg 
    python3-pyaudio 
    libasound2-dev 
    portaudio19-dev 
    libportaudio2 
    libportaudiocpp0 
    alsa-utils

echo "Installing Poetry"
curl -sSL https://install.python-poetry.org | python3 -
export PATH="/home/ubuntu/.local/bin:$PATH"
poetry --version

echo "Add permission to file"
sudo chmod 777 /var/

echo "Install Python dependencies"
poetry install

echo "Before running finyl, make sure to enable i2c in raspi config and disable HDMI audio"

echo "Once completed, run: poetry run python finyl/main.py in finyl directory"