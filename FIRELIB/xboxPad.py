from numpy import *
import Block
from Connexion import *
import Tools
import time
import zmq

class xboxPad(Block.Block):
    """ this class describes a block """
    
    def __init__(self,n):
        Block.Block.__init__(self)
        self.outputs["axe X1"] = Connexion(default = 0)
        self.outputs["axe Y1"] = Connexion(default = 0)
        self.outputs["axe X2"] = Connexion(default = 0)
        self.outputs["axe Y2"] = Connexion(default = 0)
        self.outputs["gache"] = Connexion(default = 0)
        self.outputs["hat X1"] = Connexion(default = 0)
        self.outputs["hat Y1"] = Connexion(default = 0)
        self.outputs["button A"] = Connexion(default = 0)
        self.outputs["button B"] = Connexion(default = 0)
        self.outputs["button X"] = Connexion(default = 0)
        self.outputs["button Y"] = Connexion(default = 0)
        self.outputs["button L"] = Connexion(default = 0)
        self.outputs["button R"] = Connexion(default = 0)
        self.outputs["button back"] = Connexion(default = 0)
        self.outputs["button start"] = Connexion(default = 0)
        self.n = n
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.REQ)
        self._socket.connect("tcp://127.0.0.1:8081")
        self.poll = zmq.Poller()
        self.poll.register(self._socket,zmq.POLLIN)

    def start(self):
        a=1
 
    def init(self,f):
        return f
    
    def getInputs(self,f):
        a=1
        
    def setOutputs(self,f):
        t0 = Tools.getTime()
        req = {"pad":{"get_pad":"1"}}
        self._socket.send_json(req)
        expect = True
        while expect:
            socks = dict(self.poll.poll(100))
            #print socks.get(self._socket)
            if socks.get(self._socket) == zmq.POLLIN:
                reply = self._socket.recv_json()
                if not reply:
                    break
                else:
                    j = reply[self.n]
                    for button in self.outputs:
                        if j.has_key(button):
                            self.outputs[button].setValue(j[button],f)
                    expect = False
            else:
                #print "reconnect"
                self._socket.setsockopt(zmq.LINGER, 0)
                self._socket.close()
                self.poll.unregister(self._socket)
                self._socket = self._context.socket(zmq.REQ)
                self._socket.connect("tcp://127.0.0.1:8081")
                self.poll.register(self._socket,zmq.POLLIN)
                self._socket.send_json(req)
        return f
           
    def close(self):
        a=1
        