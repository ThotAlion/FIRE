from numpy import *
import Block
from Connexion import *
import Tools
import time
import pygame

class xboxPad(Block.Block):
    """ this class describes a block """
    
    def __init__(self):
        Block.Block.__init__(self)
        self.outputs["axe X1"] = Connexion(default = NaN)
        self.outputs["axe Y1"] = Connexion(default = NaN)
        self.outputs["axe X2"] = Connexion(default = NaN)
        self.outputs["axe Y2"] = Connexion(default = NaN)
        pygame.joystick.init()
        

    def start(self):
        self.j = pygame.joystick.Joystick(0)
        self.active = True
        
    def init(self):
        a=1
    
    def getInputs(self,f):
        a=1
        
    def setOutputs(self,f):
        self.j.init()
        self.outputs["axe X1"].setValue(self.get_axis(0),f)
        self.outputs["axe Y1"].setValue(self.get_axis(1),f)
        self.outputs["axe X2"].setValue(self.get_axis(2),f)
        self.outputs["axe Y2"].setValue(self.get_axis(3),f)
           
    def close(self):
        a=1
        