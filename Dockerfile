FROM ubuntu:22.04

WORKDIR /finyl
ARG DEBIAN_FRONTEND=noninteractive

ENV FINYL_ENV TEST

#install python
RUN apt update
RUN apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev  \
    libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev
RUN apt install -y python3.11 python3-pip
RUN ln -s /usr/bin/python3 /usr/bin/python

# install audio dependencies
RUN apt install -y ffmpeg python3-pyaudio python3-dev libpython3.11-dev \
    libasound2-dev portaudio19-dev libportaudio2 libportaudiocpp0 alsa-utils

COPY . .

# curl install instead
RUN pip install poetry

# install deps
RUN poetry install

CMD poetry run python finyl/main.py