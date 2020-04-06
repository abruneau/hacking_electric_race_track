#!/usr/bin/env python

import RPi.GPIO as GPIO
import time

import env

def _setup():
     # Configure the GPIO pin
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(env.LATCH, GPIO.OUT) # P0 
    GPIO.setup(env.CLK, GPIO.OUT) # P1 
    GPIO.setup(env.dataBit, GPIO.OUT) # P7

    # Setup IO
    GPIO.output(env.LATCH, 0)
    GPIO.output(env.CLK, 0)

def _cleanup():
    GPIO.cleanup(env.LATCH)
    GPIO.cleanup(env.CLK)
    GPIO.cleanup(env.dataBit)


def _pulseCLK():
    global CLK
    GPIO.output(env.CLK, 1)
   # time.sleep(.01) 
    GPIO.output(env.CLK, 0)
    return

def _serLatch():
    GPIO.output(env.LATCH, 1)
   # time.sleep(.01)
    GPIO.output(env.LATCH, 0)
    return

# MSB out first!
def light(value):
    for  x in range(0,8):
        temp = value & 0x80
        if temp == 0x80:
           GPIO.output(env.dataBit, 1) # data bit HIGH
        else:
           GPIO.output(env.dataBit, 0) # data bit LOW
        _pulseCLK()        
        value = value << 0x01 # shift left
    _serLatch() # output byte
    return 

def countdown():
    sequence = [1,3,7,8,0]

    _setup()

    try:
        for code in sequence:
            light(code)
            time.sleep(1)
    finally:
        _cleanup()

def finish():
    sequence = [15,0,15,0,15,0,15,0,15,0,15,0]

    _setup()
    try:
        for code in sequence:
            light(code)
            time.sleep(.2)
    finally:
        _cleanup()
