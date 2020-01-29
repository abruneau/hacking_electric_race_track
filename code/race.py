#!/usr/bin/env python

import time
import RPi.GPIO as GPIO
import datetime
import threading
import json

lock = threading.Lock()
pins = {18: "1", 17: "2"}

threads = []
f = open("results.txt", 'a')
run_event = threading.Event()

def log(f, t, text):
    try:
        lock.acquire()

        event = {
            "time": t.isoformat(),
            "car": text
        }

        j = json.dumps(event)

        f.write("{0}\n".format(j))
        f.flush()

        lock.release()
    except Exception as e: 
        print("An exception occurred")
        print(e)
        

def read_sensor(channel, f, run_event):
    GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # Si on detecte un passage, on enregistre
    # et on attend que la voiture soit passee
    while run_event.is_set():
        state = GPIO.input(channel)
        if not state:
            # la voiture passe
            log(f, datetime.datetime.now(), pins[channel])
            print datetime.datetime.now(), pins[channel]
            while not state and run_event.is_set():
                state = GPIO.input(channel)
                time.sleep(0.02)  # Pause pour ne pas saturer le processeur
            # La voiture est passee
        time.sleep(0.02)  # Pause pour ne pas saturer le processeur

def start():
    global threads, f, run_event

    # Configure the GPIO pin
    GPIO.setmode(GPIO.BCM)

    run_event.set()

    car1 = threading.Thread(target=read_sensor, args=(18, f, run_event))
    car1.start()
    threads += [car1]
    car2 = threading.Thread(target=read_sensor, args=(17, f, run_event))
    car2.start()
    threads += [car2]

def stop():
    global threads, f, run_event
    print "attempting to close threads."
    run_event.clear()
    for t in threads:
        t.join()
    print "threads successfully closed"
    print 'Cleaning up GPIO'
    GPIO.cleanup()
    f.close()

def main():
    
    start()

    try:
        while 1:
            time.sleep(.1)
    except KeyboardInterrupt:
        stop()

if __name__ == '__main__':
    main()