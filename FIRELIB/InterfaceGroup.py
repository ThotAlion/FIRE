from Interface import Interface

class InterfaceGroup(Interface):
    """Interface containing others interfaces"""
    
    def __init__(self,name = "Group"):
        """constructor of the interface"""
        Interface.__init__(self,name)
        self._isGroup = True
    
    def start(self):
        # do nothing
        return
        