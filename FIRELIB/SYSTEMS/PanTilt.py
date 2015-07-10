import System
import ..Connexion
import pypot.robot

class PanTilt(System.Sytem):
    """Class concerning a particular pypot robot which is a pan-tilt turret. The first motor is along Z axis, the second along Y axis"""
    
    def __init__(self,name="PanTilt"):
        self = System.Sytem.__init__(self,name=name)
        # list of Inputs
        self.inputs.append(Connexion.Connexion(type=Connexion.IN,
        name="u head z",
        description="Commanded position along Z axis.",
        unit="deg",
        valueInit=0.0,
        valueMin=-90.0,
        valueMax=90.0))
        
        self.inputs.append(Connexion.Connexion(type=Connexion.IN,
        name="u head y",
        description="Commanded position along Y axis.",
        unit="deg",
        valueInit=0.0,
        valueMin=-90.0,
        valueMax=90.0))
        
        # list of Outputs
        self.outputs.append(Connexion.Connexion(type=Connexion.OUT,
        name="q head z",
        description="Angular position along Z axis.",
        unit="deg",
        valueInit=0.0,
        valueMin=-90.0,
        valueMax=90.0))
        
        self.outputs.append(Connexion.Connexion(type=Connexion.OUT,
        name="q head y",
        description="Angular position along Y axis.",
        unit="deg",
        valueInit=0.0,
        valueMin=-90.0,
        valueMax=90.0))
        
        # starting the pypot robot
        config = {}
        config['controllers'] = {}
        config['controllers']['panTilt'] = {
        'port': 'auto',
        'sync_read': True,
        'attached_motors': ['head_z', 'head_y'],
        'protocol': 1
        }
        config['motors'] = {}
        config['motors']['head_z'] = {
        'id': 16,
        'type': 'AX-12',
        'orientation': 'direct',
        'offset': 0.0,
        'angle_limit': (-90.0, 90.0),
        }
        config['motors']['head_y'] = {
        'id': 9,
        'type': 'AX-12',
        'orientation': 'direct',
        'offset': 0.0,
        'angle_limit': (-90.0, 90.0),
        }
        self._robot = pypot.robot.from_config(config)
        
    def read_inputs(self,f):
        for i in self.inputs:
            if f.has_key(i.connectedTo):
                i.value = f[i.connectedTo]
    
    def write_outputs(self,f)
        for o in self.outputs:
            if f.has_key(o.connectedTo):
                f[o.connectedTo] = o.value
        return f