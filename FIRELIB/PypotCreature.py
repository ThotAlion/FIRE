from Connexion import Connexion
from Interface import Interface
from numpy import *
import zmq
import Tools
import time
from threading import Thread
from PyQt4.QtGui import *
from PyQt4.QtCore import *

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
        self.controlWidget = PypotControlWidget(self)
        self.configWidget = PypotConfigWidget(self)
        self.isCompliant = False
        self.isSlimy = False
        self.slimyThr = 30
        self.motornames = []
        
    def identify(self):
        rootInputs = self._inputs.invisibleRootItem()
        rootOutputs = self._outputs.invisibleRootItem()
        
        
        
        # setup temporary zmq context
        c = zmq.Context()
        s = c.socket(zmq.REQ)
        s.connect("tcp://"+self._IP+":"+self._port)
        
        # first request
        req = {"robot":{"get_all_register_values":{}}}
        s.send_json(req)
        robot = s.recv_json()
        s.close()
        self.motornames = robot.keys()

        for motor in robot:
            # get motor parameters
            # angle_limit
            angle_limit = robot[motor]["angle_limit"]
            # ID
            id = robot[motor]["id"]
            
            rootOutputs.appendRow(Connexion(motor+" present_position",direction=Connexion.OUT,
            description = "Position of servo "+motor+" ID:"+str(id),
            unit = "deg",
            connectedTo="",
            valueInit = 0.0, 
            valueMin = -Inf, 
            valueMax = Inf))
            
            rootOutputs.appendRow(Connexion(motor+" present_torque",direction=Connexion.OUT,
            description = "Torque applied on servo "+motor+" ID:"+str(id),
            unit = "%",
            connectedTo="",
            valueInit = 0.0, 
            valueMin = -100, 
            valueMax = 100))
            
            rootOutputs.appendRow(Connexion(motor+" present_speed",direction=Connexion.OUT,
            description = "Speed of servo "+motor+" ID:"+str(id),
            unit = "deg/s",
            connectedTo="",
            valueInit = 0.0, 
            valueMin = -Inf, 
            valueMax = Inf))
            
            rootOutputs.appendRow(Connexion(motor+" present_temperature",direction=Connexion.OUT,
            description = "Temperature of servo "+motor+" ID:"+str(id),
            unit = "degC",
            connectedTo="",
            valueInit = 0.0, 
            valueMin = 0, 
            valueMax = Inf))
            
            rootOutputs.appendRow(Connexion(motor+" present_voltage",direction=Connexion.OUT,
            description = "Voltage of servo "+motor+" ID:"+str(id),
            unit = "V",
            connectedTo="",
            valueInit = 0.0, 
            valueMin = 0, 
            valueMax = Inf))
            
            rootOutputs.appendRow(Connexion(motor+" present_goal",direction=Connexion.OUT,
            description = "Command of servo "+motor+" ID:"+str(id),
            unit = "deg",
            connectedTo="",
            valueInit = 0.0, 
            valueMin = -Inf, 
            valueMax = Inf))
        
            rootInputs.appendRow(Connexion(motor+" goal_position",direction=Connexion.IN,
            description = "Goal position of servo "+motor+" ID:"+str(id),
            unit = "deg",
            connectedTo="",
            valueInit = NaN, 
            valueMin = min(angle_limit), 
            valueMax = max(angle_limit)))
            
            rootInputs.appendRow(Connexion(motor+" moving_speed",direction=Connexion.IN,
            description = "Maximal speed of servo "+motor+" ID:"+str(id),
            unit = "deg/s",
            connectedTo="",
            valueInit = 0.0, 
            valueMin = 0, 
            valueMax = Inf))
        self.executionState = self.READY
        self.taskState = self.STOPPED
        
    
    def start(self):
        self._clientThread = clientThread(self._IP,self._port)
        self._clientThread.start()
        self.taskState = self.PROGRESS
        
    def close(self):
        self._clientThread.close()
        self.executionState = self.READY
        self.taskState = self.STOPPED
    
    def deliverOutputs(self,channels):
        robot = self._clientThread._robotIn
        for motor in robot:
            channels = self._outputs.setConnexion(motor+" present_position",robot[motor]["present_position"],channels)
            channels = self._outputs.setConnexion(motor+" present_torque",robot[motor]["present_load"],channels)
            channels = self._outputs.setConnexion(motor+" present_temperature",robot[motor]["present_temperature"],channels)
            channels = self._outputs.setConnexion(motor+" present_speed",robot[motor]["present_speed"],channels)
            channels = self._outputs.setConnexion(motor+" present_voltage",robot[motor]["present_voltage"],channels)
            channels = self._outputs.setConnexion(motor+" present_goal",robot[motor]["goal_position"],channels)

        return channels
        
    def receiveInputs(self,channels):
        robot = {}
        for motor in self.motornames:
            goal = self._inputs.getConnexion(motor+" goal_position",channels)
            maxspeed = self._inputs.getConnexion(motor+" moving_speed",channels)
            torque = self._inputs.getConnexion(motor+" present_torque",channels)
            pos = self._inputs.getConnexion(motor+" present_position",channels)
            present_goal = self._inputs.getConnexion(motor+" present_goal",channels)
            if not robot.has_key(motor):
                robot[motor] = {}
            if self.isCompliant:
                robot[motor]["compliant"] = True
            elif self.isSlimy:
                if abs(torque)>self.slimyThr:
                    robot[motor]["compliant"] = False
                    robot[motor]["goal_position"] = pos
                else:
                    robot[motor]["compliant"] = False
                    robot[motor]["goal_position"] = present_goal
            else:
                if isnan(goal):
                    robot[motor]["compliant"] = True
                    robot[motor]["goal_position"] = 0.0
                else:
                    robot[motor]["compliant"] = False
                    robot[motor]["goal_position"] = goal[0]
            robot[motor]["moving_speed"] = maxspeed[0]
                
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
            t0 = Tools.getTime()
            req = {"robot":{"get_all_register_values":{}}}
            self._socket.send_json(req)
            self._robotIn = self._socket.recv_json()

            req = {"robot":{"set_all_register_values":{"dict":self._robotOut}}}
            self._socket.send_json(req)
            a = self._socket.recv_json()
            t1 = Tools.getTime()
            #print t1-t0
            while Tools.getTime()-t0<0.02:
                a=1
    def close(self):
        self._active = False
        time.sleep(0.5)
        self._socket.close()
        
class PypotConfigWidget(QWidget):
    
    def __init__(self,parent):
        QWidget.__init__(self)
        self.parent = parent
        # list of component :
        self.wLabelTitle = QLabel("System : Pypot Creature by IP")
        self.IPLabel = QLabel("IP adress of the robot :")
        self.PortLabel = QLabel("Port of the server :")
        self.IPEdit = QLineEdit("127.0.0.1")
        self.PortEdit = QLineEdit("8080")
        self.identifyButton = QPushButton("Clear and identify the robot")
        
        # widget setup
        self.setFixedSize(300,200)
        self.mainlayout = QVBoxLayout(self)
        self.IPLayout = QHBoxLayout()
        self.IPLayout.addWidget(self.IPLabel)
        self.IPLayout.addWidget(self.IPEdit)
        self.PortLayout = QHBoxLayout()
        self.PortLayout.addWidget(self.PortLabel)
        self.PortLayout.addWidget(self.PortEdit)
        self.mainlayout.addWidget(self.wLabelTitle)
        self.mainlayout.addLayout(self.IPLayout)
        self.mainlayout.addLayout(self.PortLayout)
        self.mainlayout.addWidget(self.identifyButton)
        
        # connect the signals
        self.connect(self.IPEdit,SIGNAL("editingFinished()"),self.setIP)
        self.connect(self.PortEdit,SIGNAL("editingFinished()"),self.setPort)
        self.connect(self.identifyButton,SIGNAL("pressed()"),self.parent.identify)
        
    def setIP(self):
        ip = str(self.IPEdit.text())
        self.parent._IP = ip
        
    def setPort(self):
        port = str(self.PortEdit.text())
        self.parent._Port = port
            
class PypotControlWidget(QWidget):
    
    def __init__(self,parent):
        QWidget.__init__(self)
        self.parent = parent
        # list of component :
        self.wLabelTitle = QLabel("System : Pypot Creature by IP")
        self.compliantButton = QCheckBox("Completely compliant")
        self.slimyButton = QCheckBox("Slimy")
        
        # widget setup
        self.setFixedSize(300,100)
        self.mainlayout = QVBoxLayout(self)
        self.mainlayout.addWidget(self.wLabelTitle)
        self.mainlayout.addWidget(self.compliantButton)
        self.mainlayout.addWidget(self.slimyButton)
        
        # connect the signals
        self.connect(self.compliantButton,SIGNAL("stateChanged(int)"),self.setCompliant)
        self.connect(self.slimyButton,SIGNAL("stateChanged(int)"),self.setSlimy)
        
    def setCompliant(self,val):
        if val == Qt.Checked:
            self.parent.isCompliant = True
        else:
            self.parent.isCompliant = False
        
    def setSlimy(self,val):
        if val == Qt.Checked:
            self.parent.isSlimy = True
        else:
            self.parent.isSlimy = False
                      

    
    
        