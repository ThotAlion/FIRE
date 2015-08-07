from Connexion import Connexion
from Interface import Interface
from numpy import *
import zmq
import time
from threading import Thread

class PypotCreature(Interface):
    """Interface for robot piloted by IP"""
    
    def __init__(self,name = "Pypot creature",IP = '127.0.0.1',port = '8080'):
        """constructor of Pypot creature"""
        Interface.__init__(self,name=name)
        # name of the interface
        self._name = name
        # set the IP address
        self._IP = IP
        self._port = port
        # setup temporary zmq context
        c = zmq.Context()
        s = c.socket(zmq.REQ)
        s.connect("tcp://"+self._IP+":"+self._port)
        
        # first request
        req = {"robot":{"get_all_register_values":{}}}
        s.send_json(req)
        robot = s.recv_json()
        s.close()

        for motor in robot:
            # get motor parameters
            # angle_limit
            angle_limit = robot[motor]["angle_limit"]
            # ID
            id = robot[motor]["id"]
            
            # list of outputs
            # present_position
            self._outputs[motor+" present_position"]=Connexion(direction=Connexion.OUT,
            description = "Present position of motor "+motor+"(ID:"+str(id)+")",
            unit = "deg",
            connectedTo="",
            valueInit = 0.0, 
            valueMin = -Inf, 
            valueMax = Inf)
            # present_load
            self._outputs[motor+" present_load"]=Connexion(direction=Connexion.OUT,
            description = "Present load of motor "+motor+"(ID:"+str(id)+")",
            unit = "%",
            connectedTo="",
            valueInit = 0.0, 
            valueMin = -Inf, 
            valueMax = Inf)
            # present_temperature
            self._outputs[motor+" present_temperature"]=Connexion(direction=Connexion.OUT,
            description = "Present temperature of motor "+motor+"(ID:"+str(id)+")",
            unit = "degC",
            connectedTo="",
            valueInit = 0.0, 
            valueMin = -Inf, 
            valueMax = Inf)
            # present_speed
            self._outputs[motor+" present_speed"]=Connexion(direction=Connexion.OUT,
            description = "Present speed of motor "+motor+"(ID:"+str(id)+")",
            unit = "deg/s",
            connectedTo="",
            valueInit = 0.0, 
            valueMin = -Inf, 
            valueMax = Inf)
            # present_voltage
            self._outputs[motor+" present_voltage"]=Connexion(direction=Connexion.OUT,
            description = "Present voltage of motor "+motor+"(ID:"+str(id)+")",
            unit = "V",
            connectedTo="",
            valueInit = 0.0, 
            valueMin = -Inf, 
            valueMax = Inf)
            
            # list of inputs
            # goal position
            self._inputs[motor+" goal_position"]=Connexion(direction=Connexion.IN,
            description = "Goal position of motor "+motor+"(ID:"+str(id)+")",
            unit = "deg",
            connectedTo="",
            valueInit = NaN, 
            valueMin = min(angle_limit), 
            valueMax = max(angle_limit))
            # moving speed
            self._inputs[motor+" moving_speed"]=Connexion(direction=Connexion.IN,
            description = "Maximal speed of motor "+motor+"(ID:"+str(id)+")",
            unit = "deg/s",
            connectedTo="",
            valueInit = 0, 
            valueMin = -Inf, 
            valueMax = Inf)
        self._clientThread = clientThread(self._IP,self._port)
        self._clientThread.start()

    def deliverOutputs(self,channels):
        robot = self._clientThread._robotIn
        for motor in robot:
            self._outputs[motor+" present_position"].value = robot[motor]["present_position"]
            self._outputs[motor+" present_load"].value = robot[motor]["present_load"]
            self._outputs[motor+" present_temperature"].value = robot[motor]["present_temperature"]
            self._outputs[motor+" present_speed"].value = robot[motor]["present_speed"]
            self._outputs[motor+" present_voltage"].value = robot[motor]["present_voltage"]
        
        for output in self._outputs:
                if self._outputs[output].isConnected:
                    channels = self._outputs[output].updateOutput(channels)
                
        return channels
        
    def receiveInputs(self,channels):
        robot = {}
        for input in self._inputs:
            if self._inputs[input].isConnected:
                self._inputs[input].updateInput(channels)
                motor,reg = input.split(" ")
                value = self._inputs[input].value
                if not robot.has_key(motor):
                    robot[motor] = {}
                if reg == "goal_position":
                    if isnan(value):
                        robot[motor]["compliant"] = True
                        robot[motor][reg] = 0.0
                    else:
                        robot[motor]["compliant"] = False
                        robot[motor][reg] = value[0]
                else:
                    robot[motor][reg] = value[0]
                
        self._clientThread._robotOut = robot
            
            
# define a class to manage IP communication with a Pypot creature            
class clientThread(Thread):
        
    def __init__(self,IP='127.0.0.1',port='8080'):
        # setup zmq context
        Thread.__init__(self)
        self._IP = IP
        self._port = port
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.REQ)
        self._socket.connect("tcp://"+self._IP+":"+self._port)
        self._robotIn = {}
        self._robotOut = {}
        self._active = True
        
    def run(self):
        while self._active:
            t0 = time.clock()
            req = {"robot":{"get_all_register_values":{}}}
            self._socket.send_json(req)
            self._robotIn = self._socket.recv_json()

            req = {"robot":{"set_all_register_values":{"dict":self._robotOut}}}
            self._socket.send_json(req)
            a = self._socket.recv_json()
            while time.clock()-t0<0.02:
                a=1
    def close(self):
        self._active = False
        time.sleep(0.5)
        self._socket.close()
        
                

    
    
        