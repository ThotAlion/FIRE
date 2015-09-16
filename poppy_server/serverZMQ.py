import pypot.robot
from pypot.server.zmqserver import ZMQRobotServer
from threading import Thread
import netifaces

# instanciate the robot
r = pypot.robot.from_json("full_poppy.json")
for m in r.motors:
    m.torque_limit = 90

addresses = netifaces.ifaddresses('wlan2')
ip = addresses[netifaces.AF_INET][0]["addr"]

server = ZMQRobotServer(r,host = ip,port='8080')

Thread(target=lambda: server.run()).start()