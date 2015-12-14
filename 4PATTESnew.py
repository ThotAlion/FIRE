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

interfaces.children['Poppy'] = FIRELIB.Robot.Robot(members,"10.0.2.1","8080")
interfaces.children['Poppy'].inputs["activate"].connectedTo = "1"
interfaces.children['Poppy'].outputs["Temperature"].connectedTo = " TC "
interfaces.children['Poppy'].inputs['Number'].connectedTo = " n "
interfaces.children['Poppy'].inputs['Duration'].connectedTo = " Delta "
for member in members:
    for art in members[member]:
        interfaces.children['Poppy'].inputs[art].connectedTo = " "+art+" "
        interfaces.children['Poppy'].outputs[art].connectedTo = " "+art+"m "

systems = FIRELIB.Group.Group()
systems.inputs["activate"].connectedTo = "1"
systems.children['Machine'] = FIRELIB.FiniteStateMachine.FiniteStateMachine("MACHINES/marche_new.csv")
systems.children['Machine'].inputs["activate"].connectedTo = "1"
systems.children['Machine'].inputs["finished"].connectedTo = " finished "
systems.children['Machine'].inputs["buttonA"].connectedTo = " buttonA "
systems.children['Machine'].inputs["buttonB"].connectedTo = " buttonB "
systems.children['Machine'].inputs["avant"].connectedTo = " Y == 1"
systems.children['Machine'].inputs["gauche"].connectedTo = " X == -1"
systems.children['Machine'].inputs["droite"].connectedTo = " X == 1"
systems.children['Machine'].outputs["CSVPath"].connectedTo = " CSVPath "




systems.children['Player'] = FIRELIB.CSVPlayer.CSVPlayer(members)
systems.children['Player'].inputs["activate"].connectedTo = "1"
systems.children['Player'].inputs["Tape"].connectedTo = " CSVPath "
systems.children['Player'].outputs["finished"].connectedTo = " finished "
systems.children['Player'].outputs['Duration'].connectedTo = " Delta "
systems.children['Player'].outputs['Number'].connectedTo = " n "

systems.children['Disp'] = FIRELIB.Display.Display(["tape name","finished","n"])
systems.children['Disp'].inputs["activate"].connectedTo = "1"
systems.children['Disp'].inputs["tape name"].connectedTo = " CSVPath "
systems.children['Disp'].inputs["finished"].connectedTo = " finished "
systems.children['Disp'].inputs["n"].connectedTo = " n "

for member in members:
    for art in members[member]:
        systems.children['Player'].outputs[art].connectedTo = " "+art+" "

# execution of FIRE engine
channels = {}
e = FIRELIB.Engine.Engine(interfaces,systems,channels)
e.start()
    

sys.exit(app.exec_())
