import time
import pygame
from pygame.locals import *



class Joystick:

    def __init__(self, joystickID):

        self.joy_state= {}
        self.id = joystickID

        pygame.init()
        pygame.joystick.init()
        self.joy = pygame.joystick.Joystick(0)
        self.joy.init()

        print "---- Init Joystick ID = "+str(self.id)
        print joy.get_name()
        print joy.get_init()

        self.init_joy_state()

    def init_joy_state(self):

    def update(self):

        res = []

        for event in pygame.event.get():

            if pygame.joystick.get_count() > 0:
                if event.type == pygame.locals.JOYBUTTONDOWN:

                    ###### BOUTON RB - LB #########

                    self.joy_state["RB"] = self.joy.get_button(5)
                    self.joy_state["LB"] = self.joy.get_button(4)
        
                    if self.joy_state["RB"]:
                        
                        if self.joy_state["LB"]:
                            res.append(["LB+RB", 0])
                        else:
                            res.append(["RB", 0])                 

                    if self.joy_state["LB"]:
                        
                        if joy_state["RB"]:
                            res.append(["LB+RB", 0])
                        else:
                            res.append(["LB", 0])


                    ###### BOUTON DE MANETTE ########
                    self.joy_state["Y"] = self.joy.get_button(3)
                    self.joy_state["X"] = self.joy.get_button(2)
                    self.joy_state["B"] = self.joy.get_button(1)
                    self.joy_state["A"] = self.joy.get_button(0)

                    if self.joy_state["hat_up"]:

                        if self.joy_state["Y"]:
                            res.append(["UP_Y", 0])
                        if self.joy_state["X"]:
                            res.append(["UP_X", 0])
                        if self.joy_state["B"]:
                            res.append(["UP_B", 0])
                        if self.joy_state["A"]:
                            res.append(["UP_A", 0])

                    elif self.joy_state["hat_down"]:

                        if self.joy_state["Y"]:
                            res.append(["DOWN_Y", 0])
                        if self.joy_state["X"]:
                            res.append(["DOWN_X", 0])
                        if self.joy_state["B"]:
                            res.append(["DOWN_B", 0])
                        if self.joy_state["A"]:
                            res.append(["DOWN_A", 0])

                    elif self.joy_state["hat_left"]:

                        if self.joy_state["Y"]:
                            res.append(["LEFT_Y", 0])
                        if self.joy_state["X"]:
                            res.append(["LEFT_X", 0])
                        if self.joy_state["B"]:
                            res.append(["LEFT_B", 0])
                        if self.joy_state["A"]:
                            res.append(["LEFT_A", 0])

                    elif self.joy_state["hat_right"]:

                        if self.joy_state["RIGHT_Y"]:
                            res.append(["RIGHT_Y", 0])
                        if self.joy_state["X"]:
                            res.append(["RIGHT_X", 0])
                        if self.joy_state["B"]:
                            res.append(["RIGHT_B", 0])
                        if self.joy_state["A"]:
                            res.append(["RIGHT_A", 0])

                    else:

                        if self.joy_state["Y"]:
                            res.append(["Y", 0])
                        if self.joy_state["X"]:
                            res.append(["X", 0])
                        if self.joy_state["B"]:
                            res.append(["B", 0])
                        if self.joy_state["A"]:
                            res.append(["A", 0])

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
                    res.append(["JOY_MAIN", ax1, ax0])


                ###### LT - RT ROTATION DU ROBOT #########
                if abs(self.joy.get_axis(2))>0.1:
                    ax2 = joy.get_axis(2)
                    self.joy_state["joy_turn"] = True

                    if(ax2 > 0 ) :
                        res.append["LT", ax2]
                        
                    else:
                        res.append["RT", -ax2]

                    
                else :
                    if joy_state["joy_turn"]:
                        res.append["RT", 0]
                        res.append["LT", 0]
                        joy_state["joy_turn"] = False

        
                ###### JOYSTICK TETE #########
                if abs(joy.get_axis(3)) + abs(joy.get_axis(4)) < 0.18 :
                    if joy_state["joy_head"]:
                        print "stop move head"
                        joy_state["joy_head"] = False
                        nao_move_head(0.0,0.0)

                else:
                    ax3 = joy.get_axis(3)
                    ax4 = joy.get_axis(4)                
                    print "move head "+str(ax3)+" - "+str(ax4)
                    joy_state["joy_head"] = True
                    nao_move_head(-ax4*40.5, -ax3*29.5)
                # axis 3 (up -1, down 1) acix 4 (-1 left, 1 right )
                            
                            
                        
                        
