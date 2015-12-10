import zmq
from threading import Thread
import json
import time
import numpy as np
import pygame

import logging
import sys

class listener(Thread):
    
    def __init__(self,IP,port):
        # setup zmq context
        Thread.__init__(self)
        self._IP = IP
        self._port = port
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.REP)
        self._socket.bind("tcp://"+self._IP+":"+self._port)
        self._padOut = []
        self._active = True
        
    def run(self):
        print "XBOX Pad server launched."
        while self._active:
            # waiting for a message
            reply = self._socket.recv_json()
            if reply.has_key("pad"):
                if reply["pad"].has_key("get_pad"):
                    self._socket.send_json(self._padOut)
                else:
                    print "message not recognized."
                    print reply
                    self._socket.send_json("{}")

if __name__ == "__main__":
    task = listener('127.0.0.1','8081')
    task.start()
    pygame.init()
    pygame.joystick.init()
    dt = 0.02
    
    goon = True
    
    while goon:
        t = time.time()
        pygame.event.get()
        nj = pygame.joystick.get_count()
        jlist = []
        for ij in range(nj):
            jlist.append({})
            j = pygame.joystick.Joystick(ij)
            j.init()
            jlist[ij]["axe X1"] = j.get_axis(0)
            jlist[ij]["axe Y1"] = j.get_axis(1)
            jlist[ij]["axe X2"] = j.get_axis(3)
            jlist[ij]["axe Y2"] = j.get_axis(4)
            jlist[ij]["gache"] = j.get_axis(2)
            jlist[ij]["hat X1"] = j.get_hat(0)[0]
            jlist[ij]["hat Y1"] = j.get_hat(0)[1]
            jlist[ij]["button A"] = j.get_button(0)
            jlist[ij]["button B"] = j.get_button(1)
            jlist[ij]["button X"] = j.get_button(2)
            jlist[ij]["button Y"] = j.get_button(3)
            jlist[ij]["button L"] = j.get_button(4)
            jlist[ij]["button R"] = j.get_button(5)
            jlist[ij]["button back"] = j.get_button(6)
            jlist[ij]["button start"] = j.get_button(7)
        task._padOut = jlist
        while time.time()-t<=dt:
            time.sleep(0.01)