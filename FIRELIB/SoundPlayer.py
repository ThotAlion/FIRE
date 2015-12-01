from numpy import *
import Block
from Connexion import *
import Tools
import time
import pygame

class SoundPlayer(Block.Block):
    """ this class describes a block """
    
    def __init__(self,Filename,mode = "Stop"):
        Block.Block.__init__(self)
        pygame.init()
        pygame.mixer.init()
        self.tape = pygame.mixer.Sound(Filename)
        self.inputs["play"] = Connexion(default = 0.0)
        

    def start(self):
        a=1
        
    def init(self,f):
        return f
    
    def getInputs(self,f):
        a=1
        
    def setOutputs(self,f):
        if self.inputs["play"].getValue(f) == 1:
            self.tape.play(loops = -1)
        else:
            self.tape.stop()    
        
        return f
           
    def close(self):
        a=1
        