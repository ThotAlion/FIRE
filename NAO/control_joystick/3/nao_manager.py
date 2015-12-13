from nao import Nao
from PyQt4 import QtGui, QtCore

class Nao_manager(QtGui.QWidget):

    def __init__(self):

        super(Nao_manager, self).__init__()

        ## NAO MANAGEMENT
        self.list_of_nao = []
        self.selection = []

        ## GUI
        self.layout1 = QtGui.QGridLayout()
        self.setLayout(self.layout1)
        self.setWindowTitle("Multiple Nao xbox controller")


    def addNao(self, name, adresseIP, port ):
        naoId = len(self.list_of_nao)
        nao = Nao(adresseIP, name, naoId)

        self.layout1.addWidget(nao, 0, naoId)
        self.list_of_nao.append(nao)
        self.selection.append(False)

    def init_nao(self):

        for nao in self.list_of_nao :
            nao.init_pos()

    def init_manager(self):

        if len(self.list_of_nao) != len(self.selection) :
            print( " probleme nao manager init ")
        else :
            self.init_nao()
            return True


    # switching from select all to unselect all
    def selectAll(self):

        is_all_selected = True
        for is_activated in self.selection:
            is_all_selected = is_all_selected and is_activated
        
        
        for is_activated in self.selection:
            is_activated = not(is_all_selected)
        self.activateNao()
   

    # select only one nao, switching from one to the other
    def selectSwitch(self, isIncreasing ):

        print "manager:selectSwitch"
        #find the last nao activated
        last_id = 0
        current_id = 0
        for is_selected in self.selection:
            if is_selected:
                last_id = current_id
            current_id += 1

        for i in range(len(self.selection)):
            self.selection[i] = ( ((last_id + 1)%len(self.selection))==i )

        self.activateNao()
                

    # select or unselect one nao, over the current selection, according to its ID
    def select(self, isSelecting, nao_id ):

        if nao_id>-1 and nao_id< len(self.list_of_nao):
            self.selection[nao_id] = isSelecting

        self.activateNao()

        

    # return True if a nao is selected
    def is_selected(self, nao_id):
        if nao_id>-1 and nao_id< len(self.list_of_nao):
            return[nao_id] 

            

    # activate some or all nao according to selection list
    def activateNao(self):
    

        for a in range(len(self.list_of_nao)):
            (self.list_of_nao[a]).activate( self.selection[a] )

    # call a memory event to all selected nao
    def nao_memoryEvent(self, name, arg ):

        for i in range(len(self.list_of_nao)):
            if self.selection[i]:
                self.list_of_nao[i].memoryEvent(name, arg)

    # update_walk and turning to all selected nao
    def nao_update_walk(self, X, Y, Theta, Speed):

        for i in range(len(self.list_of_nao)):
            if self.selection[i]:
                self.list_of_nao[i].update_walk(self, X, Y , Theta, Speed)

        print "marche X="+str(X)+" Y="+str(Y)+" Theta="+str(Theta)+" Speed="+str(Speed)+""

    # update turning head to all selected nao
    def nao_move_head(self, yaw,pitch):

        for i in range(len(self.list_of_nao)):
            if self.selection[i]:
                self.list_of_nao[i].move_head(yaw,pitch)

    # ask a posture to all selected nao
    def nao_go_posture(self, posture_name):

        for i in range(len(self.list_of_nao)):
            if self.selection[i]:
                self.list_of_nao[i].go_posture(self, posture_name)
        


    ####################################################################    
    # transmit message from interpret to itself and all selected nao(s).
    # Contains all dictionnary message and functions calls
    ####################################################################
    def transmit_msg(self, msgGlobal):

        
        
        for msg in msgGlobal:


            if(len(msg)==3):

                name = msg[0]
                arg1 = msg[1]
                arg2 = msg[2]


                #### SELECTION ####
                if   name == "SWITCH" :
                    self.selectSwitch(arg1==1)
                elif name == "SELECT_ALL" :
                    self.selectedAll()
                elif name == "SELECT":
                    self.select(True, arg1 )
                elif name == "UNSELECT":
                    self.select(False, arg1 )


                ### MOTION  ######
                elif name == "ANIM":
                    self.nao_memoryEvent("anim", arg1 )
                    
                elif name == "POSTURE":
                    self.nao_memoryEvent("PostureAsked" ,arg1)

                elif name == "WALK": #arg1 left<0 right>0 -- arg2 up>0 down<0
                    if arg1==0.0 and arg2==0.0 :
                        self.nao_update_walk(0,0,0.0,0.0)
                    else :
                        self.nao_update_walk( abs(arg2)/(arg2), 0.0, arg1*0.70, abs(arg2))
                    
                elif name == "TURN":

                    if(arg1==0):
                        self.nao_update_walk(0.0,0.0,0.0, 0.0)
                    elif arg1 > 0.0:
                        self.nao_update_walk(0.0,0.0,0.9, arg1)
                    elif arg1 < 0.0:
                        self.nao_update_walk(0.0,0.0,-0.9, abs(arg1))

                    
                elif name == "HEAD": #arg1 left<0 right>0 --- arg2 up>0, down<0

                    self.nao_move_head(arg1*40.5, arg2*29.5)

                ### OTHERS #######

                elif name == "FPS":
                    self.nao_memoryEvent("SetFps", arg1)
                    
                elif name == "LEDS":
                    self.nao_memoryEvent("SetLeds", arg1)

                elif name == "PLAY_SOUND":
                    self.nao_memoryEvent("PlaySound", arg1)

            

                
            

            

                        
        
         
