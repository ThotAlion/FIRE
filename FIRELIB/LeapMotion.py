from Connexion import Connexion
from Interface import Interface
from numpy import *
import Leap

class LeapMotion(Interface):
    """Interface for Leap-Motion device"""
    
    def __init__(self,name = "Leap-Motion"):
        """constructor of LeapMotion"""
        Interface.__init__(self,name=name)
        
        # instanciate the leap motion
        self._leap = Leap.Controller()
        
        # list the interface of the Dynamixel motors
        # head_z
        for hand in ["right","left"]:
            for finger in ["thumb","index","middle","ring","pinky"]:
                
                self._outputs[hand+"_"+finger+"_tip_position"]=Connexion(direction=Connexion.OUT,
                description = "Position of the "+hand+" "+finger,
                unit = "m",
                connectedTo="",
                valueInit = NaN, 
                valueMin = -Inf, 
                valueMax = Inf)
                
                self._outputs[hand+"_"+finger+"_pitch"]=Connexion(direction=Connexion.OUT,
                description = "Pitch angle of the "+hand+" "+finger,
                unit = "deg",
                connectedTo="",
                valueInit = NaN, 
                valueMin = -Inf, 
                valueMax = Inf)
                
                self._outputs[hand+"_"+finger+"_yaw"]=Connexion(direction=Connexion.OUT,
                description = "Yaw angle of the "+hand+" "+finger,
                unit = "deg",
                connectedTo="",
                valueInit = NaN, 
                valueMin = -Inf, 
                valueMax = Inf)
                
                self._outputs[hand+"_"+finger+"_pointing_vector"]=Connexion(direction=Connexion.OUT,
                description = "Pointing vector of the "+hand+" "+finger,
                unit = "m",
                connectedTo="",
                valueInit = NaN, 
                valueMin = -Inf, 
                valueMax = Inf)
            
            self._outputs[hand+"_hand_position"]=Connexion(direction=Connexion.OUT,
                description = "Position of the "+hand+" hand",
                unit = "m",
                connectedTo="",
                valueInit = NaN, 
                valueMin = -Inf, 
                valueMax = Inf)
                
            self._outputs[hand+"_hand_pitch"]=Connexion(direction=Connexion.OUT,
                description = "Pitch angle of the "+hand+" hand",
                unit = "deg",
                connectedTo="",
                valueInit = NaN, 
                valueMin = -Inf, 
                valueMax = Inf)
                
            self._outputs[hand+"_hand_yaw"]=Connexion(direction=Connexion.OUT,
                description = "Yaw angle of the "+hand+" hand",
                unit = "deg",
                connectedTo="",
                valueInit = NaN, 
                valueMin = -Inf, 
                valueMax = Inf)
                
            self._outputs[hand+"_hand_roll"]=Connexion(direction=Connexion.OUT,
                description = "Roll angle of the "+hand+" hand",
                unit = "deg",
                connectedTo="",
                valueInit = NaN, 
                valueMin = -Inf, 
                valueMax = Inf)
                
            self._outputs[hand+"_hand_normal_vector"]=Connexion(direction=Connexion.OUT,
                description = "Normal vector of the "+hand+" hand",
                unit = "deg",
                connectedTo="",
                valueInit = NaN, 
                valueMin = -Inf, 
                valueMax = Inf)
                
                
        
    def deliverOutputs(self,channels):
        frame = self._leap.frame()
        # by default, all is NaN
        for o in self._outputs:
            self._outputs[o] = NaN
        
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
            self._outputs[hand+"_"+finger+"_tip_position"].value = f.tip_position.to_float_array()*0.001
            self._outputs[hand+"_"+finger+"_pitch"].value = f.direction.pitch*180/pi
            self._outputs[hand+"_"+finger+"_yaw"].value = f.direction.yaw*180/pi
            self._outputs[hand+"_"+finger+"_pointing_vector"].value = f.direction.to_float_array()*0.001
      
        return channels
        
    def receiveInputs(self,channels):      
        return channels
                    
        