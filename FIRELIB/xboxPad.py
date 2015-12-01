from numpy import *
import Block
from Connexion import *
import Tools
import time
import pygame

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
        pygame.init()
        pygame.joystick.init()
        

    def start(self):
        a=1
        
        
    def init(self,f):
        return f
    
    def getInputs(self,f):
        a=1
        
    def setOutputs(self,f):
        pygame.event.get()
        j = pygame.joystick.Joystick(self.n)
        j.init()
        self.outputs["axe X1"].setValue(j.get_axis(0),f)
        self.outputs["axe Y1"].setValue(j.get_axis(1),f)
        self.outputs["axe X2"].setValue(j.get_axis(3),f)
        self.outputs["axe Y2"].setValue(j.get_axis(4),f)
        self.outputs["gache"].setValue(j.get_axis(2),f)
        self.outputs["hat X1"].setValue(j.get_hat(0)[0],f)
        self.outputs["hat Y1"].setValue(j.get_hat(0)[1],f)
        self.outputs["button A"].setValue(j.get_button(0),f)
        self.outputs["button B"].setValue(j.get_button(1),f)
        self.outputs["button X"].setValue(j.get_button(2),f)
        self.outputs["button Y"].setValue(j.get_button(3),f)
        self.outputs["button L"].setValue(j.get_button(4),f)
        self.outputs["button R"].setValue(j.get_button(5),f)
        self.outputs["button back"].setValue(j.get_button(6),f)
        self.outputs["button start"].setValue(j.get_button(7),f)

        return f
           
    def close(self):
        a=1
        