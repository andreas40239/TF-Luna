# -*- coding: utf-8 -*-
#
# PLEASE SEE library TFLUNA at pypi.org for a great solution to this interface.
# I simply copied part of the code for my own trial+error+learning approach.
#
# Step 1: disconnect and reconnect your TTL-to-USB adapter
# Step 2: Type this command in your linux-shell:   dmesg | grep tty
#         You should see which USB-device was connected and how it is called
# Step 3: Edit the name in line 10
import serial
import time
import binascii

#/dev/ttyUSB0   921600 115200 9600 
interface_luna = serial.Serial('/dev/ttyUSB0',115200)  
if interface_luna.isOpen() :
    print("open success")
else :
    print("open failed") 


# command codes
luna_getVersion    = [0x5a,0x04,0x14,0x00]   
luna_setBaud9600   = [0x5a,0x08,0x06,0x80,0x25,0x00,0x00,0x00]
luna_setBaud115200 = [0x5a,0x08,0x06,0x00,0xC2,0x01,0x00,0x00]
luna_setBaud921600 = [0x5a,0x08,0x06,0x00,0x10,0x0E,0x00,0x00]
luna_saveSettings  = [0x5a,0x04,0x11,0x00]
luna_enableOutput  = [0x5a,0x05,0x07,0x01,0x00]
luna_disableOutput = [0x5a,0x05,0x07,0x00,0x00]

interface_luna.write(luna_enableOutput)
time.sleep(0.5)

while True:
    counter = interface_luna.in_waiting
    bytes_to_read = 9
    if counter > bytes_to_read-1:
        bytes_serial = interface_luna.read(bytes_to_read) 
        interface_luna.reset_input_buffer() # reset buffer

        if bytes_serial[0] == 0x59 and bytes_serial[1] == 0x59: # check first two bytes
            distance = bytes_serial[2] + bytes_serial[3]*256 # distance in next two bytes
            strength = bytes_serial[4] + bytes_serial[5]*256 # signal strength in next two bytes
            temperature = bytes_serial[6] + bytes_serial[7]*256 # temp in next two bytes
            temperature = (temperature/8) - 256 # temp scaling and offset
            print(
                f"Distance: {distance} cm, "
                f"Strength: {strength:2.0f} / 65535 (16-bit), "
                f"Chip Temperature: {temperature:2.1f} C")
