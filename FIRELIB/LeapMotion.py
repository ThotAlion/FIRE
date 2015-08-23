from Connexion import Connexion
from Interface import Interface as Interface_
from numpy import *
import Leap

class LeapMotion(Interface_):
    """Interface for Leap-Motion device"""
    
    def __init__(self,name = "LeapMotion"):
        """constructor of LeapMotion"""
        Interface_.__init__(self,name=name)
        rootInputs = self._inputs.invisibleRootItem()
        rootOutputs = self._outputs.invisibleRootItem()
        
        
        # list the interface of the Dynamixel motors
        # head_z
        for hand in ["right","left"]:
            for finger in ["thumb","index","middle","ring","pinky"]:
                
                rootOutputs.appendRow(Connexion(hand+"_"+finger+"_tip_position",
                direction=Connexion.OUT,
                description = "Position of the "+hand+" "+finger,
                unit = "m",
                connectedTo="",
                valueInit = NaN, 
                valueMin = -Inf, 
                valueMax = Inf))
                
                rootOutputs.appendRow(Connexion(hand+"_"+finger+"_pitch",
                direction=Connexion.OUT,
                description = "Pitch angle of the "+hand+" "+finger,
                unit = "deg",
                connectedTo="",
                valueInit = NaN, 
                valueMin = -Inf, 
                valueMax = Inf))
                
                rootOutputs.appendRow(Connexion(hand+"_"+finger+"_yaw",
                direction=Connexion.OUT,
                description = "Yaw angle of the "+hand+" "+finger,
                unit = "deg",
                connectedTo="",
                valueInit = NaN, 
                valueMin = -Inf, 
                valueMax = Inf))
                
                rootOutputs.appendRow(Connexion(hand+"_"+finger+"_pointing_vector",
                direction=Connexion.OUT,
                description = "Pointing vector of the "+hand+" "+finger,
                unit = "m",
                connectedTo="",
                valueInit = NaN, 
                valueMin = -Inf, 
                valueMax = Inf))
            
            rootOutputs.appendRow(Connexion(hand+"_hand_position",
            direction=Connexion.OUT,
                description = "Position of the "+hand+" hand",
                unit = "m",
                connectedTo="",
                valueInit = NaN, 
                valueMin = -Inf, 
                valueMax = Inf))
                
            rootOutputs.appendRow(Connexion(hand+"_hand_pitch",
            direction=Connexion.OUT,
                description = "Pitch angle of the "+hand+" hand",
                unit = "deg",
                connectedTo="",
                valueInit = NaN, 
                valueMin = -Inf, 
                valueMax = Inf))
                
            rootOutputs.appendRow(Connexion(hand+"_hand_yaw",
            direction=Connexion.OUT,
                description = "Yaw angle of the "+hand+" hand",
                unit = "deg",
                connectedTo="",
                valueInit = NaN, 
                valueMin = -Inf, 
                valueMax = Inf))
                
            rootOutputs.appendRow(Connexion(hand+"_hand_roll",
            direction=Connexion.OUT,
                description = "Roll angle of the "+hand+" hand",
                unit = "deg",
                connectedTo="",
                valueInit = NaN, 
                valueMin = -Inf, 
                valueMax = Inf))
                
            rootOutputs.appendRow(Connexion(hand+"_hand_normal_vector",
            direction=Connexion.OUT,
                description = "Normal vector of the "+hand+" hand",
                unit = "deg",
                connectedTo="",
                valueInit = NaN, 
                valueMin = -Inf, 
                valueMax = Inf))
                
    def start(self):
        # instanciate the leap motion
        self._leap = Leap.Controller()
        self.taskState = self.PROGRESS
        
    def deliverOutputs(self,channels):
        frame = self._leap.frame()
        
        # fingers
        for f in frame.fingers:
            if f.hand.is_left:
                hand = "left"
            if f.hand.is_right:
                hand = "right"
            if f.type == f.TYPE_THUMB:
                finger = "thumb"
            if f.type == f.TYPE_INDEX:
                finger = "index"
            if f.type == f.TYPE_MIDDLE:
                finger = "middle"
            if f.type == f.TYPE_RING:
                finger = "ring"
            if f.type == f.TYPE_PINKY:
                finger = "pinky"
            channels = self._outputs.setConnexion(hand+"_"+finger+"_tip_position",f.tip_position.to_float_array(),channels)
            channels = self._outputs.setConnexion(hand+"_"+finger+"_pitch",f.direction.pitch*180.0/pi,channels)
            channels = self._outputs.setConnexion(hand+"_"+finger+"_yaw",f.direction.yaw*180.0/pi,channels)
            channels = self._outputs.setConnexion(hand+"_"+finger+"_pointing_vector",f.direction.to_float_array(),channels)
      
        return channels
        
    def receiveInputs(self,channels):      
        return channels

    def writeConf(self):
        conf = Interface_.writeConf(self)
        conf["_inputs"] = {}
        conf["_outputs"] = {}
        return conf
        
    def readConf(self,conf):
        Interface_.readConf(self,conf)        
        