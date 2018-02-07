import RPi.GPIO as GPIO
import MFRC522
import logging

class Rfid_reader:
    def __init__(self):
        self.MIFAREReader = MFRC522.MFRC522()

    def scan_card(self):
        return_val = 0

         # Scan for cards    
        (status,TagType) = self.MIFAREReader.MFRC522_Request(self.MIFAREReader.PICC_REQIDL)

        # If a card is found
        if status == self.MIFAREReader.MI_OK:
            logging.info( "Card detected")

        # Get the UID of the card
        (status,uid) = self.MIFAREReader.MFRC522_Anticoll()

        # If we have the UID, continue
        if status == self.MIFAREReader.MI_OK:
            # Print UID
            logging.info("Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))
            return_val =  uid[0:4]

        return return_val
