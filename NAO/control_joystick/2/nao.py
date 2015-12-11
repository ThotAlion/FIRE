from naoqi import ALProxy
import time

class Nao:


    def __init__(self,robotIP,robotName, PORT=9559):

        self.name = robotName
        
        try:
            self.motion = ALProxy("ALMotion", robotIP, PORT)
        except Exception, e:
            print self.name+" Could not create proxy to ALMotion"
            print "Error was: ",e

        try:
            self.posture = ALProxy("ALRobotPosture",robotIP, PORT)
        except Exception, e:
            print self.name+" Could not create proxy to ALRobotPosture"
            print "Error was: ",e

        try:
            self.speech = ALProxy("ALTextToSpeech", robotIP, PORT)
        except Exception, e:
            print self.name+" Could not create proxy to ALTextToSpeech"
            print "Error was: ",e

        try:
            self.memory = ALProxy("ALMemory", robotIP, PORT)
        except Exception, e:
            print self.name+" Could not create proxy to ALMemory"
            print "Error was: ",e

        try:
            self.leds = ALProxy("ALLeds", robotIP, PORT)
        except Exception, e:
            print self.name+" Could not create proxy to ALLeds"
            print "Error was: ",e

        try:
            self.behavior = ALProxy("ALBehaviorManager", robotIP, PORT)
        except Exception, e:
            print self.name+" Could not create proxy to ALBehavior"
            print "Error was: ",e

        ##### Init of nao, position and move
        self.is_walking = False
        self.is_headmoving = False
        self.is_turning = False
        self.name = robotName

        print "creation du nao: "+self.name







    def init_pos(self):

        if self.motion:
            self.motion.stopMove()
            self.motion.setStiffnesses("Body", 1.0)

        self.go_posture("Crouch")
        
        ## Enable arms control by Motion algorithm
        if self.motion:

            #self.motion.setMoveArmsEnabled(True, True)

            ## Enable head to move
            self.motion.wbEnableEffectorControl("Head", True)

        if self.behavior.isBehaviorInstalled("main_joystick-d361da/behavior_1"):
            self.behavior.stopAllBehaviors()
            self.behavior.startBehavior("main_joystick-d361da/behavior_1")
 

    ### NOT use . Use of memoryEvent("PostureAsked", name ) instead
    def go_posture(self, posture_name):

        if posture_name != "Rest":

            self.motion.stopMove()
            self.posture.goToPosture(posture_name, 0.65)

        else:
            self.motion.rest()
            print "rest !" 

        #####
        # If you just want a shortcut to reach the posture quickly when manipulating the robot
        # you can use ALRobotPostureProxy::applyPosture() (you will have to help the robot)
        #
        #Crouch,LyingBack,LyingBelly,Sit,SitRelax,Stand,StandInit,StandZero
        ##############




    def update_walk(self, X, Y, Theta, Speed):
   
        if Speed > 0.01 :
        
            Frequency = abs(Speed)
            if X>0 :
                self.is_walking = True
            else :
                self.is_turning = True

            try:
                #motion.moveToward( X, Y, Theta, [["Frequency", Frequency]])
                self.motion.setWalkTargetVelocity( X, Y, Theta, Frequency)
            except Exception, errorMsg:
                print str(errorMsg)
                print " not allowed to walk "

        else:
            if self.is_turning:
                self.motion.moveToward(0,0,0)
                self.is_turning = False

            if self.is_walking:
                self.motion.moveToward(0,0,0)
                self.is_walking = False
            #motion.stopMove()
            #nao_go_posture("StandInit")


    def  move_head(self, yaw,pitch):

       
        if(not(self.is_headmoving) and abs(yaw * pitch)>0):
            self.motion.stiffnessInterpolation("Head", 1.0, 0.1)
            self.is_headmoving = True


        fractionMaxSpeed  = 0.2
        
        self.motion.setAngles("HeadYaw",yaw*3.14/180.0, fractionMaxSpeed);
        self.motion.setAngles("HeadPitch",pitch*3.14/180.0, fractionMaxSpeed);

        if(not(self.is_headmoving) and (yaw*pitch==0.0)):
            self.motion.stiffnessInterpolation("Head", 0.0, 0.4)
            self.is_headmoving = False

      
        #timeLists  = [[0.2], [0.2]]
        #motion.angleInterpolationBezier(names, timeLists, angleLists)

    def memoryEvent(self, name, num):

        self.memory.raiseEvent(name, num)

    def use_leds(self, name, value):

        if name == "ear" :
            if value > 0 :
                self.leds.on("EarLeds")
                self.leds.on("BrainLeds")
            else:
                self.leds.off("EarLeds")
                self.leds.off("BrainLeds")

        if name == "rotate" :
            self.leds.rotateEyes(0x00FF0000, 0.5, value)

        if name == "rasta":
            self.leds.rasta(value)

    def activate(self, is_activated):
    #function in order to recognize the current nao remotely controlled


        if is_activated and self.leds:
            self.use_leds("ear", 1)
        elif self.leds :
            self.use_leds("ear", 0)
                
                               
    def say(self, toSay):

        self.speech.say(toSay)
                

    
