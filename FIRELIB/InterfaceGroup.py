from Interface import Interface
import PanTilt,PypotCreature,LeapMotion

class InterfaceGroup(Interface):
    """Interface containing others interfaces"""
    
    def __init__(self,name = "Group"):
        """constructor of the interface"""
        Interface.__init__(self,name=name)
        self._isGroup = True
        self.executionState = self.NOTREADY
    
    def start(self):
        for i in range(self.rowCount()):
            if not self.child(i).executionState == self.child(i).RUNNING:
                self.child(i).start()
        self.executionState = self.READY
        
    def close(self):
        for i in range(self.rowCount()):
            if self.child(i).executionState == self.child(i).RUNNING:
                self.child(i).close()
        self.executionState = self.FINISHED
        
    def deliverOutputs(self,channels):
        for i in range(self.rowCount()):
            if self.child(i).executionState == self.child(i).RUNNING:
                channels = self.child(i).deliverOutputs(channels)
        return channels
        
        
    def receiveInputs(self,channels):
        for i in range(self.rowCount()):
            if self.child(i).executionState == self.child(i).RUNNING:
                self.child(i).receiveInputs(channels)
        return channels
        
    def writeConf(self):
        conf = Interface.writeConf(self)
        conf["children"] = []
        for i in range(self.rowCount()):
            int = self.child(i)
            conf["children"].append(int.writeConf())
        return conf
        
    def readConf(self,conf):
        Interface.readConf(self,conf)
        for a in conf["children"]:
            int = createInterface(a["name"])
            int.readConf(a)
            self.appendRow(int)
            
def createInterface(InterfaceType):
    if InterfaceType == "PanTilt":
        newitem = PanTilt.PanTilt()
    elif InterfaceType == "PypotCreature":
        newitem = PypotCreature.PypotCreature()
    elif InterfaceType == "LeapMotion":
        newitem = LeapMotion.LeapMotion()
    elif InterfaceType == "Group":
        newitem = InterfaceGroup.InterfaceGroup()
    else:
        newitem = None
    return newitem