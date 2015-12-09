# -*- coding: cp1252 -*-
import pygame
import time
import argparse
from pygame.locals import *
from numpy import *
from naoqi import ALProxy

joy = None
hat_up = None
hat_down = None
hat_left = None
hat_right = None
motion = None
posture = None
speech = None
memory = None
leds = None
is_nao_walking = None
is_nao_headmoving = None
is_nao_turning = None


def global_init(robotIP, PORT):

    global joy, hat_up, hat_down, hat_left, has_right
    global motion, posture, speech, memory, leds
    global is_nao_walking, is_nao_headmoving


    #### Init Joystick - PI game
    pygame.init()

    pygame.joystick.init()
    joy = pygame.joystick.Joystick(0)
    joy.init()

    print joy.get_name()
    print joy.get_init()

    #### boolean of hat joystick
    hat_up = False
    hat_down = False
    hat_left = False
    hat_right = False

    ##### Init of nao, position and move
    is_nao_walking = False
    is_nao_headmoving = False
    is_nao_turning = False


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
        memory = ALProxy("ALMemory", robotIP, PORT)
    except Exception, e:
        print "Could not create proxy to ALMemory"
        print "Error was: ",e

    try:
        leds = ALProxy("ALLeds", robotIP, PORT)
    except Exception, e:
        print "Could not create proxy to ALLeds"
        print "Error was: ",e



def nao_init_pos():

    if motion:
        motion.setStiffnesses("Body", 1.0)

    nao_go_posture("StandInit")
    
    ## Enable arms control by Motion algorithm
    if motion:
        motion.setMoveArmsEnabled(True, True)

        ## Enable head to move
        motion.wbEnableEffectorControl("Head", True)
    


def nao_go_posture(posture_name):

    if posture_name != "Rest":    
        posture.goToPosture(posture_name, 0.65)

    else:
        motion.rest()
        print "rest !" 

    #####
    # If you just want a shortcut to reach the posture quickly when manipulating the robot
    # you can use ALRobotPostureProxy::applyPosture() (you will have to help the robot)
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
   
    if Speed > 0.01 :
    
        Frequency = abs(Speed)

        try:
            #motion.moveToward( X, Y, Theta, [["Frequency", Frequency]])
            motion.setWalkTargetVelocity( X, Y, Theta, Frequency)
        except Exception, errorMsg:
            print str(errorMsg)
            print " not allowed to walk "
    else:
         motion.moveToward(0,0,0)
        #motion.stopMove()
        #nao_go_posture("StandInit")

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

    global is_nao_headmoving
    
    if(not(is_nao_headmoving) and abs(yaw * pitch)>0):
        motion.stiffnessInterpolation("Head", 1.0, 0.1)
        is_nao_headmoving = True


    fractionMaxSpeed  = 0.2
    
    motion.setAngles("HeadYaw",yaw*3.14/180.0, fractionMaxSpeed);
    motion.setAngles("HeadPitch",pitch*3.14/180.0, fractionMaxSpeed);

    if(not(is_nao_headmoving) and (yaw*pitch==0.0)):
        motion.stiffnessInterpolation("Head", 0.0, 0.4)

  
    #timeLists  = [[0.2], [0.2]]
    #motion.angleInterpolationBezier(names, timeLists, angleLists)

def nao_move_hands(isLeftOpen, isRightOpen):
    
    stiffness = 1.0
    time = 1.0
    motion.stiffnessInterpolation("Hand", stiffness, time)

    if isLeftOpen:
        motion.openHand("LHAND")
    else:
        motion.closeHand("LHAND")

    if isRightOpen:
        motion.openHand("RHAND")
    else:
        motion.closeHand("RHAND")

def nao_memoryEvent(name, num):

    memory.raiseEvent(name, num)

def nao_leds(name, value):

    if name == "ear" :
        if value > 0 :
            leds.on("EarLeds")
        else:
            leds.off("EarLeds")

    if name == "rotate" :
        leds.rotateEyes(0x00FF0000, 0.5, value)

    if name == "rasta":
        leds.rasta(value)
        
                           
def nao_say(toSay):

    speech.say("Dance, dance, dance! How are You?")
                

def joystick_update():

    global is_nao_headmoving, is_nao_walking, is_nao_turning
    global hat_up, hat_down, hat_left, hat_right
    
    for event in pygame.event.get():
        
        if pygame.joystick.get_count() > 0:
            if event.type == pygame.locals.JOYBUTTONDOWN:

                ###### BOUTON DE MANETTE #########

                if joy.get_button(5):
                    print "RB tourner à gauche"
                    nao_move_hands(False, False)

                if joy.get_button(4):
                    print "LB tourner à droite"
                    nao_move_hands(True, True)

                if joy.get_button(3):

                    if hat_up:
                        print "Y up  Led couleur 1"
                        nao_leds("ear", 1 )
                    elif hat_down:
                        print " Y down Se lever"
                        nao_go_posture("Stand")
                    elif hat_left:
                        print " Y left Bras gauche     "
                    elif hat_right:
                        print "Y right Bras droite"
                    else :
                        print "Y dire quelque chose"
                        nao_say("bijour les amis")

                if joy.get_button(2):
                    if hat_up:
                        print "X up Led couleur 2"
                        nao_leds("rotate", 2)
                    elif hat_down:
                        print " X down position Crouch"
                        nao_go_posture("Rest")
                    elif hat_left:
                        print " X left Bras gauche"
                    elif hat_right:
                        print "X right Bras droit"
                    else :
                        print "X animation 1"
                        nao_memoryEvent("anim", 1)

                if joy.get_button(1):
                    if hat_up:
                        print "B up Led couleur 3"
                        nao_leds("rasta", 2)
                    elif hat_down:
                        print " B down position stand init"
                        nao_go_posture("StandInit")
                    elif hat_left:
                        print " B left Bras gauche"
                    elif hat_right:
                        print "B right Bras droit"
                    else :
                        print "B animation 2"
                        nao_memoryEvent("anim", 2)

                if joy.get_button(0):
                    if hat_up:
                        print "A up Led couleur 4"
                        nao_leds("ear",0 )
                    elif hat_down:
                        print " A down s'assoir"
                        nao_go_posture("LyingBack")
                    elif hat_left:
                        print " A left Bras gauche"
                    elif hat_right:
                        print "A right Bras droit"
                    else :
                        print "A animation 3"
                        nao_memoryEvent("anim", 3)

            
            if event.type == pygame.locals.JOYAXISMOTION:

                ###### JOYSTICK MARCHE #########
                if abs(joy.get_axis(1)) + abs( joy.get_axis(0)) < 0.18 :
                    if is_nao_walking :
                        print "stop"
                        is_nao_walking = False
                        nao_update_walk(0.0, 0.0, 0.0, 0.0)
                    
                else:
                    ax1= joy.get_axis(1)
                    ax0= joy.get_axis(0)
                    print "avance "+str(ax1)+ " - "+str(ax0)
                    is_nao_walking = True                
                    nao_update_walk(abs(ax1)/(-ax1),0.0, -ax0*0.75, abs(ax1))
                # axis 1, avant (-1) arriere (1), axis 0, gauche (-1), droite (1)


                ###### LT - RT ROTATION DU ROBOT #########
                if abs(joy.get_axis(2))>0.1:
                    is_nao_turning = True
                    ax2 = joy.get_axis(2)

                    if(ax2 > 0 ) :
                        
                        print"LT "+str(ax2)
                        nao_update_walk(0.0,0.0,0.9 , ax2)
                    else:
                        print"RT "+str(joy.get_axis(2))
                        nao_update_walk(0.0,0.0,-0.9 , abs(ax2))

                    
                else :
                    if is_nao_turning:
                        is_nao_turning = False
                        print("Stop turning")
                        nao_update_walk(0.0, 0.0, 0.0, 0.0)
        
                ###### JOYSTICK TETE #########
                if abs(joy.get_axis(3)) + abs(joy.get_axis(4)) < 0.18 :
                    if is_nao_headmoving :
                        print "stop move head"
                        is_nao_headmoving = False
                        nao_move_head(0.0,0.0)
                else:
                    ax3 = joy.get_axis(3)
                    ax4 = joy.get_axis(4)                
                    print "move head "+str(ax3)+" - "+str(ax4)
                    nao_move_head(-ax4*85.5, -ax3*29.5)
                # axis 3 (up -1, down 1) acix 4 (-1 left, 1 right )

            ###### JOYSTICK HAT #########
            if event.type == pygame.locals.JOYHATMOTION:
                (a,b) = joy.get_hat(0)
                if a > 0.2 :
                    #print "hat right"
                    hat_right = True
                else:
                    hat_right = False
                if a < -0.2 :
                    #print "hat left"
                    hat_left = True
                else:
                    hat_left = False
                if b > 0.2 :
                    #print "hat up"
                    hat_up = True
                else :
                    hat_up = False
                if b < -0.2 :
                    #print "hat down"
                    hat_down = True
                else:
                    hat_down = False


def main(robotIP, PORT=9559):
    global_init(robotIP, PORT)
    nao_init_pos()

    time.sleep(2)
    while 1:
        joystick_update()
        time.sleep(0.02)

        
                           
                
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="10.0.1.12",
                        help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559,
                        help="Robot port number")

    args = parser.parse_args()
    main(args.ip, args.port)
            
