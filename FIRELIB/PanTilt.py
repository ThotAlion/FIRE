from Connexion import Connexion
from Interface import Interface
from numpy import *
import pypot.robot

class PanTilt(Interface):
    """Interface for pan-tilt robot"""
    
    def __init__(self,name = "pan-tilt turret",ID_head_z=16, ID_head_y=9):
        """constructor of pan tilt turret"""
        Interface.__init__(self,name=name)
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
        'angle_limit': (-90.0, 90.0),
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
            valueMin = -90, 
            valueMax = 90))
            
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
            valueMin = -Inf, 
            valueMax = Inf))
            
            rootOutputs.appendRow(Connexion(motor+"_present_voltage",direction=Connexion.OUT,
            description = "Voltage of servo "+motor,
            unit = "V",
            connectedTo="",
            valueInit = 0.0, 
            valueMin = -Inf, 
            valueMax = Inf))
        
            rootInputs.appendRow(Connexion(motor+"_goal_position",direction=Connexion.IN,
            description = "Goal position of servo "+motor,
            unit = "deg",
            connectedTo="",
            valueInit = NaN, 
            valueMin = -90, 
            valueMax = 90))
            
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
            self._outputs.findItems(motor+"_present_position")[0].value = m.present_position
            self._outputs.findItems(motor+"_present_torque")[0].value = m.present_load
            self._outputs.findItems(motor+"_present_speed")[0].value = m.present_speed
            self._outputs.findItems(motor+"_present_temperature")[0].value = m.present_temperature
            self._outputs.findItems(motor+"_present_voltage")[0].value = m.present_voltage
            
            # update the outputs
            for i in range(self._outputs.rowCount()):
                channels = self._outputs.item(i).updateOutput(channels)

        return channels
        
    def receiveInputs(self,channels):
        
        for motor in ["head_z","head_y"]:
            m = getattr(self._robot,motor)
            
            if self._inputs.findItems(motor+"_goal_position")[0].isConnected:
                self._inputs.findItems(motor+"_goal_position")[0].updateInput(channels)
                if isnan(self._inputs.findItems(motor+"_goal_position")[0].value):
                    m.compliant = True
                else:
                    m.compliant = False
                    m.goal_position = self._inputs.findItems(motor+"_goal_position")[0].value
            else:
                m.compliant = True
            
            if self._inputs.findItems(motor+"_max_speed")[0].isConnected:
                self._inputs.findItems(motor+"_max_speed")[0].updateInput(channels)
                m.moving_speed = self._inputs.findItems(motor+"_max_speed")[0].value
            else:
                m.moving_speed = 0
                
        return channels
                    
        