from numpy import *
import Block
from Connexion import *
import zmq
from threading import Thread
import Tools

class Poppy(Block.Block):
    """ this class describes a block """
    
    def __init__(self,IP = '127.0.0.1',port = '8080'):
        Block.Block.__init__(self)
        self.IP = IP
        self.port = port
        arti_list = ['head_y','head_z',
                     'abs_x','abs_y','abs_z','bust_y','bust_x',
                     'l_shoulder_y','l_shoulder_x','l_arm_z','l_elbow_y',
                     'r_shoulder_y','r_shoulder_x','r_arm_z','r_elbow_y',
                     'l_hip_x','l_hip_z','l_hip_y','l_knee_y','l_ankle_y',
                     'r_hip_x','r_hip_z','r_hip_y','r_knee_y','r_ankle_y',]
        input_list = ['goal_position','compliant','moving_speed']
        output_list = ['present_position','present_speed']
        
        for art in arti_list:
            self.inputs[art] = {}
            self.inputs[art]['goal_position'] = Connexion(default = 0.0)
            self.inputs[art]['compliant'] = Connexion(default = True)
            self.inputs[art]['moving_speed'] = Connexion(default = 0.0)
            self.outputs[art] = {}
            for output in output_list:
                self.outputs[art][output] = Connexion()
    
    def start(self):
        self.COM = clientThread(self.IP,self.port)
        self.COM.start()
        self.active = True
        
    def init(self):
        a=1
    
    def getInputs(self,f):
        r = {}
        r['name'] = []
        r['goal_position'] = []
        r['compliant'] = []
        r['moving_speed'] = []
        for art in self.inputs:
            r['name'].append(art)
            r['goal_position'].append(self.inputs[art]['goal_position'].getValue(f))
            r['compliant'].append(self.inputs[art]['compliant'].getValue(f))
            r['moving_speed'].append(self.inputs[art]['moving_speed'].getValue(f))
        self.COM._robotOut = r
        
    def setOutputs(self,f):
        r = self.COM._robotIn
        if len(r)>0:
            for i in range(len(r['name'])):
                art = r['name'][i]
                self.outputs[art]['present_position'].setValue(r['present_position'][i],f)
                self.outputs[art]['present_speed'].setValue(r['present_speed'][i],f)
        return f
        
class clientThread(Thread):
        
    def __init__(self,IP,port):
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
        