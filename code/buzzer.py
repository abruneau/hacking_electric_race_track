#!/usr/bin/env python

from gpiozero import TonalBuzzer
from gpiozero.tones import Tone
import time

import env

def bip(beeper,frequency, duration):
    beeper.play(frequency)
    time.sleep(duration)
    beeper.stop()

def countdown():
    beeper = TonalBuzzer(env.BeepPin, octaves=2)
    for i in range(0,3):
        bip(beeper, Tone("A4"),0.1)
        time.sleep(0.9)
    bip(beeper, Tone("A5"), 1)

def finish():
    beeper = TonalBuzzer(env.BeepPin, octaves=2)
    bip(beeper, Tone("A5"), 2)

def main():
    try:
        countdown()
    except KeyboardInterrupt:
        print('Skip')

if __name__ == '__main__':
    main()