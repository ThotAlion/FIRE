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
members["abs"] = ['abs_x','abs_y','abs_z']
members["bust"] = ['bust_y','bust_x']
members["left arm"] =  ['l_shoulder_y','l_shoulder_x','l_arm_z','l_elbow_y','l_wrist_z','l_wrist_x']
members["right arm"] = ['r_shoulder_y','r_shoulder_x','r_arm_z','r_elbow_y','r_wrist_z','r_wrist_x']
members["left leg"] =  ['l_hip_x','l_hip_z','l_hip_y','l_knee_y','l_ankle_y']
members["right leg"] = ['r_hip_x','r_hip_z','r_hip_y','r_knee_y','r_ankle_y']


interfaces = FIRELIB.Group.Group()
interfaces.inputs["activate"].connectedTo = "1"
interfaces.children['Poppy'] = FIRELIB.Robot.Robot(members,"10.0.0.2","8080")
interfaces.children['Poppy'].inputs["activate"].connectedTo = "1"

systems = FIRELIB.Group.Group()
systems.inputs["activate"].connectedTo = "1"
systems.children['Machine'] = FIRELIB.FiniteStateMachine.FiniteStateMachine("MACHINES/machine.csv")

systems.children['CSVRecorder'] = FIRELIB.CSVRecorder.CSVRecorder(members)
systems.children['CSVRecorder'].inputs["activate"].connectedTo = "1"

for member in members:
    for art in members[member]:
        interfaces.children['Poppy'].inputs[art].connectedTo = " "+art+" "
        interfaces.children['Poppy'].outputs[art].connectedTo = " "+art+"m "
        if systems.children['CSVRecorder'].outputs.has_key(art):
            systems.children['CSVRecorder'].outputs[art].connectedTo = " "+art+" "
        if systems.children['CSVRecorder'].inputs.has_key(art):
            systems.children['CSVRecorder'].inputs[art].connectedTo = " "+art+"m "
systems.children['CSVRecorder'].outputs['Number'].connectedTo = " n "
interfaces.children['Poppy'].inputs['Number'].connectedTo = " n "
systems.children['CSVRecorder'].outputs['Duration'].connectedTo = " Delta "
interfaces.children['Poppy'].inputs['Duration'].connectedTo = " Delta "
        
# execution of FIRE engine
channels = {}
e = FIRELIB.Engine.Engine(interfaces,systems,channels)
e.start()
    

sys.exit(app.exec_())

