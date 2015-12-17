
import time
import pygame
from pygame.locals import *
from PyQt4 import QtGui, QtCore
import os



class Joystick(QtCore.QThread):

    joy_event = QtCore.pyqtSignal(list)

    def __init__(self,parent=None):

        QtCore.QThread.__init__(self, parent)
        self.parent=parent
        self.exiting = False

        self.joy_state= {}
        self.id = 0

        self.start()


    def __del__(self):
        self.exiting = True
        self.wait()

    def init_joy_state(self):

        self.joy_state["hat_up"] = False
        self.joy_state["hat_down"] = False
        self.joy_state["hat_right"] = False
        self.joy_state["hat_left"] = False
        self.joy_state["RB"]=False
        self.joy_state["LB"]=False
        self.joy_state["joy_main"] = False
        self.joy_state["joy_head"] = False
        self.joy_state["joy_turn"] = False

    def run(self):

        os.environ["SDL_VIDEODRIVER"] = "dummy"
        pygame.init()
        pygame.joystick.init()
        try :
            self.joy = pygame.joystick.Joystick(0)
            self.joy.init()
            print "---- Init Joystick ID = "+str(self.id)
            print self.joy.get_name()
            print self.joy.get_init()
        except :
            print "error"

        done = False

        self.init_joy_state()

        while done==False:
        
            res = []

            for event in pygame.event.get():

                if pygame.joystick.get_count() > 0:
                    if event.type == pygame.locals.JOYBUTTONDOWN:

                        ###### BOUTON RB - LB #########

                        self.joy_state["RB"] = self.joy.get_button(5)
                        self.joy_state["LB"] = self.joy.get_button(4)
            
                        if self.joy_state["RB"]:
                            
                            if self.joy_state["LB"]:
                                res.append(["LB+RB", 0,0])
                            else:
                                res.append(["RB", 0,0])                 

                        if self.joy_state["LB"]:
                            
                            if self.joy_state["RB"]:
                                res.append(["LB+RB",0, 0])
                            else:
                                res.append(["LB",0, 0])


                        ###### BOUTON DE MANETTE ########
                        self.joy_state["Y"] = self.joy.get_button(3)
                        self.joy_state["X"] = self.joy.get_button(2)
                        self.joy_state["B"] = self.joy.get_button(1)
                        self.joy_state["A"] = self.joy.get_button(0)

                        if self.joy_state["hat_up"]:

                            if self.joy_state["Y"]:
                                res.append(["UP_Y",0, 0])
                            if self.joy_state["X"]:
                                res.append(["UP_X",0, 0])
                            if self.joy_state["B"]:
                                res.append(["UP_B",0, 0])
                            if self.joy_state["A"]:
                                res.append(["UP_A",0, 0])

                        elif self.joy_state["hat_down"]:

                            if self.joy_state["Y"]:
                                res.append(["DOWN_Y",0, 0])
                            if self.joy_state["X"]:
                                res.append(["DOWN_X",0, 0])
                            if self.joy_state["B"]:
                                res.append(["DOWN_B",0, 0])
                            if self.joy_state["A"]:
                                res.append(["DOWN_A",0, 0])

                        elif self.joy_state["hat_left"]:

                            if self.joy_state["Y"]:
                                res.append(["LEFT_Y",0, 0])
                            if self.joy_state["X"]:
                                res.append(["LEFT_X",0, 0])
                            if self.joy_state["B"]:
                                res.append(["LEFT_B",0, 0])
                            if self.joy_state["A"]:
                                res.append(["LEFT_A",0, 0])

                        elif self.joy_state["hat_right"]:

                            if self.joy_state["Y"]:
                                res.append(["RIGHT_Y",0, 0])
                            if self.joy_state["X"]:
                                res.append(["RIGHT_X",0, 0])
                            if self.joy_state["B"]:
                                res.append(["RIGHT_B",0, 0])
                            if self.joy_state["A"]:
                                res.append(["RIGHT_A",0, 0])

                        elif self.joy_state["RB"]:

                            if self.joy_state["Y"]:
                                res.append(["RB_Y",0, 0])
                            if self.joy_state["X"]:
                                res.append(["RB_X",0, 0])
                            if self.joy_state["B"]:
                                res.append(["RB_B",0, 0])
                            if self.joy_state["A"]:
                                res.append(["RB_A",0, 0])

                        elif self.joy_state["LB"]:

                            if self.joy_state["Y"]:
                                res.append(["LB_Y",0, 0])
                            if self.joy_state["X"]:
                                res.append(["LB_X",0, 0])
                            if self.joy_state["B"]:
                                res.append(["LB_B",0, 0])
                            if self.joy_state["A"]:
                                res.append(["LB_A",0, 0])

                        else:

                            if self.joy_state["Y"]:
                                res.append(["Y",0, 0])
                            if self.joy_state["X"]:
                                res.append(["X",0, 0])
                            if self.joy_state["B"]:
                                res.append(["B",0, 0])
                            if self.joy_state["A"]:
                                res.append(["A",0, 0])

                    if event.type == pygame.locals.JOYAXISMOTION:

                        ###### JOYSTICK MARCHE #########
                        # axis 1, avant (-1) arriere (1), axis 0, gauche (-1), droite (1)
                        ################################

                        if abs(self.joy.get_axis(1)) + abs( self.joy.get_axis(0)) < 0.18 :
                            if self.joy_state["joy_main"]:                        
                                self.joy_state["joy_main"] = False
                                res.append(["JOY_MAIN", 0, 0])
                            
                        else:
                            ax1= self.joy.get_axis(1)
                            ax0= self.joy.get_axis(0)
                            self.joy_state["joy_main"] = True
                            if self.joy_state["hat_up"]:
                                res.append(["UP_JOY_MAIN", -ax0, -ax1])
                            elif self.joy_state["hat_left"] or self.joy_state["hat_right"]:
                                res.append(["LEFT_JOY_MAIN", -ax0, -ax1])
                            else :
                                res.append(["JOY_MAIN", -ax0, -ax1])


                        ###### LT - RT ROTATION DU ROBOT #########
                        if abs(self.joy.get_axis(2))>0.1:
                            ax2 = self.joy.get_axis(2)
                            self.joy_state["joy_turn"] = True

                            if(ax2 > 0 ) :
                                res.append(["LT", ax2,0])
                                
                            else:
                                res.append(["RT", ax2,0])

                            
                        else :
                            if self.joy_state["joy_turn"]:
                                res.append(["RT", 0,0])
                                res.append(["LT", 0,0])
                                self.joy_state["joy_turn"] = False

                
                        ###### JOYSTICK TETE #########
                        if abs(self.joy.get_axis(3)) + abs(self.joy.get_axis(4)) < 0.18 :
                            if self.joy_state["joy_head"]:
                                self.joy_state["joy_head"] = False
                                res.append(["JOY_SEC", 0,0])
                        # axis 3 (up -1, down 1) acix 4 (-1 left, 1 right )                       res.apppend(["joy_head", 0, 0])


                        else:
                            ax3 = self.joy.get_axis(3)
                            ax4 = self.joy.get_axis(4)                
                            self.joy_state["joy_head"] = True
                            res.append(["JOY_SEC", ax4, -ax3])
                        # axis 3 (up -1, down 1) acix 4 (-1 left, 1 right )


                            ###### JOYSTICK HAT #########
                    if event.type == pygame.locals.JOYHATMOTION:
                        (a,b) = self.joy.get_hat(0)
                        if a > 0.2 :
                            self.joy_state["hat_right"] = True
                        else:
                            self.joy_state["hat_right"] = False
                        if a < -0.2 :
                            self.joy_state["hat_left"] = True
                        else:
                            self.joy_state["hat_left"] = False
                        if b > 0.2 :
                            self.joy_state["hat_up"] = True
                        else :
                            self.joy_state["hat_up"] = False
                        if b < -0.2 :
                            self.joy_state["hat_down"] = True
                        else:
                            self.joy_state["hat_down"]= False
            #######
            #If something is pressed, the the Qt Signal
            #######
            if len(res)>0:
                self.joy_event.emit(res)
                            
