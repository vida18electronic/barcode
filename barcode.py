#!/usr/bin/python3
import lcddriver
import time
import sys
import requests
import json
import os,subprocess
import re
import atexit
from time import sleep

from gpiozero import LED

display = lcddriver.lcd()

green = LED(16)
red   = LED(20)
blue  = LED(21)

URL="http://tfsnew.vida18.com:8083/api/routes/barcode"

def barcode_reader():
    """Barcode code obtained from 'brechmos' 
    https://www.raspberrypi.org/forums/viewtopic.php?f=45&t=55100"""
    hid = {4: 'a', 5: 'b', 6: 'c', 7: 'd', 8: 'e', 9: 'f', 10: 'g', 11: 'h', 12: 'i', 13: 'j', 14: 'k', 15: 'l', 16: 'm',
           17: 'n', 18: 'o', 19: 'p', 20: 'q', 21: 'r', 22: 's', 23: 't', 24: 'u', 25: 'v', 26: 'w', 27: 'x', 28: 'y',
           29: 'z', 30: '1', 31: '2', 32: '3', 33: '4', 34: '5', 35: '6', 36: '7', 37: '8', 38: '9', 39: '0', 44: ' ',
           45: '-', 46: '=', 47: '[', 48: ']', 49: '\\', 51: ';', 52: '\'', 53: '~', 54: ',', 55: '.', 56: '/'}

    hid2 = {4: 'A', 5: 'B', 6: 'C', 7: 'D', 8: 'E', 9: 'F', 10: 'G', 11: 'H', 12: 'I', 13: 'J', 14: 'K', 15: 'L', 16: 'M',
            17: 'N', 18: 'O', 19: 'P', 20: 'Q', 21: 'R', 22: 'S', 23: 'T', 24: 'U', 25: 'V', 26: 'W', 27: 'X', 28: 'Y',
            29: 'Z', 30: '!', 31: '@', 32: '#', 33: '$', 34: '%', 35: '^', 36: '&', 37: '*', 38: '(', 39: ')', 44: ' ',
            45: '_', 46: '+', 47: '{', 48: '}', 49: '|', 51: ':', 52: '"', 53: '~', 54: '<', 55: '>', 56: '?'}

    fp = open('/dev/hidraw0', 'rb')

    ss = ""
    shift = False

    done = False

    while not done:

        ## Get the character from the HID
        buffer =fp.read(8)
        buffer=buffer.decode("utf-8") 
        #print([x for x in iterbytes(b(buffer))])
        for c in buffer:
            if ord(c) > 0:

                ##  40 is carriage return which signifies
                ##  we are done looking for characters
                if int(ord(c)) == 40:
                    done = True
                    break;

                ##  If we are shifted then we have to
                ##  use the hid2 characters.
                if shift:

                    ## If it is a '2' then it is the shift key
                    if int(ord(c)) == 2:
                        shift = True

                    ## if not a 2 then lookup the mapping
                    else:
                        ss += hid2[int(ord(c))]
                        shift = False

                ##  If we are not shifted then use
                ##  the hid characters

                else:

                    ## If it is a '2' then it is the shift key
                    if int(ord(c)) == 2:
                        shift = True

                    ## if not a 2 then lookup the mapping
                    else:
                        ss += hid[int(ord(c))]
    return ss

def no_barcode():
  display.lcd_clear()
  display.lcd_display_string("     RESET!      ",1)
  display.lcd_display_string("NO BARCODEREADER",2)

def scan_m():
  display.lcd_clear()
  display.lcd_display_string(" Welcome Vida18 ",1)
  display.lcd_display_string("  PLEASE SCAN!  ",2)

def error_m():
  display.lcd_clear()
  display.lcd_display_string("ERROR ERROR",1)
  display.lcd_display_string("CALL SUPPORT",2)

def webserver(barcode):
    payload={'input': barcode}
    r=requests.get(URL,params=payload)
    #print(r.url)
    #print(r.status_code)
    if r.status_code<0:
        x={"message":"ERRORWEBSER","code":r.status_code}
        return json.loads(json.dumps(x))
    else:
        return json.loads(json.dumps(r.json()))

def scanned(rta):
   display.lcd_clear()
   m="CODE:"+ str(rta["code"])
   display.lcd_display_string(m,1)
   display.lcd_display_string(rta["message"],2)



if __name__ == '__main__':
    try:
      green.off()
      red.off()
      blue.off()
      scan_m()
      while True:
        try:
          while True:
             barcode=barcode_reader()
             rta=webserver(barcode)
             scanned(rta)
             code=rta["code"]
             if code==1:
                 green.on()
                 red.off()
                 blue.off()
             elif code==2:
                 green.off()
                 red.on()
                 blue.off()
             elif code==3:
                 green.off()
                 red.off()
                 blue.on()
             else:
                 green.off()
                 red.off()
                 blue.off()
        except OSError as e:
             no_barcode()
    except KeyboardInterrupt:
         error_m()
         pass
