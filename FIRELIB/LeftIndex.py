from numpy import *
import Block
from Connexion import *
import Tools
import time
import Leap

class LeftIndex(Block.Block):
    """ this class describes a block """
    
    def __init__(self):
        Block.Block.__init__(self)
        self.outputs["index pitch"] = Connexion(default = "M")
        self.outputs["index yaw"] = Connexion(default = "M")

    def start(self):
        self.leap = Leap.Controller()
        
    def init(self):
        a=1
    
    def getInputs(self,f):
        a=1
        
    def setOutputs(self,f):
        self.outputs["index pitch"].setValue("M",f)
        self.outputs["index yaw"].setValue("M",f)
        frame = self.leap.frame()
        for fin in frame.fingers:
            if fin.hand.is_left and fin.type == fin.TYPE_INDEX:
                self.outputs["index pitch"].setValue(fin.direction.pitch*180.0/pi,f)
                self.outputs["index yaw"].setValue(fin.direction.yaw*180.0/pi,f)
        return f
           
    def close(self):
        a=1
        