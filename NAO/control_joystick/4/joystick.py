
import time
import pygame
from pygame.locals import *
from PyQt4 import QtGui, QtCore
import os



class Joystick(QtCore.QThread):

    joy_event1 = QtCore.pyqtSignal(list)
    view_event1 = QtCore.pyqtSignal(str)
    joy_event2 = QtCore.pyqtSignal(list)
    view_event2 = QtCore.pyqtSignal(str)
    second_joy_detected = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):

        QtCore.QThread.__init__(self, parent)
        self.parent=parent
        self.exiting = False

        self.list_of_joy_state =[]
        self.joy_state= {}
        self.joy_state2= {}
        self.list_of_joy = []


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
        
    def emit_view_event(self, name, id):
    
        if id == 0 :
            self.view_event1.emit(name)
        if id == 1 :
            self.view_event2.emit(name)
        

    def run(self):

        os.environ["SDL_VIDEODRIVER"] = "dummy"
        pygame.init()
        
        ## Sleep, wait for the main programm running a bit
        time.sleep(2)
        
        ## Init Joystick
        pygame.joystick.init()
        for j in range(pygame.joystick.get_count()):
        
            joy = pygame.joystick.Joystick(j)
            joy.init()
            self.list_of_joy.append(joy)
            
            print "---- Init Joystick ID = "
            print joy.get_name()
            
            ##if second joystick detected##
            if(j==1):
                self.second_joy_detected.emit(1)
                print "SECOND JOYSTICK DETECTED"
            

        done = False
        
        ##Init the list of dictionnary

        self.init_joy_state()
        for j in range(pygame.joystick.get_count()):
            self.list_of_joy_state.append(self.joy_state.copy())

        ## Loop of joystick
        while done==False:
        
            res = []
            for j in range(pygame.joystick.get_count()):
                res.append([])
            
            count = 0

            for event in pygame.event.get():

                count += 1
                

                if pygame.joystick.get_count() > 0:
                
                    if event.type == pygame.locals.JOYBUTTONDOWN:

                        ###### BOUTON RB - LB #########

                        for j in range(pygame.joystick.get_count()):
                        
                            self.list_of_joy_state[j]["RB"] = self.list_of_joy[j].get_button(5)
                            if self.list_of_joy_state[j]["LB"] and not(self.list_of_joy[j].get_button(4)):
                                self.emit_view_event("none", j)
                            
                            self.list_of_joy_state[j]["LB"] = self.list_of_joy[j].get_button(4)
                            
                            
                
                            if self.list_of_joy_state[j]["RB"]:
                                
                                if self.list_of_joy_state[j]["LB"]:
                                    res[j].append(["LB+RB", 0,0])
                                else:
                                    res[j].append(["RB", 0,0])                 

                            if self.list_of_joy_state[j]["LB"]:
                                
                                if self.list_of_joy_state[j]["RB"]:
                                    res[j].append(["LB+RB",0, 0])
                                else:
                                    res[j].append(["LB",0, 0])
                                    self.emit_view_event("lb", j)
                                   


                        ###### BOUTON DE MANETTE ########
                        
                        for j in range(pygame.joystick.get_count()): 
                            
                            self.list_of_joy_state[j]["Y"] = self.list_of_joy[j].get_button(3)
                            self.list_of_joy_state[j]["X"] = self.list_of_joy[j].get_button(2)
                            self.list_of_joy_state[j]["B"] = self.list_of_joy[j].get_button(1)
                            self.list_of_joy_state[j]["A"] = self.list_of_joy[j].get_button(0)

                            if self.list_of_joy_state[j]["hat_up"]:

                                if self.list_of_joy_state[j]["Y"]:
                                    res[j].append(["UP_Y",0, 0])
                                if self.list_of_joy_state[j]["X"]:
                                    res[j].append(["UP_X",0, 0])
                                if self.list_of_joy_state[j]["B"]:
                                    res[j].append(["UP_B",0, 0])
                                if self.list_of_joy_state[j]["A"]:
                                    res[j].append(["UP_A",0, 0])

                            elif self.list_of_joy_state[j]["hat_down"]:

                                if self.list_of_joy_state[j]["Y"]:
                                    res[j].append(["DOWN_Y",0, 0])
                                if self.list_of_joy_state[j]["X"]:
                                    res[j].append(["DOWN_X",0, 0])
                                if self.list_of_joy_state[j]["B"]:
                                    res[j].append(["DOWN_B",0, 0])
                                if self.list_of_joy_state[j]["A"]:
                                    res[j].append(["DOWN_A",0, 0])

                            elif self.list_of_joy_state[j]["hat_left"]:

                                if self.list_of_joy_state[j]["Y"]:
                                    res[j].append(["LEFT_Y",0, 0])
                                if self.list_of_joy_state[j]["X"]:
                                    res[j].append(["LEFT_X",0, 0])
                                if self.list_of_joy_state[j]["B"]:
                                    res[j].append(["LEFT_B",0, 0])
                                if self.list_of_joy_state[j]["A"]:
                                    res[j].append(["LEFT_A",0, 0])

                            elif self.list_of_joy_state[j]["hat_right"]:

                                if self.list_of_joy_state[j]["Y"]:
                                    res[j].append(["RIGHT_Y",0, 0])
                                if self.list_of_joy_state[j]["X"]:
                                    res[j].append(["RIGHT_X",0, 0])
                                if self.list_of_joy_state[j]["B"]:
                                    res[j].append(["RIGHT_B",0, 0])
                                if self.list_of_joy_state[j]["A"]:
                                    res[j].append(["RIGHT_A",0, 0])

                            elif self.list_of_joy_state[j]["RB"]:

                                if self.list_of_joy_state[j]["Y"]:
                                    res[j].append(["RB_Y",0, 0])
                                if self.list_of_joy_state[j]["X"]:
                                    res[j].append(["RB_X",0, 0])
                                if self.list_of_joy_state[j]["B"]:
                                    res[j].append(["RB_B",0, 0])
                                if self.list_of_joy_state[j]["A"]:
                                    res[j].append(["RB_A",0, 0])

                            elif self.list_of_joy_state[j]["LB"]:

                                if self.list_of_joy_state[j]["Y"]:
                                    res[j].append(["LB_Y",0, 0])
                                if self.list_of_joy_state[j]["X"]:
                                    res[j].append(["LB_X",0, 0])
                                if self.list_of_joy_state[j]["B"]:
                                    res[j].append(["LB_B",0, 0])
                                if self.list_of_joy_state[j]["A"]:
                                    res[j].append(["LB_A",0, 0])

                            else:

                                if self.list_of_joy_state[j]["Y"]:
                                    res[j].append(["Y",0, 0])
                                if self.list_of_joy_state[j]["X"]:
                                    res[j].append(["X",0, 0])
                                if self.list_of_joy_state[j]["B"]:
                                    res[j].append(["B",0, 0])
                                if self.list_of_joy_state[j]["A"]:
                                    res[j].append(["A",0, 0])

                    if event.type == pygame.locals.JOYAXISMOTION:

                        ###### JOYSTICK MARCHE #########
                        # axis 1, avant (-1) arriere (1), axis 0, gauche (-1), droite (1)
                        ################################
                       
                        joy_threshold = 0.32
                        
                        for j in range(pygame.joystick.get_count()):

                            if abs(self.list_of_joy[j].get_axis(1)) + abs( self.list_of_joy[j].get_axis(0)) < joy_threshold :
                                if self.list_of_joy_state[j]["joy_main"]:                        
                                    self.list_of_joy_state[j]["joy_main"] = False
                                    res[j].append(["JOY_MAIN", 0, 0])
                                
                            else:
                                ax1= self.list_of_joy[j].get_axis(1)
                                ax0= self.list_of_joy[j].get_axis(0)
                                self.list_of_joy_state[j]["joy_main"] = True
                                if self.list_of_joy_state[j]["hat_up"]:
                                    res[j].append(["UP_JOY_MAIN", -ax0, -ax1])
                                elif self.list_of_joy_state[j]["hat_left"] or self.list_of_joy_state[j]["hat_right"]:
                                    res[j].append(["LEFT_JOY_MAIN", -ax0, -ax1])
                                else :
                                    res[j].append(["JOY_MAIN", -ax0, -ax1])


                            ###### LT - RT ROTATION DU ROBOT #########
                            if abs(self.list_of_joy[j].get_axis(2))>0.1:
                                ax2 = self.list_of_joy[j].get_axis(2)
                                self.list_of_joy_state[j]["joy_turn"] = True

                                if(ax2 > 0 ) :
                                    res[j].append(["LT", ax2,0])
                                    
                                else:
                                    res[j].append(["RT", ax2,0])

                                
                            else :
                                if self.list_of_joy_state[j]["joy_turn"]:
                                    res[j].append(["RT", 0,0])
                                    res[j].append(["LT", 0,0])
                                    self.list_of_joy_state[j]["joy_turn"] = False

                    
                            ###### JOYSTICK TETE #########
                            joyHead_threshold = 0.25
                            
                            if abs(self.list_of_joy[j].get_axis(3)) + abs(self.list_of_joy[j].get_axis(4)) < joyHead_threshold :
                                if self.list_of_joy_state[j]["joy_head"]:
                                    self.list_of_joy_state[j]["joy_head"] = False
                                    res[j].append(["JOY_SEC", 0,0])
                            # axis 3 (up -1, down 1) acix 4 (-1 left, 1 right ) 


                            else:
                                ax3 = self.list_of_joy[j].get_axis(3)
                                ax4 = self.list_of_joy[j].get_axis(4)                
                                self.list_of_joy_state[j]["joy_head"] = True
                                res[j].append(["JOY_SEC", ax4, -ax3])
                            # axis 3 (up -1, down 1) acix 4 (-1 left, 1 right )


                            ###### JOYSTICK HAT #########
                    if event.type == pygame.locals.JOYHATMOTION:
                    
                        for j in range(pygame.joystick.get_count()):
                    
                            (a,b) = self.list_of_joy[j].get_hat(0)
                            if a > 0.2 :
                                self.list_of_joy_state[j]["hat_right"] = True
                                self.emit_view_event("right", j)
                            else:
                                self.list_of_joy_state[j]["hat_right"] = False
                                
                            if a < -0.2 :
                                self.list_of_joy_state[j]["hat_left"] = True
                                self.emit_view_event("left", j)
                            else:
                                self.list_of_joy_state[j]["hat_left"] = False
                                
                            if b > 0.2 :
                                self.list_of_joy_state[j]["hat_up"] = True
                                self.emit_view_event("up", j)
                            else :
                                self.list_of_joy_state[j]["hat_up"] = False
                                
                            if b < -0.2 :
                                self.list_of_joy_state[j]["hat_down"] = True
                                self.emit_view_event("down", j)
                            else:
                                self.list_of_joy_state[j]["hat_down"]= False
                                
                            if not(self.list_of_joy_state[j]["hat_up"] or self.list_of_joy_state[j]["hat_left"] or self.list_of_joy_state[j]["hat_right"] or self.list_of_joy_state[j]["hat_down"] ):
                                self.emit_view_event("none", j)

            #######
            #If something is pressed, the the Qt Signal
            #######
            for a in range(len(res)):
            
                if a==0 and len(res[a])>0 :
            
                    self.joy_event1.emit(res[a])
                    #print "emit 1"
                elif a==1 and len(res[a])>0 :
                
                    self.joy_event2.emit(res[a])
                    #print "emit 2"
                    

            time.sleep(0.07)
                            
