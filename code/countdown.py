#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
from multiprocessing import Process

LATCH = 23 # Pin 12 Latch clock
CLK = 27 # Pin 11 shift clock
dataBit = 22 # Pin 14 A
BeepPin = 24

# Configure the GPIO pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(LATCH, GPIO.OUT) # P0 
GPIO.setup(CLK, GPIO.OUT) # P1 
GPIO.setup(dataBit, GPIO.OUT) # P7
GPIO.setup(BeepPin, GPIO.OUT)

# Setup IO
GPIO.output(LATCH, 0)
GPIO.output(CLK, 0)
GPIO.output(BeepPin, 0)

def runInParallel(*fns):
    proc = []
    for fn in fns:
        p = Process(target=fn)
        p.start()
        proc.append(p)
    for p in proc:
        p.join()

### ############################
### LED control
### ############################

def pulseCLK():
    GPIO.output(CLK, 1)
   # time.sleep(.01) 
    GPIO.output(CLK, 0)
    return

def serLatch():
    GPIO.output(LATCH, 1)
   # time.sleep(.01)
    GPIO.output(LATCH, 0)
    return

# MSB out first!
def ssrWrite(value):
    for  x in range(0,8):
        temp = value & 0x80
        if temp == 0x80:
           GPIO.output(dataBit, 1) # data bit HIGH
        else:
           GPIO.output(dataBit, 0) # data bit LOW
        pulseCLK()        
        value = value << 0x01 # shift left
    serLatch() # output byte
    return 

def lightup():
    sequence = [1,3,7,8,0]

    for code in sequence:
        ssrWrite(code)
        time.sleep(1)


### #####################################
### Sound control
### #####################################

def bip(frequency, duration):
    # This is the semiperiod of each note.
    beepDelay = 1.0 / frequency ;

    # This is how much time we need to spend on the note.
    Time = int(duration / (beepDelay * 2 ))
    for i in range(0, Time):
        # 1st semiperiod
        GPIO.output(BeepPin, 1)
        time.sleep(beepDelay)
        # 2nd semiperiod
        GPIO.output(BeepPin, 0)
        time.sleep(beepDelay)

def makenoize():
    for i in range(0,3):
        bip(880,0.1)
        time.sleep(0.9)
    
    bip(880*2, 1)


def start():
    runInParallel(lightup, makenoize)
