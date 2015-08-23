import time
import sys
import PanTilt,PypotCreature,LeapMotion,InterfaceGroup
import Hub,Recorder

def getTime():
    if sys.platform.startswith('win'):
        return time.clock()
    else:
        return time.time()
        
def createInterface(InterfaceType):
    if InterfaceType == "PanTilt":
        newitem = PanTilt.PanTilt()
    elif InterfaceType == "PypotCreature":
        newitem = PypotCreature.PypotCreature()
    elif InterfaceType == "LeapMotion":
        newitem = LeapMotion.LeapMotion()
    elif InterfaceType == "Group":
        newitem = InterfaceGroup.InterfaceGroup()
    else:
        newitem = None
    return newitem
    
def createSystem(SystemType):
    if SystemType == "Hub":
        newitem = Hub.Hub()
    elif SystemType == "Recorder":
        newitem = Recorder.Recorder()
    else:
        newitem = None
    return newitem