from naoqi import ALProxy
import time
from PyQt4 import QtGui, QtCore

class Nao(QtGui.QWidget):


    def __init__(self,robotIP,robotName,robotID, PORT=9559, parent=None):

        
        ######### GUI
        #QtGui.QWidget.__init__(self)
        super(Nao, self).__init__(parent)
        #slider marche
        self.slider1 = QtGui.QSlider(QtCore.Qt.Horizontal)
        #radio de connection
        self.radio_connect1 = QtGui.QRadioButton("None")
        self.radio_connect1.setChecked(QtCore.Qt.Checked)
        self.radio_connect2 = QtGui.QRadioButton("Connected")
        self.radio_connect2.setChecked(False)
        self.radio_connect3 = QtGui.QRadioButton("Ready")
        self.radio_connect3.setChecked(False)
        #progress bar de batterie
        self.battery_progress = QtGui.QProgressBar()
        self.battery_progress.setTextVisible(True)
        self.battery_progress.setMinimum(0)
        self.battery_progress.setMaximum(100)
        #niveau dautonomie
        self.lcd = QtGui.QLCDNumber(1)
        self.lcd.setSegmentStyle(QtGui.QLCDNumber.Flat)
        #Stiffness
        self.checkBox_stiff = QtGui.QCheckBox("Stiffness")
        #TODO change isChecked par clicked pour eviter le double envoi
        self.checkBox_stiff.clicked.connect(lambda: self.setStiffness(self.checkBox_stiff.isChecked() ))
        #Bouton restart
        self.button_proxy = QtGui.QPushButton("Proxy")
        self.button_proxy.clicked.connect(self.init_proxy)
        self.button_behavior = QtGui.QPushButton("Restart")
        self.button_behavior.clicked.connect(self.restart_behavior)
        #layout
        layout1 = QtGui.QVBoxLayout()
        layout1.addWidget(self.battery_progress)
        layout1.addWidget(self.lcd)
        layout1.addWidget(self.checkBox_stiff)
        layout1.addWidget(self.radio_connect1)
        layout1.addWidget(self.radio_connect2)
        layout1.addWidget(self.radio_connect3)
        layout1.addWidget(self.button_behavior)
        layout1.addWidget(self.button_proxy)
        #Group box
        groupBox = QtGui.QGroupBox(str(robotID)+": "+robotName)
        groupBox.setLayout(layout1)
        #Layout Main
        layoutMain = QtGui.QHBoxLayout()
        layoutMain.addWidget(groupBox)
        self.setLayout(layoutMain)

        ### Nao init
        self.name = robotName
        self.ip = robotIP
        self.port = PORT
        self.id = robotID
        self.autonomeLevel = 1
        self.lcd.display(self.autonomeLevel)
        
        ##### Init of nao, position and move
        self.is_walking = False
        self.is_headmoving = False
        self.is_turning = False
        
        self.init_proxy()


        print "creation du nao: "+str(self.id)+ " : "+self.name

    def init_proxy(self)  : 
        
        try:
            self.motion = ALProxy("ALMotion", self.ip, self.port)
        except Exception, e:
            print self.name+" Could not create proxy to ALMotion"
            print "Error was: ",e
            self.motion = None

        # try:
            # self.posture = ALProxy("ALRobotPosture",robotIP, PORT)
        # except Exception, e:
            # print self.name+" Could not create proxy to ALRobotPosture"
            # print "Error was: ",e
            # self.posture = None

        # try:
            # self.speech = ALProxy("ALTextToSpeech", robotIP, PORT)
        # except Exception, e:
            # print self.name+" Could not create proxy to ALTextToSpeech"
            # print "Error was: ",e
            # self.speech = None

        try:
            self.memory = ALProxy("ALMemory", self.ip, self.port)
        except Exception, e:
            print self.name+" Could not create proxy to ALMemory"
            print "Error was: ",e
            self.memory = None

        try:
            self.leds = ALProxy("ALLeds", self.ip, self.port)
        except Exception, e:
            print self.name+" Could not create proxy to ALLeds"
            print "Error was: ",e
            self.leds = None

        try:
            self.behavior = ALProxy("ALBehaviorManager", self.ip, self.port)
        except Exception, e:
            print self.name+" Could not create proxy to ALBehavior"
            print "Error was: ",e
            self.behavior = None

        try:
            self.battery = ALProxy("ALBattery", self.ip, self.port)
        except Exception, e:
            print self.name+" Could not create proxy to ALBattery"
            print "Error was: ",e
            self.battery = None

        # try:
            # self.audio = ALProxy("ALAudioDevice",self.ip, self.port)
        # except Exception, e:
            # print self.name+" Could not create proxy to ALAudioDevice"
            # print "Error was: ",e
            # self.audio = None

        


    def init_pos(self):

        if self.motion:
            self.motion.stopMove()
            self.motion.setStiffnesses("Body", 1.0)

        self.go_posture("Crouch")
        
        ## Enable arms control by Motion algorithm
        if self.motion:

            self.motion.setMoveArmsEnabled(True, True)

            ## Enable head to move
            self.motion.wbEnableEffectorControl("Head", True)

        ## Be start behavior
        self.restart_behavior()

        if self.motion:
            self.motion.rest()
            
    
    
    def restart_behavior(self):
    
        if self.behavior :
            if self.behavior.isBehaviorInstalled("starter-eb8f6c/behavior_1"):
                self.behavior.stopAllBehaviors()
                self.behavior.startBehavior("starter-eb8f6c/behavior_1")
            else :
                print "starter-ebf6c - behavior_1 is not installed"
        

    ### NOT use . Use of memoryEvent("PostureAsked", name ) instead
    def go_posture(self, posture_name):

        if posture_name != "Rest":
            if self.motion  :
                self.motion.stopMove()
                self.memory.raiseEvent("PostureAsked", posture_name)

        else:
            if self.motion : 
                self.motion.stopMove()
                self.motion.rest()
            print "rest !" 

        #####
        # If you just want a shortcut to reach the posture quickly when manipulating the robot
        # you can use ALRobotPostureProxy::applyPosture() (you will have to help the robot)
        #
        #Crouch,LyingBack,LyingBelly,Sit,SitRelax,Stand,StandInit,StandZero
        ##############
        
    def update_walk_to_point(self, X, Y, Theta, Speed):
        
        if Speed > 0.01 :
        
            Frequency = abs(Speed)
            if X>0 :
                self.is_walking = True
            else :
                self.is_turning = True
                
            #Bridage des nao
            #pour Lucy et Baltzar, afin de d'eviter marche destabilisante

          
            if self.name == "Lucy" and Frequency < 0.75 :
                X = X * Frequency
                Frequency = 0.75
                
                print "bridage lucy"
            if self.name == "Baltazar" and Frequency > 0.8:
                Frequency = 0.8
                print "bridage Baltzar"
                

            try:
                self.motion.stopMove()
                self.motion.setMoveArmsEnabled(True, True)
                self.motion.moveTo( X, Y, Theta, Frequency)
                
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
        




    def update_walk(self, X, Y, Theta, Speed):
   
        if Speed > 0.01 :
        
            Frequency = abs(Speed)
            if X>0 :
                self.is_walking = True
            else :
                self.is_turning = True
                
            #Bridage des nao
            #pour Lucy et Baltzar, afin de d'eviter marche destabilisante

          
            if self.name == "Lucy" and Frequency < 0.65 :
                Frequency = 0.65
                print "bridage lucy"
            if self.name == "Baltazar" and Frequency > 0.8:
                Frequency = 0.8
                print "bridage Baltzar"
                

            try:
                #motion.moveToward( X, Y, Theta, [["Frequency", Frequency]])
                self.motion.setMoveArmsEnabled(True, True)
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


    def move_head(self, yaw,pitch):

       
        if(not(self.is_headmoving) and abs(yaw * pitch)>0):

            try:
                self.motion.stiffnessInterpolation("Head", 1.0, 0.8)
            except Exception, errorMsg:
                print str(errorMsg)
            self.is_headmoving = True


        fractionMaxSpeed  = 0.35

        try:
            self.motion.setAngles("HeadYaw",yaw*3.14/180.0, fractionMaxSpeed);
            self.motion.setAngles("HeadPitch",pitch*3.14/180.0, fractionMaxSpeed);
        except Exception, errorMsg:
            print str(errorMsg)


        if(not(self.is_headmoving) and (yaw*pitch==0.0)):
            try:
                self.motion.stiffnessInterpolation("Head", 0.0, 0.4)
            except Exception, errorMsg:
                print str(errorMsg)

    
            self.is_headmoving = False

      
        #timeLists  = [[0.2], [0.2]]
        #motion.angleInterpolationBezier(names, timeLists, angleLists)

    def memoryEvent(self, name, num):

        self.memory.raiseEvent(name, num)
		
    def changeAutonomeLevel(self, isIncreasing, isReset, isStop):
	
        if(isReset):
            self.autonomeLevel = 1
            self.memory.raiseEvent("autonome", self.autonomeLevel)
            
        if(isStop):
            self.autonomeLevel = 3
            self.memory.raiseEvent("autonome", self.autonomeLevel)
            
        if( not(isReset) and not(isStop) ):
            if isIncreasing :
                self.autonomeLevel += 1
            else :
                self.autonomeLevel -= 1
                if self.autonomeLevel < 0:
                    self.autonomeLevel = 0
        self.memory.raiseEvent("autonome", self.autonomeLevel)
                

        self.lcd.display(self.autonomeLevel)	

    def changeAutonomeLevelDirect(self, level):
	
        self.memory.raiseEvent("autonome", level)
        self.lcd.display(self.autonomeLevel)	    
        
    def use_leds(self, name, value):

        # here is the light on when a nao is activated
        if name == "ear" :
            if value > 0 :
                try:
                    self.leds.on("EarLeds")
                except Exception, errorMsg:
                    print str(errorMsg)
            else:
                try:
                    self.leds.off("EarLeds")
                except Exception, errorMsg:
                    print str(errorMsg)
                    
        if name == "brain" :
            if value > 0 :
                try:
                    self.leds.on("BrainLeds")
                except Exception, errorMsg:
                    print str(errorMsg)
            else:
                try:
                    self.leds.off("BrainLeds")
                except Exception, errorMsg:
                    print str(errorMsg)

        elif name == "eye" :
            if value > 0 :
                try:
                    self.leds.on("FaceLed")                    
                except Exception, errorMsg:
                    print str(errorMsg)
            else:
                try:
                    self.leds.off("FaceLed")
                except Exception, errorMsg:
                    print str(errorMsg)
               


    #function in order to recognize the current nao remotely controlled
    def activate(self, is_activated, joy_id):
    

        if is_activated and self.leds:
            if joy_id == 1:
                self.use_leds("ear", 1)
            elif joy_id == 2:
                self.use_leds("brain", 1)
        elif self.leds :
            if joy_id ==1:
                self.use_leds("ear", 0)
            elif joy_id ==2:
                self.use_leds("brain", 0)
                                               
    # def say(self, toSay):

        # try:        
            # self.speech.say(toSay)
        # except Exception, errorMsg:
            # print str(errorMsg)
            
    def setStiffness(self, is_active):
    
        stiffness_value = 0.0
        stiffness_duration = 1.0
        if is_active:
            stiffness_value = 1.0
        
        print ("set stiffness :"+str(stiffness_value))
        self.motion.stiffnessInterpolation('Body', stiffness_value, stiffness_duration)
        
    def getStiffness(self):
    
        jointName   = "Body"
        stiffnesses = []
        try:
            stiffnesses = self.motion.getStiffnesses(jointName)
        except Exception, errorMsg:
            print str(errorMsg)
        res = 0.0
        for a in stiffnesses :
            res += a
            
        if res < 1.0 :
            self.checkBox_stiff.setCheckState(QtCore.Qt.Unchecked)
        else:
            self.checkBox_stiff.setCheckState(QtCore.Qt.Checked)
    
    
    
    ## fonction called by a timer, to check nao status ( battery, connection, stiffness ...)
    def get_status(self):
        
        #Check battery level
        batLevel = 0

        try:
            batLevel = self.battery.getBatteryCharge()
        except Exception, errorMsg:
            print str(errorMsg)
        
        #Check behavior running
        self.battery_progress.setValue(batLevel)
        
        try:

            if self.behavior.isBehaviorInstalled("main_joystick-d361da/behavior_1"):
               
                if self.behavior.isBehaviorRunning("main_joystick-d361da/behavior_1"):
                    self.radio_connect3.setChecked(QtCore.Qt.Checked)
                else:
                    self.radio_connect2.setChecked(QtCore.Qt.Checked)
        except Exception, errorMsg:
            print str(errorMsg)
            self.radio_connect1.setChecked(QtCore.Qt.Checked)
            
        #Check stiffness status
        self.getStiffness()
        
        

                
        
            

    
                

    

    