#!/usr/bin/python
import os, sys
import logging
import time
import json
import struct
from datetime import datetime as dt
from Lcd_display import Lcd_display
from Rfid_reader import Rfid_reader

try:
    #setup logging
    formatter = logging.Formatter('%(asctime)s; %(message)s')
    year = str(dt.now().year)
    month = str(dt.now().month)
    time_str = year + month.rjust(2,'0')
    print time_str
    h1 = logging.FileHandler('logfiles/eventlog_%s.log' % time_str)
    h1.setFormatter (formatter)
    h2 = logging.FileHandler('logfiles/saleslog_%s.log' % time_str)
    h2.setFormatter (formatter)
    event_log = logging.getLogger('event')
    event_log.addHandler(h1)
    event_log.setLevel(logging.INFO)
    sales_log = logging.getLogger('sales')
    sales_log.addHandler(h2)
    sales_log.setLevel(logging.INFO)

    event_log.info('main.py started')

    RFID = Rfid_reader()
    LCD = Lcd_display()

    file = open('customer_list','r')
    try:
        customer_dict = json.loads(file.read())
    except:
        customer_dict = {}

    print customer_dict

    #save pid to file for cron process
    pid = str(os.getpid())
    pidfile = "/home/pi/CoffeeClub/main.pid"
    open(pidfile,'w').write(pid)

    while True:

        fin = open('stop.txt','r')
        stop = int(fin.read())
        if stop:
            raise Exception

        year = str(dt.now().year)
        month = str(dt.now().month)
        new_time_str = year + month.rjust(2,'0')
        if new_time_str != time_str:
            time_str = new_time_str
            h1 = logging.FileHandler('logfiles/eventlog_%s.log' % time_str)
            h1.setFormatter (formatter)
            h2 = logging.FileHandler('logfiles/saleslog_%s.log' % time_str)
            h2.setFormatter (formatter)
            event_log.handlers = []
            event_log.addHandler(h1)
            sales_log.handlers = []
            sales_log.addHandler(h2)
        LCD.lcd_string('CoffeeClub CKW',LCD.LCD_LINE_1) 
        LCD.lcd_string('Bereit!',LCD.LCD_LINE_2)
        card_id_raw = RFID.scan_card()

        if card_id_raw != 0:
            event_log.info('Card detected')
            #print card_id_raw[0],card_id_raw[1], card_id_raw[2], card_id_raw[3]
            #print card_id_raw
            c = struct.unpack('I',bytearray(card_id_raw)) # Calculate value of four bytes
            card_id = c[0]
            card_id = str(card_id)
            #print card_id

            if card_id in customer_dict:
               # log event
               event_log.info('Recognized customer %s %s. Kdnr: %d UID: %s' % (customer_dict[card_id]['Vorname'],customer_dict[card_id]['Nachname'],customer_dict[card_id]['Kdnr'],card_id))

            else:
               # add customer
               new_kdnr = 1001 + len(customer_dict)
               new_customer = {'Kdnr':new_kdnr,'Vorname':'Barista','Nachname':'unbekannt'}
               customer_dict[card_id] = new_customer

               with open('customer_list','w') as fout:
                   json.dump(customer_dict, fout,indent=True)
               backup_file = "logfiles/customer_list_%s" % new_time_str
               with open(backup_file,'w') as fout:
                   json.dump(customer_dict, fout,indent=True)

               event_log.info('Created customer %s %s. Kdnr: %d UID: %s' % (customer_dict[card_id]['Vorname'],customer_dict[card_id]['Nachname'],customer_dict[card_id]['Kdnr'],card_id))

            # End sale with log and message
            sales_log.info(str(customer_dict[card_id]['Kdnr'])+'; '+customer_dict[card_id]['Vorname']+'; '+customer_dict[card_id]['Nachname']+'; '+card_id)
            str1 = ('Hallo %s' % customer_dict[card_id]['Vorname'])
            LCD.lcd_string(str1,LCD.LCD_LINE_1)
            LCD.lcd_string('Kdnr:'+str(customer_dict[card_id]['Kdnr']),LCD.LCD_LINE_2)
            time.sleep(2)
            LCD.lcd_string('Geniesse deinen',LCD.LCD_LINE_1)
            LCD.lcd_string('Kaffee',LCD.LCD_LINE_2)
            time.sleep(1)
        time.sleep(1)
finally:
    LCD.lcd_clear()
    event_log.info('Process stopped')
