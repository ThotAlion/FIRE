# -*- coding: cp1252 -*-
from nao import Nao
import pygame
import time
from pygame.locals import *
from numpy import *
import argparse

joy = None
joy_state = {}
list_of_nao = []
current_nao = None

def global_init():

    global joy, joy_state, list_of_nao, current_nao

    #### Init Joystick - PI game
    pygame.init()

    pygame.joystick.init()
    joy = pygame.joystick.Joystick(0)
    joy.init()

    print joy.get_name()
    print joy.get_init()

    joy_state = { "hat_up":False, "hat_down":False, "hat_left": False, "hat_right":False}
    joy_state["RB"]=False
    joy_state["LB"]=False
    joy_state["joy_main"] = False
    joy_state["joy_head"] = False
    joy_state["joy_turn"] = False

    ### Init list_of_nao according to the Ip and Name ###

    current_nao = 0
    list_of_nao.append( Nao("10.0.1.11", "Lucas"))
    #list_of_nao.append( Nao("10.0.1.12", "MaMa"))
    list_of_nao.append( Nao("10.0.1.13", "Lycie"))
    list_of_nao.append( Nao("10.0.1.14", "Polytech"))

    print "Nombre de nao présent: "+str(len(list_of_nao))
    for nao in list_of_nao:
        print str(nao.name)

def nao_init():
    global list_of_nao

    for nao in list_of_nao:
        nao.init_pos()

    #turn on light on activated nao
    nao_activate()


def joystick_update():

    global joy_state, joy
    
    for event in pygame.event.get():
        
        if pygame.joystick.get_count() > 0:
            if event.type == pygame.locals.JOYBUTTONDOWN:

                ###### BOUTON RB - LB #########

                joy_state["RB"] = joy.get_button(5)
                joy_state["LB"] = joy.get_button(4)
    
                if joy.get_button(5):
                    
                    joy_state["RB"] = True
                    if joy_state["LB"]:
                        nao_switch_all()
                    else:
                        nao_switch(True)
                        
                else:
                    joy_state["RB"]=False
                    

                if joy.get_button(4):
                    
                    joy_state["LB"] = True
                    if joy_state["RB"]:
                        nao_switch_all()
                    else:
                        nao_switch(False)
                        
                else:
                    joy_state["LB"]=False
                    

                ###### BOUTON DE MANETTE #########

                if joy.get_button(3):

                    if joy_state["hat_up"]:
                        print "Y up  Play sound"
                        nao_memoryEvent("PlaySound", 0)
                    elif joy_state["hat_down"]:
                        print " Y down  s assoir"
                        nao_go_posture("Stand")
                    elif joy_state["hat_left"]:
                        print " Y left setFps :20  "
                        nao_memoryEvent("SetFps", 20)
                    elif joy_state["hat_right"]:
                        print "Y right anim cote"
                        nao_memoryEvent("anim", 3)
                        
                    else :
                        print "Yplay Cun torsion"
                        nao_memoryEvent("anim", 1)
                        

                if joy.get_button(2):
                    if joy_state["hat_up"]:
                        print "X up Play sound"
                        nao_memoryEvent("PlaySound", 1)
                    elif joy_state["hat_down"]:
                        print " X down position Crouch"
                        nao_go_posture("Rest")
                    elif joy_state["hat_left"]:
                        print " X left set fps 12"
                        nao_memoryEvent("anim", 9)
                    elif joy_state["hat_right"]:
                        print "X right anim clavier"
                        nao_memoryEvent("anim", 5)
                        
                    else :
                        print "X animation 2 bow"
                        nao_memoryEvent("anim", 2)

                if joy.get_button(1):
                    if joy_state["hat_up"]:
                        print "B up Led couleur 3"
                        nao_leds("rasta", 2)
                    elif joy_state["hat_down"]:
                        print " B down position stand init"
                        nao_go_posture("StandInit")
                    elif joy_state["hat_left"]:
                        print " B left set FPS 25"
                        nao_memoryEvent("SetFps", 25)
                    elif joy_state["hat_right"]:
                        print "B right anim 7 Salut A"
                        nao_memoryEvent("anim", 7)
                    else :
                        print "B animation 8 ronde"
                        nao_memoryEvent("anim", 9)

                if joy.get_button(0):
                    if joy_state["hat_up"]:
                        print "A up Led couleur 4"
                        nao_leds("ear",0 )
                    elif joy_state["hat_down"]:
                        print " A down s'assoir"
                        nao_go_posture("Sit")
                    elif joy_state["hat_left"]:
                        print " A left Set FPS 30"
                        nao_memoryEvent("SetFps", 30)
                    elif joy_state["hat_right"]:
                        print "A right anim pyramide"
                        nao_memoryEvent("anim", 6)
                    else :
                        print "A animation 4 clavier"
                        nao_memoryEvent("anim", 4)

            
            if event.type == pygame.locals.JOYAXISMOTION:

                ###### JOYSTICK MARCHE #########
                # axis 1, avant (-1) arriere (1), axis 0, gauche (-1), droite (1)
                if abs(joy.get_axis(1)) + abs( joy.get_axis(0)) < 0.18 :
                    if joy_state["joy_main"]:
                        print "stop"
                        nao_update_walk(0.0, 0.0, 0.0, 0.0)
                        joy_state["joy_main"] = False
                    
                else:
                    ax1= joy.get_axis(1)
                    ax0= joy.get_axis(0)
                    print "avance "+str(ax1)+ " - "+str(ax0)
                    joy_state["joy_main"] = True
                    nao_update_walk(abs(ax1)/(-ax1),0.0, -ax0*0.75, abs(ax1))
                


                ###### LT - RT ROTATION DU ROBOT #########
                if abs(joy.get_axis(2))>0.1:
                    ax2 = joy.get_axis(2)
                    joy_state["joy_turn"] = True

                    if(ax2 > 0 ) :
                        
                        print"LT "+str(ax2)
                        nao_update_walk(0.0,0.0,0.9 , ax2)
                    else:
                        print"RT "+str(joy.get_axis(2))
                        nao_update_walk(0.0,0.0,-0.9 , abs(ax2))

                    
                else :
                    if joy_state["joy_turn"]:
                        print("Stop turning")
                        joy_state["joy_turn"] = False
                        nao_update_walk(0.0, 0.0, 0.0, 0.0)
        
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

            ###### JOYSTICK HAT #########
            if event.type == pygame.locals.JOYHATMOTION:
                (a,b) = joy.get_hat(0)
                if a > 0.2 :
                    #print "hat right"
                    joy_state["hat_right"] = True
                else:
                    joy_state["hat_right"] = False
                if a < -0.2 :
                    #print "hat left"
                    joy_state["hat_left"] = True
                else:
                    joy_state["hat_left"] = False
                if b > 0.2 :
                    #print "hat up"
                    joy_state["hat_up"] = True
                else :
                    joy_state["hat_up"] = False
                if b < -0.2 :
                    #print "hat down"
                    joy_state["hat_down"] = True
                else:
                    joy_state["hat_down"]= False


def nao_go_posture(posture_name):
    global current_nao, list_of_nao
    #posture using choregraphe, to avoid waiting time.
    # using memoryEvent, instead of go_to_posture method
    
    if current_nao>-1:
        list_of_nao[current_nao].memoryEvent("PostureAsked",posture_name)
    else:
        for nao in list_of_nao:
            nao.memoryEvent("PostureAsked",posture_name)
        

def nao_update_walk(X, Y, Theta, Speed):
    global current_nao, list_of_nao

    if current_nao>-1:
        list_of_nao[current_nao].update_walk(X, Y, Theta, Speed)
    else:
        for nao in list_of_nao:
            nao.update_walk(X, Y, Theta, Speed)

def nao_move_head(yaw,pitch):
    global current_nao, list_of_nao
    
    if current_nao>-1:
        list_of_nao[current_nao].move_head(yaw,pitch)
    else:
        for nao in list_of_nao:
            nao.move_head(yaw,pitch)

def nao_memoryEvent(name, num):
    global current_nao, list_of_nao

    if current_nao>-1:
        list_of_nao[current_nao].memoryEvent(name, num)
    else:
        for nao in list_of_nao:
            nao.memoryEvent(name, num)
            
def nao_leds(name, value):
    global current_nao, list_of_nao

    if current_nao>-1:
        list_of_nao[current_nao].use_leds(name, value)
    else:
        for nao in list_of_nao:
            nao.use_leds(name, value)

def nao_say(toSay):
    global current_nao, list_of_nao

    if current_nao>-1:
        list_of_nao[current_nao].say(toSay)
    else:
        for nao in list_of_nao:
            nao.say(toSay)

def nao_switch(is_increasing):
    global current_nao, list_of_nao

    if current_nao<0:
        current_nao = 0

    else:
        if is_increasing:
            current_nao += 1
            current_nao = current_nao%len(list_of_nao)
        else:
            current_nao -= 1
            if current_nao < 0:
                current_nao = len(list_of_nao) - 1

    nao_activate()

def nao_switch_all():
    global current_nao, list_of_nao

    current_nao = -1
    nao_activate()
    print "Active them all!"

def nao_activate():
    global list_of_nao, current_nao

    print "nao courrant: "+str(current_nao)+" : "+list_of_nao[current_nao].name

    #active only one nao
    for a in range(len(list_of_nao)):
        list_of_nao[a].activate(a==current_nao or current_nao==-1)



def is_current_nao_walking():
    global current_nao, list_of_nao

    return list_of_nao[current_nao].is_walking

def is_current_nao_turning():
    global current_nao, list_of_nao

    return list_of_nao[current_nao].is_turning

def is_current_nao_headmoving():
    global current_nao, list_of_nao

    return list_of_nao[current_nao].is_headmoving





def main(robotPresent):
    global_init()
    time.sleep(2)
    nao_init()

    time.sleep(1)
    while 1:
        joystick_update()
        time.sleep(0.01)



    


    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--nb", type=int, default=0x00000000,
                        help="list des robots presents")

    args = parser.parse_args()
    main(args.nb)
