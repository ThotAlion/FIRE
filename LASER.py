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


interfaces.children['pad'] = FIRELIB.xboxPad.xboxPad(0)
interfaces.children['pad'].inputs["activate"].connectedTo = "1"
interfaces.children['pad'].outputs['button A'].connectedTo = " buttonA "

interfaces.children['Index'] = FIRELIB.LeftIndex.LeftIndex()
interfaces.children['Index'].inputs["activate"].connectedTo = "1"
interfaces.children['Index'].outputs['index pitch'].connectedTo = " pitch "
interfaces.children['Index'].outputs['index yaw'].connectedTo = " yaw "

systems = FIRELIB.Group.Group()
systems.inputs["activate"].connectedTo = "1"

systems.children['Machine'] = FIRELIB.FiniteStateMachine.FiniteStateMachine("MACHINES/laser.csv")
systems.children['Machine'].inputs["activate"].connectedTo = "1"
systems.children['Machine'].inputs["f_retourne"].connectedTo = " f_retourne "
systems.children['Machine'].inputs["f_genou"].connectedTo = " f_genou "
systems.children['Machine'].inputs["f_laser"].connectedTo = " f_laser "
systems.children['Machine'].inputs["buttonA"].connectedTo = " buttonA "
systems.children['Machine'].outputs["b_arret"].connectedTo = " b_arret "
systems.children['Machine'].outputs["b_retourne"].connectedTo = " b_retourne "
systems.children['Machine'].outputs["b_genou"].connectedTo = " b_genou "
systems.children['Machine'].outputs["b_laser"].connectedTo = " b_laser "

systems.children['Ratelim'] = FIRELIB.Ratelim.Ratelim(2,10)
systems.children['Ratelim'].inputs["activate"].connectedTo = " b_laser "
systems.children['Ratelim'].inputs['ch0'].connectedTo = " yaw "
systems.children['Ratelim'].outputs['ch0'].connectedTo = " yawr "
systems.children['Ratelim'].inputs['ch1'].connectedTo = " pitch "
systems.children['Ratelim'].outputs['ch1'].connectedTo = " pitchr "

systems.children['retourne'] = FIRELIB.CSVPlayer.CSVPlayer("TAPES_CSV/dos_2_ventre.csv")
systems.children['retourne'].inputs["activate"].connectedTo = " b_retourne "
systems.children['retourne'].outputs["finished"].connectedTo = " f_retourne "
systems.children['retourne'].outputs['Duration'].connectedTo = " Delta "
systems.children['retourne'].outputs['Number'].connectedTo = " n "
for member in members:
    for art in members[member]:
        systems.children['retourne'].outputs[art].connectedTo = " "+art+" "

systems.children['releve'] = FIRELIB.CSVPlayer.CSVPlayer("TAPES_CSV/ventre_2_genou.csv")
systems.children['releve'].inputs["activate"].connectedTo = " b_genou "
systems.children['releve'].outputs["finished"].connectedTo = " f_genou "
systems.children['releve'].outputs['Duration'].connectedTo = " Delta "
systems.children['releve'].outputs['Number'].connectedTo = " n "
for member in members:
    for art in members[member]:
        systems.children['releve'].outputs[art].connectedTo = " "+art+" "

systems.children['mou'] = FIRELIB.CSVPlayer.CSVPlayer("TAPES_CSV/_mou.csv")
systems.children['mou'].inputs["activate"].connectedTo = " b_arret "
systems.children['mou'].outputs['Duration'].connectedTo = " Delta "
systems.children['mou'].outputs['Number'].connectedTo = " n "
for member in members:
    for art in members[member]:
        systems.children['mou'].outputs[art].connectedTo = " "+art+" "

systems.children['tete direct'] = FIRELIB.Wires.Wires(2)
systems.children['tete direct'].inputs["activate"].connectedTo = " b_direct "
systems.children['tete direct'].inputs["ch0"].connectedTo = " head_y "
systems.children['tete direct'].outputs["ch0"].connectedTo = " head_y "
systems.children['tete direct'].inputs["ch1"].connectedTo = " head_z "
systems.children['tete direct'].outputs["ch1"].connectedTo = " head_z "

systems.children['tete laser'] = FIRELIB.Wires.Wires(2)
systems.children['tete laser'].inputs["activate"].connectedTo = " b_laser "
systems.children['tete direct'].inputs["ch0"].connectedTo = " str(- pitchr ) "
systems.children['tete direct'].outputs["ch0"].connectedTo = " head_y "
systems.children['tete direct'].inputs["ch1"].connectedTo = " str(- yawr ) "
systems.children['tete direct'].outputs["ch1"].connectedTo = " head_z "

# execution of FIRE engine
channels = {}
e = FIRELIB.Engine.Engine(interfaces,systems,channels)
e.start()
    

sys.exit(app.exec_())

