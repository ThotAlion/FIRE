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
    
    def __init__(self,name = "PypotCreature",IP = '127.0.0.1',port = '8080'):
        """constructor of Pypot creature"""
        Interface.__init__(self,name=name)
        # set the IP address
        self._IP = IP
        self._port = port
        self.controlWidget = PypotControlWidget(self)
        self.configWidget = PypotConfigWidget(self)
        self.isCompliant = False
        self.isSlimy = False
        self.slimyThr = 30
        self.motornames = []
        self.executionState = self.NOTREADY
        
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
        self.motornames = robot["name"]
        self.motorhash = {}
        for i in range(len(self.motornames)):
            self.motorhash[self.motornames[i]]=i
        

        for i in range(len(robot["name"])):
            motor = robot["name"][i]
            # get motor parameters
            # angle_limit
            angle_limit = robot["angle_limit"][i]
            # ID
            id = robot["id"][i]
            
            rootOutputs.appendRow(Connexion(motor+" present_position",direction=Connexion.OUT,
            description = "Position of servo "+motor+" ID:"+str(id),
            unit = "deg",
            connectedTo="",
            valueInit = 0.0, 
            valueMin = -Inf, 
            valueMax = Inf))
            
            rootOutputs.appendRow(Connexion(motor+" present_load",direction=Connexion.OUT,
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
        self.executionState = self.NOTREADY
        
    
    def start(self):
        self._clientThread = clientThread(self._IP,self._port)
        self._clientThread.start()
        self.executionState = self.READY
        
    def close(self):
        self._clientThread.close()
        self.executionState = self.FINISHED
    
    def deliverOutputs(self,channels):
        robot = self._clientThread._robotIn
        for i in range(self._outputs.rowCount()):
            try:
                conn = self._outputs.item(i)
                conn_name = str(conn.text())
                motor,reg = conn_name.split(" ")
                imotor = self.motorhash[motor]
                conn.value = robot[reg][imotor]
                if conn.isConnected:
                    channels = conn.updateOutput(channels)
            except:
                pass
        return channels
        
    def receiveInputs(self,channels):
        nmotor = len(self.motornames)
        robot = {}
        robot["compliant"] = [True]*nmotor
        robot["goal_position"] = [0.0]*nmotor
        robot["moving_speed"] = [0.0]*nmotor
        robot["name"] = self.motornames
        if not self.isCompliant:
            for i in range(self._inputs.rowCount()):
                try:
                    conn = self._inputs.item(i)
                    if conn.isConnected:
                        conn.updateInput(channels)
                        conn_name = str(conn.text())
                        motor,reg = conn_name.split(" ")
                        imotor = self.motorhash[motor]
                        if reg == "goal_position":
                            if isnan(conn.value[0]):
                                robot["goal_position"][imotor] = 0.0
                                robot["compliant"][imotor] = True
                            else:
                                robot["goal_position"][imotor] = conn.value[0]
                                robot["compliant"][imotor] = False
                        else:
                            robot[reg][imotor] = conn.value[0]
                except:
                    pass
        self._clientThread._robotOut = robot
        
    def writeConf(self):
        conf = Interface.writeConf(self)
        conf["IP"] = self._IP
        conf["port"] = self._port
        return conf
        
    def readConf(self,conf):
        Interface.readConf(self,conf)
        self._IP = conf["IP"]
        self._port = conf["port"]
    

            
            
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
                      

    
    
        