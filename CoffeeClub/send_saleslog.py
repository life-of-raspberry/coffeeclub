#!/usr/bin/python
import time
from send_email import send_email
from datetime import datetime as dt

now_time = dt.now()
year = str(now_time.year)
month = str(now_time.month)
month = month.rjust(2,'0')
day = str(now_time.day)
day = day.rjust(2,'0')
file_ending = year+month
subject = "Buchungen bis und mit %s.%s.%s" % (day,month,year)
file_path = "logfiles/saleslog_%s%s.log" % (year,month)

time.sleep(120)

send_email(subject,file_path)

