from Interface_ import Interface_

class InterfaceGroup(Interface_):
    """Interface containing others interfaces"""
    
    def __init__(self,name = "Group"):
        """constructor of the interface"""
        Interface_.__init__(self,name=name)
        self._isGroup = True
    
    def start(self):
        for i in range(self.rowCount()):
            if not self.child(i).executionState == self.child(i).RUNNING:
                self.child(i).start()
        self.executionState = self.RUNNING
        self.taskState = self.PROGRESS
        
    def close(self):
        for i in range(self.rowCount()):
            if self.child(i).executionState == self.child(i).RUNNING:
                self.child(i).close()
        self.executionState = self.READY
        self.taskState = self.STOPPED
        
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
        conf = Interface_.writeConf(self)
        return conf
        
    def readConf(self,conf):
        Interface_.readConf(self,conf)