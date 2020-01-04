import json
import requests
import sys
import os
import socket
import fcntl
import struct


#info_device={"MAC_ADDRESS":"xx","IP_ADDRESS":"xxx","BLOCK_ID":"01","STOP_ID":"xxx"}
#info_buncher={"BUNCHER_ID":"xx","BUNCH_ID":"xx","COMPOSITION_ID":"xx","TUB_ID":"xx","TxR":"xx","GR":"xx","VARIETY_ID":"xx","BLOCK_ID":"xx"}

def getMAC(interface='wlan0'):
  # Return the MAC address of the specified interface
  try:
    str = open('/sys/class/net/%s/address' %interface).read()
  except:
    str = "00:00:00:00:00:00"
  return str[0:17]


def get_local_ip_address(target):
  ipaddr = ''
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((target, 8000))
    ipaddr = s.getsockname()[0]
    s.close()
  except:
    pass

  return ipaddr

def  savedevice(info_device):
       mac=str(getMAC())
       mac=mac.upper()
       ip=str(get_local_ip_address('10.0.1.1'))
       ip=ip.upper()
       info_device["MAC_ADDRESS"]=mac
       info_device["IP_ADDRESS"]=ip
       #print(getMAC)
       hostname="http://tfsnew.vida18.com:8078/api/devices"
       #responde = os.system("ping -c 1 "+hostname)
       r=requests.post(hostname,json=info_device)
       if str(r.json())== '1':
           return True
       else:
           return False

def savebunch(info_buncher,info_device):
       mac=str(getMAC())
       mac=mac.upper()
       info_device["MAC_ADDRESS"]=mac
       info_total={"MAC_ADDRESS":info_device["MAC_ADDRESS"], 
       "STOP_ID":'S'+str(info_device["STOP_ID"]),
       "BLOCK_ID":'BK'+str(info_device["BLOCK_ID"]),
       "BUNCHER_ID":'B'+str(info_buncher["BUNCHER_ID"]),
       "BUNCH_ID":'R'+str(info_buncher["BUNCH_ID"]),
       "COMPOSITION_ID":'CM'+str(info_buncher["COMPOSITION_ID"]),
       "SORTER_ID":'C'+str(info_buncher["BUNCHER_ID"]),
       "TUB_ID":'T'+str(info_buncher["TUB_ID"]),
       "VARIETY_ID":'V'+str(info_buncher["VARIETY_ID"])
       }
       hostname="http://tfsnew.vida18.com:8078/api/tracking"
       r=requests.post(hostname,json=info_total)
       if str(r.json())== '1':
           return True
       else:
           return False


#print(savebunch(info_buncher,info_device))
