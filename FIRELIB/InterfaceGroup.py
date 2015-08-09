from Interface import Interface

class InterfaceGroup(Interface):
    """Interface containing others interfaces"""
    
    def __init__(self,parent=None,name = "group"):
        """constructor of the interface"""
        Interface.__init__(self,parent,name)
        self.children = []
    
    def start(self):
        # do nothing
        return
    
    def addInterface(self,interface):
        self.children.append(interface)
        
    def insertInterface(self,i,interface):
        self.children.insert(i,interface)
        
    def removeInterface(self,i):
        self.children.remove(i)
        