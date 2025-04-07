FROM debian:12-slim

RUN apt update -y && \
    apt install -y \
        bluez

COPY ./svc/init.sh /root/init.sh
COPY bluetooth.conf /etc/bluetooth/main.conf
