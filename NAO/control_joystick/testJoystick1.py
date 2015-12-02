# -*- coding: cp1252 -*-
import pygame
import math
import time
import argparse
from pygame.locals import *
from naoqi import ALProxy


#### Init Joystick - PI game
pygame.init()

pygame.joystick.init()
joy = pygame.joystick.Joystick(0)
joy.init()

print joy.get_name()
print joy.get_init()
#Print number of joystick available
#print "number of hat"+str(joy.get_numhats())
#print "number of ball"+str(joy.get_numballs())
#print "number of axes"+str(joy.get_numaxes())

##### init Nao Proxy
nao_ip = "nao.local"
nao_port = 9559

try:
    motion = ALProxy("ALMotion", nao_ip, nao_port)
except Exception, e:
    print "Could not create proxy to ALMotion"
    print "Error was: ",e

try:
    posture = ALProxy("ALRobotPosture", nao_ip, nao_port)
except Exception, e:
    print "Could not create proxy to ALRobotPosture"
    print "Error was: ",e

try:
    speech = ALProxy("ALTextToSpeech", nao_ip, nao_port)
except Exception, e:
    print "Could not create proxy to ALTextToSpeech"
    print "Error was: ",e

try:
    memory = ALProxy("ALMemory")
except Exception, e:
    print "Could not create proxy to ALMemory"
    print "Error was: ",e




###### MEMO #########
# motion.moveInit() :: motion.moveTo(0.5, 0, 0)
# motion.setStiffnesses("Body", 1.0)
# speech.say("something")
# memory.subscribeToEvent("nom de l'event", "nom du module", "nom de la fonction a appeler")
#####################



def nao_init_pos():

    nao_go_posture("StandInit")
    
    ## Enable arms control by Motion algorithm
    motion.setMoveArmsEnabled(True, True)

    ## Enable head to move
    motion.wbEnableEffectorControl("Head", True)
    


def nao_go_posture(posture_name):

    posture.goToPosture(posture_name, 1.0)

    #####
    # Présence d'une fonction motion.rest() ? pour aller sur une posture de repos
    # présence d'un motion.wakeUp()
    #If you just want a shortcut to reach the posture quickly when manipulating the robot
    #you can use ALRobotPostureProxy::applyPosture() (you will have to help the robot)
    #####

    ##### MEMO DES POSTURES
    #
    #Crouch,
    #LyingBack,
    #LyingBelly,
    #Sit,
    #SitRelax,
    #Stand,
    #StandInit,
    #StandZero
    ##############


def nao_update_walk(X, Y, Theta, Speed):

    is_nao_walking = False

    if Speed > 0.01:
        is_nao_walking = True

    if is_nao_walking :
    
        Frequency = Speed

        try:
            motion.moveToward( X, Y, Theta, [["Frequency", Frequency]]
        except Exception, errorMsg:
            print str(errorMsg)
            print " not allowed to walk "
    else:

        motion.stopMove()
        nao_go_posture("StandInit")

    ########### MEMO ######
    # motion.stopMove()
    # motionProxy.moveTo(x, y, theta,
    #        [ ["MaxStepX", 0.02],         # step of 2 cm in front
    #          ["MaxStepY", 0.16],         # default value
    #          ["MaxStepTheta", 0.4],      # default value
    #          ["MaxStepFrequency", 0.0],  # low frequency
    #          ["StepHeight", 0.01],       # step height of 1 cm
    #          ["TorsoWx", 0.0],           # default value
    #          ["TorsoWy", 0.1] ])         # torso bend 0.1 rad in front
    #################

def  nao_move_head(yaw,pitch):

    stiffness = 1.0
    time = 1.0
    motion.stiffnessInterpolation("Head", stiffness, time)

    fractionMaxSpeed  = 0.1f
    names      = ["HeadYaw", "HeadPitch"]
    angleLists = [[yaw*almath.TO_RAD], [pitch*almath.TO_RAD]]
    motion.setAngles(names, anglesLists, fractionMaxSpeed);

    #timeLists  = [[0.2], [0.2]]
    #motion.angleInterpolationBezier(names, timeLists, angleLists)

def nao_move_hands(isLeftOpen, isRightOpen):
    
    if isLeftOpen:
        motion.openHand("LHAND")
    else:
        motion.closeHand("LHAND")

    if isRightOpen:
        motion.openHand("RHAND")
    else:
        motion.closeHand("RHAND")
                           
                           
                

def joystick_update():    

    for event in pygame.event.get():
        
        if pygame.joystick.get_count() > 0:
            if event.type == pygame.locals.JOYBUTTONDOWN:
                if joy.get_button(5):
                    print "RB"
                if joy.get_button(4):
                    print "LB"
                if joy.get_button(3):
                    print "Y"
                if joy.get_button(2):
                    print "X"
                if joy.get_button(1):
                    print "B"
                if joy.get_button(0):
                    print "A"

            if event.type == pygame.locals.JOYAXISMOTION:
                if joy.get_axis(1) > 0.2 :
                    print "down"+str(joy.get_axis(1))
                if joy.get_axis(1) < -0.2 :
                    print "up"+str(joy.get_axis(1))
                if joy.get_axis(0) > 0.2 :
                    print "right"+str(joy.get_axis(0))
                if joy.get_axis(0) < -0.2 :
                    print "left"+str(joy.get_axis(0))

                if joy.get_axis(3) > 0.2 :
                    print "2n down"+str(joy.get_axis(3))
                if joy.get_axis(3) < -0.2 :
                    print "2n up"+str(joy.get_axis(3))
                if joy.get_axis(4) > 0.2 :
                    print "2n right"+str(joy.get_axis(4))
                if joy.get_axis(4) < -0.2 :
                    print "2n left"+str(joy.get_axis(4))

            if event.type == pygame.locals.JOYHATMOTION:
                (a,b) = joy.get_hat(0)
                if a > 0.2 :
                    print "hat right"+str(a)
                if a < -0.2 :
                    print "hat left"+str(a)
                if b > 0.2 :
                    print "hat up"+str(b)
                if b < -0.2 :
                    print "hat down"+str(b)

def main(robotIP, PORT=9559):
    

                           
                
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559,
                        help="Robot port number")

    args = parser.parse_args()
    main(args.ip, args.port)
            
