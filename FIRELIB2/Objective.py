

class Objective(Object):
    """ this class describes an objective and a resolution 
    type : can be 'motor' (can be extended later)
    name : name of the motor
    command : can be 'mou','pmou','linear','start_spline','end_spline','spline'
    parameter : number to parametrize the trajectory
    consign : goal to achieve
    speed : maximal speed of the actuator
    """
    
    def __init__(self,type = 'motor',name,command,parameter,consign,speed):
        self.type = type
        self.name = name
        self.command = command
        self.parameter = parameter
        self.consign = consign
        self.speed = speed
    
    def setInit(self,x0):
        self.initCond = x0
    
    def getCommand(self,state):
        """ this method gets the consign of the motor for the specified time """
        command = {}
        if self.type == 'motor':
            if self.command == 'mou':
                command["goal_position"] = state["present_position"]
                command["compliant"] = True
                command["moving_speed"] = self.speed
            elif self.command == 'pmou':
                command["goal_position"] = state["present_position"]
                command["compliant"] = False
                command["moving_speed"] = self.speed
            elif self.command == 'linear':
                rt = state["rtime"]
                x0 = self.initCond
                command["goal_position"] = x0+rt*(self.consign-x0)
                command["compliant"] = False
                command["moving_speed"] = self.speed
            elif self.command == 'start_spline':
                rt = state["rtime"]
                delta = (self.consign-self.initCond)
                a = delta
                command["goal_position"] = self.initCond+rt*rt*a
                command["compliant"] = False
                command["moving_speed"] = self.speed
            elif self.command == 'end_spline':
                rt = state["rtime"]
                delta = (self.consign-self.initCond)
                a = -delta
                b = 2*delta
                command["goal_position"] = self.initCond+a*rt*rt+b*rt
                command["compliant"] = False
                command["moving_speed"] = self.speed
            elif self.command == 'spline':
                rt = state["rtime"]
                x0 = state["initCond"]
                delta = (self.consign-self.initCond)
                a = -2*delta
                b = 3*delta
                command["goal_position"] = self.initCond+a*rt*rt*rt+b*rt*rt
                command["compliant"] = False
                command["moving_speed"] = self.speed
        
        return command