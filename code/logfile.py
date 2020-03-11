#!/usr/bin/env python

import threading
import json

import env

lock = threading.Lock()

def openfile():
    return open(env.filename, 'a')

def log(f, t, e, p):
    try:
        lock.acquire()

        event = {
            "time": t.isoformat(),
            "event": e
        }

        j = json.dumps(event)

        f.write("{0}\n".format(j))
        f.flush()

        lock.release()
        if p:
            print t, env.events[e]
    except Exception as e: 
        print("An exception occurred")
        print(e)