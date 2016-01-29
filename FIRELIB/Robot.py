from numpy import *
import Block
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from Connexion import *
import zmq
import json
from threading import Thread
import Tools
import time

class Robot(Block.Block,QWidget):
    """ this class describes a block """
    
    def __init__(self,members,IP = '127.0.0.1',port = '8080'):
        Block.Block.__init__(self)
        QWidget.__init__(self)
        self.IP = IP
        self.port = port
        # members is a dictionnary containing list of motors
        self.members = members
        # declaration of connexions
        # duration of the pose
        self.inputs["Duration"] = Connexion(default = "1")
        # name of the pose
        self.inputs["Name"] = Connexion(default = "toto")
        # number of the pose
        self.inputs["Number"] = Connexion(default = "0")
        # emergency stop
        self.inputs["Emergency"] = Connexion(default = "0")
        # temperature inside the robot
        self.outputs["Temperature"] = Connexion(default = "0")
        # battery voltage of the robot
        self.outputs["Voltage"] = Connexion(default = "0")
        for member in self.members:
            for art in self.members[member]:
                # which pose to present
                self.inputs[art] = Connexion(default = "M")
                # what position for each motor
                self.outputs[art] = Connexion(default = "0")
            
        # creation of components
        self.dict_checkbox = {}
        
        self.dict_checkbox["All"] = QCheckBox("Force All mou")
        self.resetButton = QPushButton("Reset Robot")
        for member in self.members:
            self.dict_checkbox[member] = QCheckBox("Force "+member+" mou")
        
        self.tempLabel = QLabel("Max Temp : 0deg")
        self.hottestMotor = QLabel("Hottest motor : TBD")
        self.minVoltLabel = QLabel("Min Voltage : 0V")
        self.maxVoltLabel = QLabel("Max Voltage : 0V")
        
        # composition
        mainlayout = QVBoxLayout(self)
        for member in self.dict_checkbox:
            mainlayout.addWidget(self.dict_checkbox[member])
        mainlayout.addWidget(self.tempLabel)
        mainlayout.addWidget(self.hottestMotor)
        mainlayout.addWidget(self.minVoltLabel)
        mainlayout.addWidget(self.maxVoltLabel)
        mainlayout.addWidget(self.resetButton)
        
        # signals
        for member in self.members:
                self.connect(self.dict_checkbox["All"],SIGNAL("toggled(bool)"),self.dict_checkbox[member],SLOT("setChecked(bool)"))
        
        self.show()
        
    
    def start(self):
        self.COM = clientThread(self.IP,self.port)
        self.COM.start()
        
    def init(self,f):
        return f
    
    def getInputs(self,f):
        r = {}
        r["Duration"] = self.inputs['Duration'].getValue(f)
        r["Name"] = self.inputs['Name'].getValue(f)
        r["Number"] = self.inputs['Number'].getValue(f)
        for member in self.members:
            for art in self.members[member]:
                if self.inputs["Emergency"].getValue(f) == "1":
                    a = "M"
                elif self.dict_checkbox[member].isChecked():
                    a = "M"
                else:
                    a = self.inputs[art].getValue(f)
                r[art] = a
        if self.resetButton.isDown():
            self.COM._reset = True
        else:
            self.COM._reset = False
        self.COM._robotOut = r
        
    def setOutputs(self,f):
        r = self.COM._robotIn
        if len(r)>0:
            self.outputs["Temperature"].setValue(float(r["Temperature"]),f)
            self.outputs["Voltage"].setValue(r["VoltageMin"],f)
            for member in self.members:
                for art in self.members[member]:
                    if r.has_key(art):
                        self.outputs[art].setValue(r[art],f)
            self.tempLabel.setText("Max Temp : "+r["Temperature"]+"deg")
            if r.has_key("Hottest"):
                self.hottestMotor.setText("Hottest motor : "+r["Hottest"])
            self.minVoltLabel.setText("Min voltage : "+r["VoltageMin"]+"V")
            self.maxVoltLabel.setText("Max voltage : "+r["VoltageMax"]+"V")
            
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
        self._reset = False
        self._active = True
        self.poll = zmq.Poller()
        self.poll.register(self._socket,zmq.POLLIN)
        
    def run(self):
        send = 0
        while self._active:
            t0 = Tools.getTime()
            if self._reset == False:
                if send == 0:
                    req = {"robot":{"get_pose":"1"}}
                elif send == 1:
                    req = {"robot":{"set_pose":self._robotOut}}
            else:
                req = {"robot":{"reset":"1"}}
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
                    #print "reconnect"
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
            
    def close(self):
        self._active = False
        time.sleep(0.5)
        self._socket.close()
        