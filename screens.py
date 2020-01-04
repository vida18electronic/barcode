import lcddriver
import time
import array as arr

# Load the driver and set it to "display"
# If you use something from the driver library use the "display." prefix first
#display = lcddriver.lcd()

# Main body of code
def scanbloque(bloque,display):
       # display.lcd_clear()
        bq="        "+str(bloque)+"        "
        display.lcd_display_string("      VIDA 18",1)
        display.lcd_display_string("     BIENVENIDO",2)
        display.lcd_display_string("   ESCANEE BLOQUE", 3) # Write line of text to first line of display
        display.lcd_display_string(bq, 4) # Write line of text to second line of display
       # display.lcd_clear()

def twinkle(lines,display):
        for line in lines:
            # print(line)
             display.lcd_display_string("                    ",line)

def buncher (display,info_buncher):

          ID_RAMO=str(info_buncher["BUNCH_ID"])
          if len(ID_RAMO) < 7:
               indice=len(ID_RAMO)
               while indice < 7:
                     ID_RAMO=ID_RAMO+' '
                     indice += 1

          ID_TINA=str(info_buncher["TUB_ID"])
          if len(ID_TINA) < 6:
               indice=len(ID_TINA)
               while indice < 6:
                     ID_TINA=ID_TINA+' '
                     indice += 1

          TxR=str(info_buncher["TxR"])
          if len(TxR) < 4:
               indice=len(TxR)
               while indice < 4:
                     TxR=TxR+' '
                     indice += 1

          GR=str(info_buncher["GR"])
          if len(GR) < 4:
               indice=len(GR)
               while indice < 4:
                     GR=GR+' '
                     indice += 1

          VARIEDAD=str(info_buncher["VARIETY_ID"])
          if len(VARIEDAD) < 11:
               indice=len(VARIEDAD)
               while indice < 11:
                     VARIEDAD=VARIEDAD+' '
                     indice += 1

#          print("ID_TINA")
#          print(ID_TINA)
          line1='BLOQUE:'+str(info_buncher["BLOCK_ID"])+' '+'BUNCHER:'+str(info_buncher["BUNCHER_ID"])
          line2='#R:' + ID_RAMO +' ' +'#T:' + ID_TINA
          line3='TxR:'+TxR +'     '+'GR:' + GR
          line4='VARIEDAD:' + VARIEDAD
#          print(line1)
#          print(line2)
#          print(line3)
#          print(line4)
          display.lcd_display_string(line1,1)
          display.lcd_display_string(line2,2)
          display.lcd_display_string(line3,3)
          display.lcd_display_string(line4,4)


def blink_default(display,block,info_buncher):

          line1='BLOQUE:'+block+'           '
          display.lcd_display_string(line1,1)


#try:
#    while True:
            #
#           time.sleep(0.5)
#           twinkle([3,4])
#           time.sleep(0.5)
#except KeyboardInterrupt:
#       print("CLEAN")
#       display.lcd_clear()
