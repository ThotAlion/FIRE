from PyQt4.QtGui import *
from PyQt4.QtCore import *
from Connexion import Connexion
from Interface import Interface as Interface_
from numpy import *
import pypot.robot

class PanTilt(Interface_):
    """Interface for pan-tilt robot"""
    
    def __init__(self,name = "PanTilt",ID_head_z=16, ID_head_y=9):
        """constructor of pan tilt turret"""
        Interface_.__init__(self,name=name,icon=QIcon("FIRELIB/icons/pantilt.png"))
        # set the ID of the two servo
        self.ID_head_z = ID_head_z
        self.ID_head_y = ID_head_y
        
        # instanciate the robot
        self.config = {}
        self.config['controllers'] = {}
        self.config['controllers']['panTilt'] = {
        'port': 'auto',
        'sync_read': True,
        'attached_motors': ['head'],
        'protocol': 1
        }
        self.config['motorgroups'] = {}
        self.config['motorgroups']['head'] = ['head_z', 'head_y']
        self.config['motors'] = {}
        self.config['motors']['head_z'] = {
        'id': self.ID_head_z,
        'type': 'AX-12',
        'orientation': 'direct',
        'offset': 0.0,
        'angle_limit': (-90.0, 90.0),
        }
        self.config['motors']['head_y'] = {
        'id': self.ID_head_y,
        'type': 'AX-12',
        'orientation': 'direct',
        'offset': 0.0,
        'angle_limit': (-120.0, 120.0),
        }
        
        
        # list the interface of the Dynamixel motors
        # head_z
        rootInputs = self._inputs.invisibleRootItem()
        rootOutputs = self._outputs.invisibleRootItem()
        for motor in ["head_z","head_y"]:
            rootOutputs.appendRow(Connexion(motor+"_present_position",direction=Connexion.OUT,
            description = "Position of servo "+motor,
            unit = "deg",
            connectedTo="",
            valueInit = 0.0, 
            valueMin = -Inf, 
            valueMax = Inf))
            
            rootOutputs.appendRow(Connexion(motor+"_present_torque",direction=Connexion.OUT,
            description = "Torque applied on servo "+motor,
            unit = "%",
            connectedTo="",
            valueInit = 0.0, 
            valueMin = -100, 
            valueMax = 100))
            
            rootOutputs.appendRow(Connexion(motor+"_present_speed",direction=Connexion.OUT,
            description = "Speed of servo "+motor,
            unit = "deg/s",
            connectedTo="",
            valueInit = 0.0, 
            valueMin = -Inf, 
            valueMax = Inf))
            
            rootOutputs.appendRow(Connexion(motor+"_present_temperature",direction=Connexion.OUT,
            description = "Temperature of servo "+motor,
            unit = "degC",
            connectedTo="",
            valueInit = 0.0, 
            valueMin = 0, 
            valueMax = Inf))
            
            rootOutputs.appendRow(Connexion(motor+"_present_voltage",direction=Connexion.OUT,
            description = "Voltage of servo "+motor,
            unit = "V",
            connectedTo="",
            valueInit = 0.0, 
            valueMin = 0, 
            valueMax = Inf))
        
            rootInputs.appendRow(Connexion(motor+"_goal_position",direction=Connexion.IN,
            description = "Goal position of servo "+motor,
            unit = "deg",
            connectedTo="",
            valueInit = NaN, 
            valueMin = self.config['motors'][motor]['angle_limit'][0], 
            valueMax = self.config['motors'][motor]['angle_limit'][1]))
            
            rootInputs.appendRow(Connexion(motor+"_max_speed",direction=Connexion.IN,
            description = "Maximal speed of servo "+motor,
            unit = "deg/s",
            connectedTo="",
            valueInit = 0.0, 
            valueMin = 0, 
            valueMax = Inf))
        self.executionState = self.READY
        self.taskState = self.STOPPED
    
    def start(self):
        self._robot = pypot.robot.from_config(self.config)
        self._robot.start_sync()
        self.executionState = self.RUNNING
        self.taskState = self.PROGRESS
        
            
    def close(self):
        self._robot.close()
        self.executionState = self.READY
        self.taskState = self.STOPPED
        
    def deliverOutputs(self,channels):
        for motor in ["head_z","head_y"]:
            m = getattr(self._robot,motor)
            channels = self._outputs.setConnexion(motor+"_present_position",m.present_position,channels)
            channels = self._outputs.setConnexion(motor+"_present_torque",m.present_load,channels)
            channels = self._outputs.setConnexion(motor+"_present_speed",m.present_speed,channels)
            channels = self._outputs.setConnexion(motor+"_present_temperature",m.present_temperature,channels)
            channels = self._outputs.setConnexion(motor+"_present_voltage",m.present_voltage,channels)

        return channels
        
        
    def receiveInputs(self,channels):
        
        for motor in ["head_z","head_y"]:
            m = getattr(self._robot,motor)
            
            goal = self._inputs.getConnexion(motor+"_goal_position",channels)
            if not goal is None:
                if isnan(goal):
                    m.compliant = True
                else:
                    m.compliant = False
                    m.goal_position = goal
            else:
                m.compliant = True
                
            maxSpeed = self._inputs.getConnexion(motor+"_max_speed",channels)
            if not maxSpeed is None:
                m.moving_speed = maxSpeed
            else:
                m.moving_speed = 0
                
        return channels
        
    def writeConf(self):
        conf = Interface_.writeConf(self)
        conf["ID_head_z"] = self.ID_head_z
        conf["ID_head_y"] = self.ID_head_y
        return conf
        
    def readConf(self,conf):
        Interface_.readConf(self,conf)
        self.ID_head_z = conf["ID_head_z"]
        self.ID_head_y = conf["ID_head_y"]
                    
class PanTiltWidget(QWidget):
    
    def __init__(self,parent):
        QWidget.__init__(self,parent)
        
        
        # list of components
        self.wIDhead_z = QSpinBox()
        self.wIDhead_y = QSpinBox()
        self.wLabelhead_z = QLabel("ID of motor around z axis:")
        self.wLabelhead_y = QLabel("ID of motor around y axis:")
        self.wCOMPort = QLabel("Not Connected")
        
        
        # widget setup
        self.mainlayout = QVBoxLayout(self)
        self.mainlayout.addWidget(self.wAddConnexion)
        self.mainlayout.addWidget(self.wRemoveConnexion)
        self.mainlayout.addWidget(self.wComboConnexion)
        
        # connect the signals
        self.connect(self.wAddConnexion,SIGNAL("pressed()"),parent.addConnexion)       