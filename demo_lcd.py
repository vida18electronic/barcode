# Simple string program. Writes and updates strings.
# Demo program for the I2C 16x2 Display from Ryanteck.uk
# Created by Matthew Timmons-Brown for The Raspberry Pi Guy YouTube channel

# Import necessary libraries for communication and display use
import lcddriver
import time

# Load the driver and set it to "display"
# If you use something from the driver library use the "display." prefix first
display = lcddriver.lcd()

# Main body of code
try:
    while True:
        # Remember that your sentences can only be 16 characters long!
        print("Writing to display")
        display.lcd_display_string("VIDA18,BONCHER,LISTO",1)
        display.lcd_display_string("BLOQUE:xx PAREJA:xx", 2) # Write line of text to first line of display
        display.lcd_display_string("TINA:xxxx COM:xx/xx", 3) # Write line of text to second line of display
        display.lcd_display_string("VARIEDAD:xxxxxxx",4)
                                             # Give time for t
        #display.lcd_display_string("Welcome VIDA18!",3) 
        #display.lcd_display_string("You Scan", 4)  # Refresh the first line of display with a different message
        #time.sleep(2)                                     # Give time for the message to be read
        #display.lcd_clear()                               # Clear the display of any data
        time.sleep(2)                                     # Give time for the message to be read

except KeyboardInterrupt: # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
    print("Cleaning up!")
    display.lcd_clear()
