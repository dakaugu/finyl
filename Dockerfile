FROM debian:12

WORKDIR /finyl
ARG DEBIAN_FRONTEND=noninteractive

ENV FINYL_ENV TEST

COPY . .

RUN sed -i 's/sudo//g' install.sh

