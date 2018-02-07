#!/bin/sh
date
ps up `cat /home/pi/CoffeeClub/main.pid ` >/dev/null && echo "Python Script Running" || (echo "Script Restarted" && python /home/pi/CoffeeClub/main.py)
