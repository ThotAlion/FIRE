from numpy import *
import Block
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from Connexion import *
import zmq
from threading import Thread
import Tools
import time

class Poppy(Block.Block,QWidget):
    """ this class describes a block """
    
    def __init__(self,IP = '127.0.0.1',port = '8080'):
        Block.Block.__init__(self)
        QWidget.__init__(self)
        self.IP = IP
        self.port = port
        arti_list = ['head_y','head_z',
                     'abs_x','abs_y','abs_z','bust_y','bust_x',
                     'l_shoulder_y','l_shoulder_x','l_arm_z','l_elbow_y',
                     'r_shoulder_y','r_shoulder_x','r_arm_z','r_elbow_y',
                     'l_hip_x','l_hip_z','l_hip_y','l_knee_y','l_ankle_y',
                     'r_hip_x','r_hip_z','r_hip_y','r_knee_y','r_ankle_y',
                     'r_wrist_z','r_wrist_x','l_wrist_z','l_wrist_x']
        input_list = ['goal_position','compliant','moving_speed']
        output_list = ['present_position','present_speed']
        
        for art in arti_list:
            self.inputs[art] = {}
            self.inputs[art]['goal_position'] = Connexion(default = NaN)
            self.inputs[art]['moving_speed'] = Connexion(default = 0.0)
            self.outputs[art] = {}
            for output in output_list:
                self.outputs[art][output] = Connexion()
        # creation of components
        self.allMou = QCheckBox("Force All mou")
        self.torsoMou = QCheckBox("Force torso mou")
        self.absMou = QCheckBox("Force abdomen mou")
        self.headMou = QCheckBox("Force head mou")
        self.rLegMou = QCheckBox("Force right leg mou")
        self.lLegMou = QCheckBox("Force left leg mou")
        self.rArmMou = QCheckBox("Force right arm mou")
        self.lArmMou = QCheckBox("Force left arm mou")
        self.tempLabel = QLabel("Max Temp : 0deg")
        self.voltLabel = QLabel("Min Voltage : 0V")
        
        # composition
        mainlayout = QVBoxLayout(self)
        mainlayout.addWidget(self.allMou)
        mainlayout.addWidget(self.torsoMou)
        mainlayout.addWidget(self.absMou)
        mainlayout.addWidget(self.headMou)
        mainlayout.addWidget(self.rLegMou)
        mainlayout.addWidget(self.lLegMou)
        mainlayout.addWidget(self.rArmMou)
        mainlayout.addWidget(self.lArmMou)
        mainlayout.addWidget(self.tempLabel)
        mainlayout.addWidget(self.voltLabel)
        
        # signals
        self.connect(self.allMou,SIGNAL("toggled(bool)"),self.torsoMou,SLOT("setChecked(bool)"))
        self.connect(self.allMou,SIGNAL("toggled(bool)"),self.absMou,SLOT("setChecked(bool)"))
        self.connect(self.allMou,SIGNAL("toggled(bool)"),self.headMou,SLOT("setChecked(bool)"))
        self.connect(self.allMou,SIGNAL("toggled(bool)"),self.rLegMou,SLOT("setChecked(bool)"))
        self.connect(self.allMou,SIGNAL("toggled(bool)"),self.lLegMou,SLOT("setChecked(bool)"))
        self.connect(self.allMou,SIGNAL("toggled(bool)"),self.rArmMou,SLOT("setChecked(bool)"))
        self.connect(self.allMou,SIGNAL("toggled(bool)"),self.lArmMou,SLOT("setChecked(bool)"))
        
        self.show()
        
    
    def start(self):
        self.COM = clientThread(self.IP,self.port)
        self.COM.start()
        
    def init(self,f):
        return f
    
    def getInputs(self,f):
        r = {}
        r['name'] = []
        r['goal_position'] = []
        r['compliant'] = []
        r['moving_speed'] = []
        for art in self.inputs:
            r['name'].append(art)
            a = self.inputs[art]['goal_position'].getValue(f)
            if isnan(a) or \
                (art in ['head_y','head_z'] and self.headMou.isChecked()) or \
                (art in ['bust_y','bust_x'] and self.torsoMou.isChecked()) or \
                (art in ['abs_x','abs_y','abs_z'] and self.absMou.isChecked()) or \
                (art in ['l_shoulder_y','l_shoulder_x','l_arm_z','l_elbow_y','l_wrist_z','l_wrist_x'] and self.lArmMou.isChecked()) or \
                (art in ['r_shoulder_y','r_shoulder_x','r_arm_z','r_elbow_y','r_wrist_z','r_wrist_x'] and self.rArmMou.isChecked()) or \
                (art in ['l_hip_x','l_hip_z','l_hip_y','l_knee_y','l_ankle_y'] and self.lLegMou.isChecked()) or \
                (art in ['r_hip_x','r_hip_z','r_hip_y','r_knee_y','r_ankle_y'] and self.rLegMou.isChecked()):
                r['goal_position'].append(0.0)
                r['compliant'].append(True)
            else:
                r['goal_position'].append(a)
                r['compliant'].append(False)
            r['moving_speed'].append(self.inputs[art]['moving_speed'].getValue(f))
        self.COM._robotOut = r
        
    def setOutputs(self,f):
        r = self.COM._robotIn
        if len(r)>0:
            for i in range(len(r['name'])):
                art = r['name'][i]
                self.outputs[art]['present_position'].setValue(r['present_position'][i],f)
                self.outputs[art]['present_speed'].setValue(r['present_speed'][i],f)
            self.tempLabel.setText("Max Temp : "+str(max(r["present_temperature"]))+"deg")
            self.voltLabel.setText("Min voltage : "+str(min(r["present_voltage"]))+"V")
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
        self.poll = zmq.Poller()
        self.poll.register(self._socket,zmq.POLLIN)
        
    def run(self):
        send = 0
        while self._active:
            t0 = Tools.getTime()
            if send == 0:
                req = {"robot":{"get_all_register_values":{}}}
            else:
                req = {"robot":{"set_all_register_values":{"dict":self._robotOut}}} 
            self._socket.send_json(req)
            expect = True
            while expect:
                socks = dict(self.poll.poll(100))
                #print socks.get(self._socket)
                if socks.get(self._socket) == zmq.POLLIN:
                    #print "t1"
                    reply = self._socket.recv_json()
                    #print reply
                    if not reply:
                        break
                    else:
                        if send == 0:
                            self._robotIn = reply
                        expect = False
                else:
                    print "reconnect"
                    self._socket.setsockopt(zmq.LINGER, 0)
                    self._socket.close()
                    self.poll.unregister(self._socket)
                    self._socket = self._context.socket(zmq.REQ)
                    self._socket.connect("tcp://"+self._IP+":"+self._port)
                    self.poll.register(self._socket,zmq.POLLIN)
                    self._socket.send_json(req)
            if send == 0:
                send = 1
            else:
                send = 0
            while Tools.getTime()-t0<0.02:
                a=1
    
    def run_old(self):
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
        