import zmq
import pypot.robot
from threading import Thread
import netifaces
import json
import time
import numpy as np


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
        
    def run(self):
        print "toto"
        while self._active:
            # waiting for a message
            reply = self._socket.recv_json()
            if reply.has_key("robot"):
                if reply["robot"].has_key("get_pose"):
                    self._socket.send_json(self._robotOut)
                elif reply["robot"].has_key("set_pose"):
                    self._robotIn = reply["robot"]["set_pose"]
                    self._socket.send_json({})
                else:
                    print "message not recognized."
                    print reply
                    self._socket.send_json("{}")

if __name__ == "__main__":
    addresses = netifaces.ifaddresses('wlan4')
    ip = addresses[netifaces.AF_INET][0]["addr"]
    robot = pypot.robot.from_json("full_poppy.json")
    task = listener(ip,'8080')
    task.start()
    number = "-1"
    duration = "1"
    goal_pose = {}
    v = {}
    p0 = {}
    v0 = {}
    pc = {}
    
    goon = True
    
    while goon:
        t = time.time()
        
        # print t
        # allocate the present_pose register
        a = {}
        p = {}
        
        tempc = 0
        voltage = 1000
        for mot in robot.motors:
            p[mot.name] = mot.present_position
            a[mot.name] = str(np.round(p[mot.name]*100)/100)
            tempc = max(tempc,mot.present_temperature)
            if mot.model!='XL-320':
                voltage = min(voltage,mot.present_voltage)
        a["Temperature"] = str(tempc)
        a["Voltage"] = str(voltage)
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
                    elif mot == "Name":
                        temp = 1
                    else:
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
                            ap = (yc-yp0*duration-y0)/(duration**2)
                            bp = yp0
                            cp = y0
                            m.compliant = False
                            pc[mot] = ap*dt**2+bp*dt+cp
                            v[mot] = 2*ap*dt+bp
                            m.goal_position = pc[mot]
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
                        else:
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
                # print "p0"
                # print p0
                # print "v0"
                # print v0
                # print "b"
                # print b
                
        while time.time()-t<=0.02:
            time.sleep(0.001)