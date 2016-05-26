import sys
import FIRELIB
import time
from PyQt4.QtGui import *
from PyQt4.QtCore import *


app = QApplication(sys.argv)
styleFile = QFile("FIRELIB\CSS\styleSheet.txt")
styleFile.open(styleFile.ReadOnly)
style = str(styleFile.readAll())
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
interfaces.children['Poppy'] = FIRELIB.Robot.Robot(members,"10.0.0.20","8080")
interfaces.children['Poppy'].inputs["activate"].connectedTo = "1"
interfaces.children['Radio'] = FIRELIB.Radio.Radio()
interfaces.children['Radio'].inputs["activate"].connectedTo = "1"

systems = FIRELIB.Group.Group()
systems.inputs["activate"].connectedTo = "1"

systems.children['CSVPlayer'] = FIRELIB.CSVPlayer.CSVPlayer(members)
systems.children['CSVPlayer'].inputs["activate"].connectedTo = "1"

systems.children['disp'] = FIRELIB.Display.Display(["tapename","fini"])
systems.children['disp'].inputs["activate"].connectedTo = "1"

for member in members:
    for art in members[member]:
        if systems.children['CSVPlayer'].outputs.has_key(art):
            systems.children['CSVPlayer'].outputs[art].connectedTo = " p"+art+" "
        if systems.children['CSVPlayer'].inputs.has_key(art):
            systems.children['CSVPlayer'].inputs[art].connectedTo = " p"+art+"m "
        interfaces.children['Poppy'].inputs[art].connectedTo = " p"+art+" "
        interfaces.children['Poppy'].outputs[art].connectedTo = " p"+art+"m "
        
systems.children['CSVPlayer'].outputs['Number'].connectedTo = " pn "
interfaces.children['Poppy'].inputs['Number'].connectedTo = " pn "

systems.children['CSVPlayer'].outputs['Duration'].connectedTo = " pDelta "
interfaces.children['Poppy'].inputs['Duration'].connectedTo = " pDelta "

interfaces.children['Radio'].outputs['Tape'].connectedTo = " Tape "
systems.children['CSVPlayer'].inputs['Tape'].connectedTo = " Tape "
systems.children['disp'].inputs['tapename'].connectedTo = " Tape "

interfaces.children['Radio'].inputs['Finished'].connectedTo = " fin "
systems.children['CSVPlayer'].outputs['finished'].connectedTo = " fin "
systems.children['disp'].inputs['fini'].connectedTo = " fin "

# execution of FIRE engine
channels = {}
e = FIRELIB.Engine.Engine(interfaces,systems,channels)
e.start()
    

sys.exit(app.exec_())

