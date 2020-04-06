#!/usr/bin/env python

import time
import datetime
from gpiozero import Button
from multiprocessing import Process

import env
import leds
import buzzer
import race
import logfile

def runInParallel(*fns):
    proc = []
    for fn in fns:
        p = Process(target=fn)
        p.start()
        proc.append(p)
    for p in proc:
        p.join()

def main():
    run = True

    startButton = Button(env.startButton, pull_up=False)
    stopButton = Button(env.stopButton, pull_up=False)

    try:
        while True: # Run forever
            if startButton.is_pressed and stopButton.is_pressed:
                f = logfile.openfile()
                logfile.log(f, datetime.datetime.now(), 4, True)
                f.close()
            elif startButton.is_pressed and not race.running():
                runInParallel(leds.countdown, buzzer.countdown)
                race.start()
                while race.running() and not stopButton.is_pressed:
                    time.sleep(0.2)
                
                if stopButton.is_pressed and race.running():
                    race.stop()
                if not stopButton.is_pressed and not race.running():
                    runInParallel(leds.finish, buzzer.finish)
                    race.wait()
            time.sleep(0.2) 
    except KeyboardInterrupt:
        print('Goodbye !!!')
        if race.running():
            race.stop()

if __name__ == '__main__':
    main()