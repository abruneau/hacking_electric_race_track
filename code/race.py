#!/usr/bin/env python

import time
import RPi.GPIO as GPIO
import datetime
import threading
import json

import env
import logfile

threads = []
run_event = threading.Event()
laps = 10

def setup():
    # Configure the GPIO pin
    GPIO.setmode(GPIO.BCM)
    for sensor in env.sensors:
        GPIO.setup(env.sensors[sensor], GPIO.IN, pull_up_down=GPIO.PUD_UP)

def cleanup():
    for sensor in env.sensors:
        GPIO.cleanup(env.sensors[sensor])

def read_sensor(sensor, f, run_event):
    laps_done = -1

    # Si on detecte un passage, on enregistre
    # et on attend que la voiture soit passee
    while run_event.is_set() and laps_done < laps:
        state = GPIO.input(env.sensors[sensor])
        if not state:
            # la voiture passe
            logfile.log(f, datetime.datetime.now(), sensor, True)
            laps_done += 1
            while not state and run_event.is_set():
                state = GPIO.input(env.sensors[sensor])
                time.sleep(0.02)  # Pause pour ne pas saturer le processeur
            # La voiture est passee
        time.sleep(0.02)  # Pause pour ne pas saturer le processeur

def start():
    global threads, f, run_event
    setup()
    f = logfile.openfile()

    run_event.set()

    logfile.log(f, datetime.datetime.now(), 0, True)

    for sensor in env.sensors:
        t = threading.Thread(target=read_sensor, args=(sensor, f, run_event))
        t.start()
        threads += [t]

def running():
    global threads
    runs = False
    for t in threads:
        if t.isAlive():
            runs = True
            break

    return runs

def wait():
    global threads, f
    for t in threads:
        t.join()

    logfile.log(f, datetime.datetime.now(), 3, True)
    f.close()
    cleanup()

def stop():
    global run_event
    print "attempting to close threads."
    run_event.clear()
    wait()

def main():
    setup()
    start()
    try:
        wait()
    except KeyboardInterrupt:
        stop()

if __name__ == '__main__':
    main()