FROM debian:12

ARG DEBIAN_FRONTEND=noninteractive

ENV FINYL_INSTALL PI
ENV FINYL_ENV FINYL_PI

COPY dist/finyl-0.1.0.tar.gz bin/
COPY install.sh .

# remove sudo occurence
RUN sed -i 's/sudo//g' install.sh
