from numpy import *
import Block
from Connexion import *


class Mirror(Block.Block):
    """ this class describes a block to mirror in real-time a robot with respect to another """
    
    def __init__(self):
        Block.Block.__init__(self)
        self.transfer_table = {"head_z":"-head_z","head_y":"head_y",
        "l_shoulder_y":"r_shoulder_y","l_shoulder_x":"-r_shoulder_x","l_arm_z":"-r_arm_z","l_elbow_y":"r_elbow_y",'l_wrist_z':'-r_wrist_z','l_wrist_x':'-r_wrist_x',
        "r_shoulder_y":"l_shoulder_y","r_shoulder_x":"-l_shoulder_x","r_arm_z":"-l_arm_z","r_elbow_y":"l_elbow_y",'r_wrist_z':'-l_wrist_z','r_wrist_x':'-l_wrist_x',
        "l_hip_x":"-r_hip_x","l_hip_z":"-r_hip_z","l_hip_y":"r_hip_y","l_knee_y":"r_knee_y","l_ankle_y":"r_ankle_y",
        "r_hip_x":"-l_hip_x","r_hip_z":"-l_hip_z","r_hip_y":"l_hip_y","r_knee_y":"l_knee_y","r_ankle_y":"l_ankle_y",
        "abs_x":"-abs_x","abs_y":"abs_y","abs_z":"-abs_z","bust_y":"bust_y","bust_x":"-bust_x"}
        
        for art in self.transfer_table:
            self.inputs[art] = Connexion(default = NaN)
            self.outputs[art] = Connexion(default = 0)
        self.inputs["n"] = Connexion(default = NaN)
        self.outputs["n"] = Connexion(default = 0)
        self.inputs["Delta"] = Connexion(default = NaN)
        self.outputs["Delta"] = Connexion(default = 0)
            
        

    def start(self):
        a=1
        
    def init(self,f):
        return f
    
    def getInputs(self,f):
        a=1
        
    def setOutputs(self,f):
        for output in self.transfer_table:
            if self.transfer_table[output][0] == "-":
                link = self.transfer_table[output][1:]
                a = self.inputs[link].getValue(f)
                if a[0] == 'L' or a[0] == 'S':
                    val = a[1:]
                    if val[0] == "-":
                        val = val[1:]
                    else:
                        val = "-"+val
                    out = a[0]+val
                else:
                    out = a
            else:
                link = self.transfer_table[output]
                out = self.inputs[link].getValue(f)
            self.outputs[output].setValue(out,f)
        self.outputs["n"].setValue(self.inputs["n"].getValue(f),f)
        self.outputs["Delta"].setValue(self.inputs["Delta"].getValue(f),f)
        
        return f
           
    def close(self):
        a=1
        