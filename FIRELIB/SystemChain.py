from System import System
import Hub,Recorder

class SystemChain(System):
    """System containing a chain of systems. Each system will be executed one after another"""
    
    def __init__(self,name = "Chain"):
        """constructor of the System"""
        System.__init__(self,name=name)
        self._isGroup = True
        self._index = 0
        self.executionState = self.NOTREADY
    
    def start(self):
        for i in range(self.rowCount()):
            self.child(i).start()
        self.executionState = self.READY
        
        
    def init(self):
        self.child(0).init()
        self.child(0).executionState = self.child(0).RUNNING
        
        
    def close(self):
        for i in range(self.rowCount()):
            if self.child(i).executionState == self.child(i).RUNNING:
                self.child(i).close()
        self.executionState = self.FINISHED
        self.taskState = self.STOPPED
        
    def deliverOutputs(self,channels):
        if self.child(self._index).executionState == self.child(self._index).RUNNING:
            channels = self.child(self._index).deliverOutputs(channels)
        elif self.child(self._index).executionState == self.child(self._index).FINISHED:
            if self._index < self.rowCount()-1:
                self._index = self._index + 1
                self.child(self._index).init()
                self.child(self._index).executionState = self.child(self._index).RUNNING
            else:
                self.executionState = self.FINISHED
        return channels
       
    def writeConf(self):
        conf = System.writeConf(self)
        conf["children"] = []
        for i in range(self.rowCount()):
            sys = self.child(i)
            conf["children"].append(sys.writeConf())
        return conf
        
    def readConf(self,conf):
        System.readConf(self,conf)
        for a in conf["children"]:
            sys = createSystem(a["name"])
            sys.readConf(a)
            self.appendRow(sys)
            
def createSystem(SystemType):
    if SystemType == "Hub":
        newitem = Hub.Hub()
    elif SystemType == "Recorder":
        newitem = Recorder.Recorder()
    elif SystemType == "Chain":
        newitem = SystemChain()
    else:
        newitem = None
    return newitem