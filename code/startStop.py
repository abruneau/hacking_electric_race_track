#!/usr/bin/env python
import time
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

import countdown


GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 

while True: # Run forever
    state = GPIO.input(25)
    if state:
        countdown.start()
        while state:
            state = GPIO.input(25)
            time.sleep(0.2)
    time.sleep(0.2) 