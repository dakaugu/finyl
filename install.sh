#!/bin/bash
_user="$(id -u -n)"

echo "Building finyl!"

echo "Adding environment variables"
export FINYL_ENV=FINYL_PI

echo "installing necessary software"
sudo apt update
sudo apt install -y nala
sudo nala install -y \
    build-essential \
    zlib1g-dev \
    libncurses5-dev \
    libgdbm-dev  \
    libnss3-dev \
    libssl-dev \
    libreadline-dev \
    libffi-dev \
    libsqlite3-dev \
    wget \
    libbz2-dev \
    python3.11 \
    python3-dev \
    libpython3.11-dev \
    python3-pip \
    i2c-tools \
    libi2c-dev \
    python3-smbus \
    curl \
    nmcli

sudo ln -s /usr/bin/python3 /usr/bin/python

echo "Installing raspi-config"
sudo apt install raspi-config

echo "Installing necessary audio dependencies"
sudo nala install -y \
    ffmpeg \
    python3-pyaudio \
    libasound2-dev \
    portaudio19-dev \
    libportaudio2 \
    libportaudiocpp0 \
    alsa-utils \
    pulseaudio

echo "Configure raspi-config"
sudo raspi-config

echo "Installing Poetry"
curl -sSL https://install.python-poetry.org | python3 -
export PATH="/home/${_user}/.local/bin:$PATH"
export PATH="/home/ubuntu/.local/bin:$PATH"
export PATH="${_user}/.local/bin:$PATH"
poetry --version

echo "Add permission to finyl files"
sudo chmod 777 /var/

echo "Install Python dependencies"
poetry install --only main

echo "Before running finyl, make sure to enable i2c in raspi config and disable HDMI audio"

echo "Once completed, run: poetry run python finyl/main.py in finyl directory"