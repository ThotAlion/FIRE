

class pose(Object):
    """ this class describes a pose during a choregraphy """
    
    def __init__(self,duration = 100,objectives = {}):
        self.duration = duration
        self.objectives = objectives
        self.isActive = False
        self.localTime = 0.0
    
    
    
    def run(self):
        for obj in self.objectives