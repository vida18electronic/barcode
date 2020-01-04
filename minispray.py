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
import screens
import threading
from gpiozero import LED
import multiprocessing
import queue
import services




#VARIABLES
block='  '
stop=' '
id='  '
display = lcddriver.lcd()
#SIZE               2               6              4           4                  11                      7
info_buncher={"BUNCHER_ID":"XX","TUB_ID":"XXXXXX","TxR":"XXXX","GR":"XXXX","VARIETY_ID":"XXXXXXXXXXX","BUNCH_ID":"XXXXXXX","COMPOSITION_ID":"xxxxx","BLOCK_ID":"XX"}
info_device={"MAC_ADDRESS":"xxxxxxx","IP_ADDRESS":"xxxxx","BLOCK_ID":"xxxxx","STOP_ID":"xxx"}
info_sorter={"SORTER_ID":"xx"}

green = LED(16)
red   = LED(20)
blue  = LED(21)

URL="http://tfsnew.vida18.com:8083/api/routes/barcode"

def barcode_reader(out_queue):
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
    out_queue.put(ss)

def initialscreen(display,bk):
       display.lcd_clear()
       time.sleep(0.2)
       while True:
           screens.scanbloque(bk,display)
           time.sleep(0.3)
           screens.twinkle([3,4],display)


def encuentra(cadena,carac):
       indice=0
       while indice < len(cadena):
            if cadena[indice] == carac:
                 return indice
            indice += 1
       return -1

def getbloque(scan):
     scan=str(scan).upper()
     try:
       if(scan[:2] == 'BK'):
            index=encuentra(scan,'.')
            if index >= 0:
                global block
                global stop
                global info_buncher
                global info_device
                block=scan[2:index]
                if int(block) <= 9:
                     block = '0'+str(block)
                    # print(block)
                stop=str(scan[index+1:])
                # print(stop)
                info_buncher["BLOCK_ID"]=block
                info_device["STOP_ID"]=stop
                info_device["BLOCK_ID"]=block
                return True
            else:
              return  False
       else:
           return False
     except:
        return False

def screendefault(display):
        global info_buncher
        global block
        display.lcd_clear()
        time.sleep(0.2)
        while True:
           screens.buncher(display,info_buncher)
           time.sleep(0.3)
           screens.twinkle([1,2,3,4],display)


def buncherscreen(display):
      global info_buncher
      global block
      display.lcd_clear()
      time.sleep(0.2)
      screens.buncher(display,info_buncher)


def scancarnet(cadena):
        global id
        global info_buncher
        cadena=str(cadena).upper()
        try:
             if(cadena[0]== 'B'):
                 id=str(cadena[1:])
                 if len(id)==1:
                    id='0'+id
                 info_buncher["BUNCHER_ID"]=str(id)
                 return True
             elif(cadena[0] == 'C'):
                 id=str(cadena[1:]) 
                 if len(id)==1:
                     id='0'+id
                 info_sorter["SORTER_ID"]=str(id)
                 return True
             elif cadena[0] == 'R':
                  return devramo(cadena[1:])
             else:
                return False
        except:
               return False

def fun_case(cadena):
      global info_buncher
      global block
      cadena=str(cadena).upper()
      caso=0
      try:
          if cadena[0]=='B' and cadena[1] != 'K':
               caso=1
               info_buncher["BLOCK_ID"]=block
          elif cadena[0]=='C' and cadena[1] != 'M':
               caso=2
          elif(cadena[0]=='R'):
               caso=3
          else:
             caso=0
          return caso
      except:
         return caso


def processbuncher(cadena,case):
        global info_buncher
        global id
        global info_sorter
        case2=case
        #print("CASE2 entrando a funcion")
        #print(case2)
        cadena=str(cadena).upper()
        try:
       # print(cadena)
          if  cadena[0]=='T':
                 info_buncher["TUB_ID"]=str(cadena[1:])
        #        print("info")
        #        print(info_buncher["TUB_ID"])
          elif cadena[0]=='B'  and cadena[1] != 'K':
                 id=str(cadena[1:])
                 if len(id)==1:
                     id='0' +id
                 info_buncher["BUNCHER_ID"]=str(cadena[1:])

          elif cadena[0]== 'C' and cadena[1] != 'M':
                 id=str(cadena[1:])
                 #print("reconocio carnet clasificador")
                 if len(id)==1:
                      id='0'+id
                 #print("ID CLASIFICADOR")
                 #print(id)
                 #print(str(info_sorter["SORTER_ID"]))
                 info_sorter["SORTER_ID"]=id
                 case2=2
                 #print("CASE2 DESPUES DE RECONOCER")
                 #print(case2)

          elif cadena[0]=='V':
                 info_buncher["VARIETY_ID"]=str(cadena[1:])

          elif cadena[0]=='R':
                 if devramo(cadena[1:]):
                     case2= 3
                 else:
                     info_buncher["BUNCH_ID"]=str(cadena[1:])

          elif cadena[0:2] == 'CM':
                 info_buncher["COMPOSITION_ID"]=str(cadena[2:])
                 index=encuentra(cadena,'/')
                 info_buncher["TxR"]=str(cadena[2:index])
                 info_buncher["GR"]=str(cadena[index+1:])

          #print("CASE FINAL FUNCION")
          #print(case2)
          return case2
        except:
           return case2

def checkinfobuncher():
       global info_buncher
       try:
          if  'X' in str(info_buncher["BUNCHER_ID"]) or 'x' in str(info_buncher["BUNCHER_ID"]) :
                  return False
          elif 'X' in str(info_buncher["TUB_ID"]) or 'x' in str(info_buncher["TUB_ID"]) :
                  return False
          elif 'X' in str(info_buncher["TxR"]) or 'x' in str(info_buncher["TxR"]):
                  return False
          elif 'X' in str(info_buncher["GR"]) or 'x' in str(info_buncher["GR"]) :
                  return False
          elif 'X' in str(info_buncher["VARIETY_ID"]) or 'x' in str(info_buncher["VARIETY_ID"]) :
                  return False
          elif 'X' in str(info_buncher["BUNCH_ID"]) or 'x' in str(info_buncher["BUNCH_ID"]) :
                  return False
          else :
                  return True
       except:
          return False


def devramo(coderamo):
     #Preguntarpor Ramo
    return False

if __name__ == '__main__':
    try:
          while True:
               process=multiprocessing.Process(target=initialscreen,args=(display,'XX'))
               process.start()
               time.sleep(0.2)
               que=queue.Queue()
               t=threading.Thread(target=barcode_reader,args=(que,))
               t.start()
               t.join()
               #scan=que.get()
               #print(bloque)
               process.terminate()
               time.sleep(0.1)
               display.lcd_clear()
               time.sleep(0.5)
               scan=que.get()
               ckblock=getbloque(scan)
               if ckblock:
                    display.lcd_clear()
                    screens.scanbloque(str(block),display)
                    time.sleep(0.5)
                    #POST REGISTRAR
                    services.savedevice(info_device)
                    display.lcd_clear()
               while  ckblock:
                        time.sleep(0.1)
                        display.lcd_clear()
                        time.sleep(0.5)
                        process=multiprocessing.Process(target=screendefault,args=(display,))
                        process.start()
                        time.sleep(0.2)
                        t=threading.Thread(target=barcode_reader,args=(que,))
                        t.start()
                        t.join()
                        #scan=que.get()
                        process.terminate()
                        scan=que.get()
                        display.lcd_clear()
                        time.sleep(0.2)
                        valido=scancarnet(scan)
                        while  valido :
                           case=fun_case(scan)
                           while case==1:   #BUNCHER
                                  print("FALTA")
                                  time.sleep(0.2)
                                  display.lcd_clear()
                                  process=multiprocessing.Process(target=buncherscreen,args=(display,))
                                  process.start()
                                  time.sleep(0.2)
                                  t=threading.Thread(target=barcode_reader,args=(que,))
                                  t.start()
                                  t.join
                                  scan=que.get()
                                  process.terminate()
                                  case2=processbuncher(scan,case)
                                  print(case2)
                                  if(case2 != case):
                                       #print(case2)
                                       case=case2
                                       break
                                  flag=checkinfobuncher()
                                  if  flag:
                                      print("GUARDANDO")
                                      buncherscreen(display)
                                      time.sleep(1)
                                      services.savebunch(info_buncher,info_device) #post data
                                      info_buncher["BUNCH_ID"]="XXXXXXX"
                           while case==2:   #NACIONAL
                                   print("NACIONAL")
                           while case==3:    #DEV
                                   print("DEVOLUCION")
    except KeyboardInterrupt:
         display.lcd_clear()
         pass
