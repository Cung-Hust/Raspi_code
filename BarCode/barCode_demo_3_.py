#RT870 python test demo
#USB-CDC readme
#by RTSCAN 20200901
 
 
import sys
import serial
import time
 
#default usb device /dev/ttyS0 115200 8n1
ser = serial.Serial("/dev/hidraw0", 115200, timeout=0.5)
 
print("Serial test start...")
if ser != None:
    print("Serial ready")
else:
    print("serial not ready")
    sys.exit()
 
ser.timerout=1 #read time out
ser.writeTimeout = 0.5 #write time out.
 
def printHex(str):
    for i in str:
        print("0x%02x"%ord(i)),
    print("")
 
def send_cmd(str):
    ser.write(str)
    time.sleep(0.2)
    t = ser.read(ser.in_waiting)