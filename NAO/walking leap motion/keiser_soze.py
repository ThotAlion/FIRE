# -*- encoding: UTF-8 -*-

''' Walk: Small example to make Nao walk '''
'''       with gait customization        '''
'''       NAO is Keyser Soze             '''
''' This example is only compatible with NAO '''

import argparse
import time
import almath
from naoqi import ALProxy
import Leap
from numpy import *

def main(robotIP, PORT=9559):

    motionProxy  = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)

    # Wake up robot
    motionProxy.wakeUp()

    # Send robot to Stand Init
    postureProxy.goToPosture("StandInit", 0.5)
    lm = Leap.Controller()
    
    while True:
        frame = lm.frame()
        y = 0.0
        p = 0.0
        for fin in frame.fingers:
            if fin.hand.is_left and fin.type == fin.TYPE_INDEX:
                y=fin.direction.yaw
                p=fin.direction.pitch
                print y
        # TARGET VELOCITY
        X         = sin(2*p)
        Y         = 0.0
        Theta     = -sin(y)
        Frequency = 4

        try:
            motionProxy.moveToward(X, Y, Theta)
        except Exception, errorMsg:
            print str(errorMsg)
            print "This example is not allowed on this robot."
            exit()

        time.sleep(0.05)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="10.0.0.4",
                        help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559,
                        help="Robot port number")

    args = parser.parse_args()
    main(args.ip, args.port)