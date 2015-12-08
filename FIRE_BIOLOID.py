import sys
import FIRELIB
import time
from PyQt4.QtGui import *
from PyQt4.QtCore import *

styleFile = QFile("FIRELIB\CSS\styleSheet.txt")
styleFile.open(styleFile.ReadOnly)
style = str(styleFile.readAll())
app = QApplication(sys.argv)
app.setStyleSheet(style)

members = {}
members["head"] = ['head_z','head_y']
members["left arm"] =  ["l_shoulder_y", "l_shoulder_x","l_elbow_x"]
members["right arm"] = ["r_shoulder_y", "r_shoulder_x","r_elbow_x"]
members["left leg"] =  ["l_hip_z", "l_hip_x","l_hip_y","l_knee_y","l_ankle_y","l_ankle_x"]
members["right leg"] = ["r_hip_z", "r_hip_x","r_hip_y","r_knee_y","r_ankle_y","r_ankle_x"]


interfaces = FIRELIB.Group.Group()
interfaces.inputs["activate"].connectedTo = "1"
interfaces.children['Bioloid'] = FIRELIB.Robot.Robot(members,"10.0.0.17","8080")
interfaces.children['Bioloid'].inputs["activate"].connectedTo = "1"


systems = FIRELIB.Group.Group()
systems.inputs["activate"].connectedTo = "1"
systems.children['CSVRecorder'] = FIRELIB.CSVRecorder.CSVRecorder(members)
systems.children['CSVRecorder'].inputs["activate"].connectedTo = "1"

for member in members:
    for art in members[member]:
        interfaces.children['Bioloid'].inputs[art].connectedTo = " "+art+" "
        interfaces.children['Bioloid'].outputs[art].connectedTo = " "+art+"m "
        if systems.children['CSVRecorder'].outputs.has_key(art):
            systems.children['CSVRecorder'].outputs[art].connectedTo = " "+art+" "
        if systems.children['CSVRecorder'].inputs.has_key(art):
            systems.children['CSVRecorder'].inputs[art].connectedTo = " "+art+"m "
            
systems.children['CSVRecorder'].outputs['Number'].connectedTo = " n "
interfaces.children['Bioloid'].inputs['Number'].connectedTo = " n "

systems.children['CSVRecorder'].outputs['Duration'].connectedTo = " Delta "
interfaces.children['Bioloid'].inputs['Duration'].connectedTo = " Delta "

# execution of FIRE engine
channels = {}
e = FIRELIB.Engine.Engine(interfaces,systems,channels,dt=0.02)
e.start()
    

sys.exit(app.exec_())

