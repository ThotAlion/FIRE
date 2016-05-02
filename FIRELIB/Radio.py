from numpy import *
import Block
from Connexion import *
import Tools
import time
import zmq
from threading import Thread

class listener(Thread):
    
    def __init__(self,IP,port):
        # setup zmq context
        Thread.__init__(self)
        self._IP = IP
        self._port = port
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.REP)
        self._socket.bind("tcp://"+self._IP+":"+self._port)
        self._dicoIn = {}
        self._dicoOut = {"Finished":0}
        self._active = True
        self._reset = False
        
    def run(self):
        print "toto"
        while self._active:
            # waiting for a message
            self._reset = False
            reply = self._socket.recv_json()
            #print reply
            if reply.has_key("dico"):
                if reply["dico"].has_key("get_dico"):
                    self._socket.send_json(self._dicoOut)
                    print self._dicoOut
                elif reply["dico"].has_key("set_dico"):
                    self._dicoIn = reply["dico"]["set_dico"]
                    self._socket.send_json({})
                else:
                    print "message not recognized."
                    print reply
                    self._socket.send_json("{}")

class Radio(Block.Block):
    """ this class describes a block """
    
    def __init__(self):
        Block.Block.__init__(self)
        self.outputs["Tape"] = Connexion(default = "TAPES_CSV/_mou.csv")
        self.outputs["Number"] = Connexion(default = -1)
        self.inputs["Finished"] = Connexion(default = 0)

    def start(self):
        self.task = listener('0.0.0.0','8080')
        self.task.start()
        
    def init(self,f):
        a=1
        return f
    
    def getInputs(self,f):
        self.task._dicoOut ={"Finished":self.inputs['Finished'].getValue(f)}
        
    def setOutputs(self,f):
        if self.task._dicoIn.has_key("Tape"):
            self.outputs["Tape"].setValue(self.task._dicoIn["Tape"],f)
        else:
            self.outputs["Tape"].setValue("TAPES_CSV/_mou.csv",f)
            
        if self.task._dicoIn.has_key("Number"):    
            self.outputs["Number"].setValue(self.task._dicoIn["Number"],f)
        else:
            self.outputs["Number"].setValue(0,f)
        return f
           
    def close(self):
        a=1
        