# -*- coding: cp1252 -*-
import pygame
import math
import time
import argparse
from pygame.locals import *
from naoqi import ALProxy

def global_init(robotIP, PORT):

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

    #boolean of hat joystick
    hat_up = False
    hat_down = False
    hat_left = False
    hat_right = False


    try:
        motion = ALProxy("ALMotion", robotIP, PORT)
    except Exception, e:
        print "Could not create proxy to ALMotion"
        print "Error was: ",e

    try:
        posture = ALProxy("ALRobotPosture",robotIP, PORT)
    except Exception, e:
        print "Could not create proxy to ALRobotPosture"
        print "Error was: ",e

    try:
        speech = ALProxy("ALTextToSpeech", robotIP, PORT)
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
            motion.moveToward( X, Y, Theta, [["Frequency", Frequency]])
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

    fractionMaxSpeed  = 0.1
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
                    print "RB tourner à gauche"
                if joy.get_button(4):
                    print "LB tourner à droite"
                if joy.get_button(3):

                    if hat_up:
                        print "Y up  Led couleur 1"
                    elif hat_down:
                        print " Y down Se lever"
                    elif hat_left:
                        print " Y left Bras gauche     "
                    elif hat_right:
                        print "Y right Bras droite"
                    else :
                        print "Y dire quelque chose"

                if joy.get_button(2):
                    if hat_up:
                        print "X up Led couleur 2"
                    elif hat_down:
                        print " X down position Crouch"
                    elif hat_left:
                        print " X left Bras gauche"
                    elif hat_right:
                        print "X right Bras droit"
                    else :
                        print "X animation 1"
                if joy.get_button(1):
                    if hat_up:
                        print "B up Led couleur 3"
                    elif hat_down:
                        print " B down position stand init"
                    elif hat_left:
                        print " B left Bras gauche"
                    elif hat_right:
                        print "B right Bras droit"
                    else :
                        print "B animation 2"
                if joy.get_button(0):
                    if hat_up:
                        print "A up Led couleur 4"
                    elif hat_down:
                        print " A down s'assoir"
                    elif hat_left:
                        print " A left Bras gauche"
                    elif hat_right:
                        print "A right Bras droit"
                    else :
                        print "A animation 3"

            if event.type == pygame.locals.JOYAXISMOTION:
                if abs(joy.get_axis(1)) + abs( joy.get_axis(0)) < 0.1 :
                    if is_nao_walking :
                        print "stop"
                        is_nao_walking = False
                    
                else:
                    print "avance "+str(joy.get_axis(1))+ " - "+str(joy.get_axis(0))
                    is_nao_walking = True
                # axis 1, avant (-1) arriere (1), axis 0, gauche (-1), droite (1)

                if abs(joy.get_axis(3)) + abs(joy.get_axis(4)) < 0.15 :
                    if is_nao_headmoving :
                        print "stop move head"
                        is_nao_headmoving = False
                else:
                    print "move head "+str(joy.get_axis(3))+" - "+str(joy.get_axis(4))
                    is_nao_headmoving = True
                # axis 3 (up -1, down 1) acix 4 (-1 left, 1 right )

            if event.type == pygame.locals.JOYHATMOTION:
                (a,b) = joy.get_hat(0)
                if a > 0.2 :
                    #print "hat right"+str(a)
                    hat_right = True
                else:
                    hat_right = False
                if a < -0.2 :
                    #print "hat left"+str(a)
                    hat_left = True
                else:
                    hat_left = False
                if b > 0.2 :
                    #print "hat up"+str(b)
                    hat_up = True
                else :
                    hat_up = False
                if b < -0.2 :
                    #print "hat down"+str(b)
                    hat_down = True
                else:
                    hat_down = False


def main(robotIP, PORT=9559):
    global_init(robotIP, PORT)
    while 1:
        joystick_update()
        
                           
                
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559,
                        help="Robot port number")

    args = parser.parse_args()
    main(args.ip, args.port)
            
