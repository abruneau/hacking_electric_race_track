#!/usr/bin/env python

import time
from gpiozero import Button
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from multiprocessing import Process

import env
import leds
import buzzer

def print_header(title):
    print ""
    print ""
    print "#############################"
    print "###"
    print "###", title
    print "###"
    print "#############################"

def runInParallel(*fns):
    proc = []
    for fn in fns:
        p = Process(target=fn)
        p.start()
        proc.append(p)
    for p in proc:
        p.join()

def test_button(pin, name):
    try:
        button = Button(pin, pull_up=False)
        print "Press button: ", name
        while True: # Run forever
            if button.is_pressed:
                print("Button was pressed")
                break
            time.sleep(0.2) 
    except KeyboardInterrupt:
        print('Skip')

def test_countdown():
    try:
        runInParallel(leds.countdown, buzzer.countdown)
    except KeyboardInterrupt:
        print('Skip')

def test_finish():
    try:
        runInParallel(leds.finish, buzzer.finish)
    except KeyboardInterrupt:
        print('Skip')

def test_sensor(pin, name):
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    try:
        print "Trigger", name
        while True: # Run forever
            state = GPIO.input(pin)
            if not state:
                print name, " was triggered"
                break
        time.sleep(0.02)
    except KeyboardInterrupt:
        print('Skip')
    finally:
        GPIO.cleanup(pin)

def main():
    print_header("Testing Start Button")
    test_button(env.startButton, "Start Button")

    print_header("Testing Stop Button")
    test_button(env.stopButton, "Stop Button")

    print_header("Testing Sensor 1")
    test_sensor(env.sensors[1], "Sensor 1")
    
    print_header("Testing Sensor 2")
    test_sensor(env.sensors[2], "Sensor 2")

    print_header("Testing countdown")
    test_countdown()

    print_header("Testing finish")
    test_finish()
    

if __name__ == '__main__':
    main()