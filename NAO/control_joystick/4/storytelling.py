from PyQt4 import QtGui, QtCore

class StoryTelling(QtGui.QWidget):

    storytelling_event = QtCore.pyqtSignal(list)

    def __init__(self):
        
        super(StoryTelling, self).__init__()
        self.isRealTime = True
        
    def transmit_msg(self,l):
        res = []
        
        #Controlling nao in real time using controller, and passing trough storrytelling object
        if(self.isRealTime) :
            self.storytelling_event.emit(l)
            