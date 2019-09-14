import zmq
from dynamixel_sdk import *
from threading import Thread
import netifaces
import json
import time
import numpy as np

import logging
import sys

root = logging.getLogger()
root.setLevel(logging.WARNING)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.WARNING)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)


class listener(Thread):
    
    def __init__(self,IP,port):
        # setup zmq context
        Thread.__init__(self)
        self._IP = IP
        self._port = port
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.REP)
        self._socket.bind("tcp://"+self._IP+":"+self._port)
        self._robotIn = {}
        self._robotOut = {}
        self._active = True
        self._reset = False
        
    def run(self):
        print "toto"
        while self._active:
            # waiting for a message
            self._reset = False
            reply = self._socket.recv_json()
            if reply.has_key("robot"):
                if reply["robot"].has_key("get_pose"):
                    self._socket.send_json(self._robotOut)
                elif reply["robot"].has_key("set_pose"):
                    self._robotIn = reply["robot"]["set_pose"]
                    self._socket.send_json({})
                elif reply["robot"].has_key("reset"):
                    self._reset = True
                    self._socket.send_json({})
                    
                else:
                    print "message not recognized."
                    print reply
                    self._socket.send_json("{}")

if __name__ == "__main__":
    ip = '0.0.0.0'
    json_name = "legs.json"
    robot = pypot.robot.from_json(json_name)
    task = listener(ip,'8080')
    task.start()
    number = "-1"
    duration = "1"
    abreath = 0.0
    tbreath = 10.0
    fact = 0.2
    goal_pose = {}
    v = {}
    p0 = {}
    v0 = {}
    pc = {}
    
    goon = True
    
    while goon:
        t = time.time()
        breath = abreath*np.sin(2*3.14*t/tbreath)
        if task._reset == True:
            print "Reset!"
            robot.close()
            robot = pypot.robot.from_json(json_name)
            print "Reset is done"
        
        # print t
        # allocate the present_pose register
        a = {}
        p = {}
        
        tempc = 0
        minVoltage = 1000
        maxVoltage = 0
        hottest = 'TBD'
        for mot in robot.motors:
            p[mot.name] = mot.present_position
            a[mot.name] = str(np.round(p[mot.name]*100)/100)
            a["v_"+mot.name] = str(np.round(mot.present_voltage*10)/10)
            tempc = max(tempc,mot.present_temperature)
            if tempc == mot.present_temperature:
                hottest = mot.name
            if mot.model!='XL-320':
                minVoltage = min(minVoltage,mot.present_voltage)
                maxVoltage = max(maxVoltage,mot.present_voltage)
        a["Temperature"] = str(tempc)
        a["VoltageMin"] = str(minVoltage)
        a["VoltageMax"] = str(maxVoltage)
        a["Hottest"] = hottest
        if len(p0)==0:
            p0 = p.copy()
            t0 = t        
        task._robotOut = a
        
        # pilot robot function of goal_pose register
        b = task._robotIn.copy()
        if b.has_key("Number") and b.has_key("Duration"):
            
            if b["Number"]==number:
                # during a pose
                for mot in b:
                    if mot == "Number":
                        number = b["Number"]
                    elif mot == "Duration":
                        duration = float(b["Duration"])
                    elif mot == "Abreath":
                        abreath = float(b["Abreath"])
                    elif mot == "Tbreath":
                        tbreath = float(b["Tbreath"])
                    elif mot == "Name":
                        temp = 1
                    elif robot.__dict__.has_key(mot):
                        m = getattr(robot,mot)
                        if b[mot][0] == "M":
                            v[mot] = 0.0
                            if m.present_position<=min(m.angle_limit):
                                m.compliant = False
                                pc[mot] = min(m.angle_limit)
                                m.goal_position = pc[mot]
                            elif m.present_position>=max(m.angle_limit):
                                m.compliant = False
                                pc[mot] = max(m.angle_limit)
                                m.goal_position = pc[mot]
                            else:
                                m.compliant = True
                                pc[mot] = p[mot]
                        elif b[mot][0] == "Z":
                            v[mot] = 0.0
                            m.compliant = True
                            pc[mot] = p[mot]
                        elif b[mot][0] == "P":
                            v[mot] = 0
                            pc[mot] = p[mot]
                            m.compliant = False
                            m.goal_position = pc[mot]
                        elif b[mot][0] == "K":
                            v[mot] = 0
                            pc[mot] = p0[mot]
                            m.compliant = False
                            m.goal_position = pc[mot]
                            if mot == 'r_shoulder_y' or mot == 'l_shoulder_y':
                                m.goal_position = m.goal_position + (1-fact)* breath
                            if mot == 'bust_y':
                                m.goal_position = m.goal_position - (1-fact)* breath
                            if mot == 'abs_y':
                                m.goal_position = m.goal_position + fact*breath
                        elif b[mot][0] == "L":
                            dt = t-t0
                            if dt>=duration:
                                dt = duration
                            yc = float(b[mot][1:])
                            y0 = p0[mot]
                            if v0.has_key(mot):
                                yp0 = v0[mot]
                            else:
                                v0=0.0
                            # cubic interpolation with end parallel to the AB segment
                            ap = (y0-yc)/(duration**3)+yp0/duration**2
                            bp = 2*(yc-y0)/(duration**2)-2*yp0/duration
                            cp = yp0
                            dp = y0
                            m.compliant = False 
                            pc[mot] = ap*dt**3+bp*dt**2+cp*dt+dp
                            v[mot] = 3*ap*dt**2+2*bp*dt+cp
                            m.goal_position = pc[mot]
                            if mot == 'r_shoulder_y' or mot == 'l_shoulder_y':
                                m.goal_position = m.goal_position + (1-fact)* breath
                            if mot == 'bust_y':
                                m.goal_position = m.goal_position - (1-fact)* breath
                            if mot == 'abs_y':
                                m.goal_position = m.goal_position + fact*breath
                        elif b[mot][0] == "S":
                            dt = t-t0
                            if dt>=duration:
                                dt = duration
                            yc = float(b[mot][1:])
                            y0 = p0[mot]
                            if v0.has_key(mot):
                                yp0 = v0[mot]
                            else:
                                yp0=0.0
                            ap = 2*(y0-yc)/(duration**3)+yp0/duration**2
                            bp = 3*(yc-y0)/(duration**2)-2*yp0/duration
                            cp = yp0
                            dp = y0
                            m.compliant = False 
                            pc[mot] = ap*dt**3+bp*dt**2+cp*dt+dp
                            v[mot] = 3*ap*dt**2+2*bp*dt+cp
                            m.goal_position = pc[mot]
                            if mot == 'r_shoulder_y' or mot == 'l_shoulder_y':
                                m.goal_position = m.goal_position + (1-fact)* breath
                            if mot == 'bust_y':
                                m.goal_position = m.goal_position - (1-fact)* breath
                            if mot == 'abs_y':
                                m.goal_position = m.goal_position + fact*breath
                        else:
                            print b
                            print mot
                            v[mot] = 0
                            pc[mot] = float(b[mot])
                            m.compliant = False
                            m.goal_position = pc[mot]
            else:
                # pose change
                p0 = pc.copy()
                t0 = t
                v0 = v.copy()
                duration = float(b["Duration"])
                number = b["Number"]
                
        while time.time()-t<=0.02:
            time.sleep(0.001)