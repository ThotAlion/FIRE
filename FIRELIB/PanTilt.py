from Connexion import Connexion
from Interface import Interface
from numpy import *
import pypot.robot

class PanTilt(Interface):
    """Interface for pan-tilt robot"""
    
    def __init__(self,name = "pan-tilt turret",ID_head_z=16, ID_head_y=9):
        """constructor of pan tilt turret"""
        Interface.__init__(self,name=name)
        # name of the interface
        self._name = name
        # set the ID of the two servo
        self.ID_head_z = ID_head_z
        self.ID_head_y = ID_head_y
        
        # instanciate the robot
        config = {}
        config['controllers'] = {}
        config['controllers']['panTilt'] = {
        'port': 'auto',
        'sync_read': True,
        'attached_motors': ['head'],
        'protocol': 1
        }
        config['motorgroups'] = {}
        config['motorgroups']['head'] = ['head_z', 'head_y']
        config['motors'] = {}
        config['motors']['head_z'] = {
        'id': self.ID_head_z,
        'type': 'AX-12',
        'orientation': 'direct',
        'offset': 0.0,
        'angle_limit': (-90.0, 90.0),
        }
        config['motors']['head_y'] = {
        'id': self.ID_head_y,
        'type': 'AX-12',
        'orientation': 'direct',
        'offset': 0.0,
        'angle_limit': (-90.0, 90.0),
        }
        self._robot = pypot.robot.from_config(config)
        self._robot.start_sync()
        
        # list the interface of the Dynamixel motors
        # head_z
        for motor in ["head_z","head_y"]:
            m = getattr(self._robot,motor)
            self._outputs[motor+"_present_position"]=Connexion(direction=Connexion.OUT,
            description = "Position of servo "+motor,
            unit = "deg",
            connectedTo="",
            valueInit = 0.0, 
            valueMin = min(m.angle_limit), 
            valueMax = max(m.angle_limit))
            
            self._outputs[motor+"_present_torque"]=Connexion(direction=Connexion.OUT,
            description = "Torque applied on servo "+motor,
            unit = "%",
            connectedTo="",
            valueInit = 0.0, 
            valueMin = -100, 
            valueMax = 100)
            
            self._outputs[motor+"_present_speed"]=Connexion(direction=Connexion.OUT,
            description = "Speed of servo "+motor,
            unit = "deg/s",
            connectedTo="",
            valueInit = 0.0, 
            valueMin = -Inf, 
            valueMax = Inf)
            
            self._outputs[motor+"_present_temperature"]=Connexion(direction=Connexion.OUT,
            description = "Temperature of servo "+motor,
            unit = "degC",
            connectedTo="",
            valueInit = 0.0, 
            valueMin = -Inf, 
            valueMax = Inf)
            
            self._outputs[motor+"_present_voltage"]=Connexion(direction=Connexion.OUT,
            description = "Voltage of servo "+motor,
            unit = "V",
            connectedTo="",
            valueInit = 0.0, 
            valueMin = -Inf, 
            valueMax = Inf)
        
            self._inputs[motor+"_goal_position"]=Connexion(direction=Connexion.IN,
            description = "Goal position of servo "+motor,
            unit = "deg",
            connectedTo="",
            valueInit = 0.0, 
            valueMin = min(m.angle_limit), 
            valueMax = max(m.angle_limit))
            
            self._inputs[motor+"_max_speed"]=Connexion(direction=Connexion.IN,
            description = "Maximal speed of servo "+motor,
            unit = "deg/s",
            connectedTo="",
            valueInit = 0.0, 
            valueMin = -Inf, 
            valueMax = Inf)
        
        
    def deliverOutputs(self,channels):
        for motor in ["head_z","head_y"]:
            m = getattr(self._robot,motor)
            self._outputs[motor+"_present_position"].value = m.present_position
            if self._outputs[motor+"_present_position"].isConnected:
                self._outputs[motor+"_present_position"].updateOutput(channels)
                
            self._outputs[motor+"_present_torque"].value = m.present_load
            if self._outputs[motor+"_present_torque"].isConnected:
                self._outputs[motor+"_present_torque"].updateOutput(channels)
                
            self._outputs[motor+"_present_speed"].value = m.present_speed
            if self._outputs[motor+"_present_speed"].isConnected:
                self._outputs[motor+"_present_speed"].updateOutput(channels)
                
            self._outputs[motor+"_present_temperature"].value = m.present_temperature
            if self._outputs[motor+"_present_temperature"].isConnected:
                self._outputs[motor+"_present_temperature"].updateOutput(channels)
                
            self._outputs[motor+"_present_voltage"].value = m.present_voltage
            if self._outputs[motor+"_present_voltage"].isConnected:
                self._outputs[motor+"_present_voltage"].updateOutput(channels)
                
        return channels
        
    def receiveInputs(self,channels):
        
        for motor in ["head_z","head_y"]:
            m = getattr(self._robot,motor)
            if self._inputs[motor+"_goal_position"].isConnected:
                self._inputs[motor+"_goal_position"].updateInput(channels)
                if self._inputs[motor+"_goal_position"].value == NaN:
                    m.compliant = True
                else:
                    m.compliant = False
                    m.goal_position = self._inputs[motor+"_goal_position"].value
            else:
                m.compliant = True
            
            if self._inputs[motor+"_max_speed"].isConnected:
                self._inputs[motor+"_max_speed"].updateInput(channels)
                m.moving_speed = self._inputs[motor+"_max_speed"].value
            else:
                m.moving_speed = 0
                
        return channels
                    
        