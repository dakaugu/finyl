FROM ubuntu:22.04

WORKDIR /finyl
ARG DEBIAN_FRONTEND=noninteractive

ENV FINYL_ENV TEST

COPY . .

# remove sudo occurence
RUN sed -i 's/sudo//g' install.sh

