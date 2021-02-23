#!/bin/sh

sudo python3 led_forcekill.py
sudo pkill -9 python
sudo pkill -9 vlc
#sudo /etc/init.d/rabbitmq-server stop


