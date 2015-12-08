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

interfaces.children['Poppy'] = FIRELIB.Robot.Robot(members,"10.0.0.4","8080")
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
interfaces.children['pad'].outputs['button B'].connectedTo = " buttonB "
interfaces.children['pad'].outputs['hat Y1'].connectedTo = " Y "
interfaces.children['pad'].outputs['hat X1'].connectedTo = " X "

systems = FIRELIB.Group.Group()
systems.inputs["activate"].connectedTo = "1"
systems.children['Machine'] = FIRELIB.FiniteStateMachine.FiniteStateMachine("MACHINES/marche.csv")
systems.children['Machine'].inputs["activate"].connectedTo = "1"
systems.children['Machine'].inputs["f_retourne"].connectedTo = " f_retourne "
systems.children['Machine'].inputs["buttonA"].connectedTo = " buttonA "
systems.children['Machine'].inputs["buttonB"].connectedTo = " buttonB "
systems.children['Machine'].inputs["f_releve"].connectedTo = " f_releve "
systems.children['Machine'].inputs["avant"].connectedTo = " Y == 1"
systems.children['Machine'].inputs["gauche"].connectedTo = " X == -1"
systems.children['Machine'].inputs["droite"].connectedTo = " X == 1"
systems.children['Machine'].inputs["f_recouche"].connectedTo = " f_recouche "
systems.children['Machine'].inputs["f_avance"].connectedTo = " f_avance "
systems.children['Machine'].outputs["b_retourne"].connectedTo = " b_retourne "
systems.children['Machine'].outputs["b_releve"].connectedTo = " b_releve "
systems.children['Machine'].outputs["b_avance"].connectedTo = " b_avance "
systems.children['Machine'].outputs["b_tourneD"].connectedTo = " b_tourneD "
systems.children['Machine'].outputs["b_tourneG"].connectedTo = " b_tourneG "
systems.children['Machine'].outputs["b_recouche"].connectedTo = " b_recouche "
systems.children['Machine'].outputs["b_mou"].connectedTo = " b_mou "
systems.children['Machine'].outputs["b_qpattes"].connectedTo = " b_qpattes "

# tapes declaration
systems.children['Retourne'] = FIRELIB.CSVPlayer.CSVPlayer("TAPES_CSV/dos_2_ventre.csv")
systems.children['Retourne'].inputs["activate"].connectedTo = " b_retourne "
systems.children['Retourne'].outputs["finished"].connectedTo = " f_retourne "
systems.children['Retourne'].outputs['Duration'].connectedTo = " Delta "
systems.children['Retourne'].outputs['Number'].connectedTo = " n "
for member in members:
    for art in members[member]:
        systems.children['Retourne'].outputs[art].connectedTo = " "+art+" "
          
systems.children['Releve'] = FIRELIB.CSVPlayer.CSVPlayer("TAPES_CSV/ventre_2_quatre.csv")
systems.children['Releve'].inputs["activate"].connectedTo = " b_releve "
systems.children['Releve'].outputs["finished"].connectedTo = " f_releve "
systems.children['Releve'].outputs['Duration'].connectedTo = " Delta "
systems.children['Releve'].outputs['Number'].connectedTo = " n "
for member in members:
    for art in members[member]:
        systems.children['Releve'].outputs[art].connectedTo = " "+art+" "

systems.children['Recouche'] = FIRELIB.CSVPlayer.CSVPlayer("TAPES_CSV/quatre_2_ventre.csv")
systems.children['Recouche'].inputs["activate"].connectedTo = " b_recouche "
systems.children['Recouche'].outputs["finished"].connectedTo = " f_recouche "
systems.children['Recouche'].outputs['Duration'].connectedTo = " Delta "
systems.children['Recouche'].outputs['Number'].connectedTo = " n "
for member in members:
    for art in members[member]:
        systems.children['Recouche'].outputs[art].connectedTo = " "+art+" "

systems.children['Avance'] = FIRELIB.CSVPlayer.CSVPlayer("TAPES_CSV/quatre_pattes_avance.csv")
systems.children['Avance'].inputs["activate"].connectedTo = " b_avance "
systems.children['Avance'].outputs["finished"].connectedTo = " f_avance "
systems.children['Avance'].outputs['Duration'].connectedTo = " Delta "
systems.children['Avance'].outputs['Number'].connectedTo = " n "
for member in members:
    for art in members[member]:
        systems.children['Avance'].outputs[art].connectedTo = " "+art+" "

systems.children['Tourner droite'] = FIRELIB.CSVPlayer.CSVPlayer("TAPES_CSV/quatre_pattes_droite.csv")
systems.children['Tourner droite'].inputs["activate"].connectedTo = " b_tourneD "
systems.children['Tourner droite'].outputs["finished"].connectedTo = " f_tourneD "
systems.children['Tourner droite'].outputs['Duration'].connectedTo = " Delta "
systems.children['Tourner droite'].outputs['Number'].connectedTo = " n "
for member in members:
    for art in members[member]:
        systems.children['Tourner droite'].outputs[art].connectedTo = " "+art+" "

systems.children['Tourner gauche'] = FIRELIB.CSVPlayer.CSVPlayer("TAPES_CSV/quatre_pattes_gauche.csv")
systems.children['Tourner gauche'].inputs["activate"].connectedTo = " b_tourneG "
systems.children['Tourner gauche'].outputs["finished"].connectedTo = " f_tourneG "
systems.children['Tourner gauche'].outputs['Duration'].connectedTo = " Delta "
systems.children['Tourner gauche'].outputs['Number'].connectedTo = " n "
for member in members:
    for art in members[member]:
        systems.children['Tourner gauche'].outputs[art].connectedTo = " "+art+" "

systems.children['Mou'] = FIRELIB.CSVPlayer.CSVPlayer("TAPES_CSV/_mou.csv")
systems.children['Mou'].inputs["activate"].connectedTo = " b_mou "
systems.children['Mou'].outputs["finished"].connectedTo = " f_mou "
systems.children['Mou'].outputs['Duration'].connectedTo = " Delta "
systems.children['Mou'].outputs['Number'].connectedTo = " n "
for member in members:
    for art in members[member]:
        systems.children['Mou'].outputs[art].connectedTo = " "+art+" "

systems.children['4pattes'] = FIRELIB.CSVPlayer.CSVPlayer("TAPES_CSV/_quatre_pattes.csv")
systems.children['4pattes'].inputs["activate"].connectedTo = " b_qpattes "
systems.children['4pattes'].outputs["finished"].connectedTo = " f_qpattes "
systems.children['4pattes'].outputs['Duration'].connectedTo = " Delta "
systems.children['4pattes'].outputs['Number'].connectedTo = " n "
for member in members:
    for art in members[member]:
        systems.children['4pattes'].outputs[art].connectedTo = " "+art+" "

# execution of FIRE engine
channels = {}
e = FIRELIB.Engine.Engine(interfaces,systems,channels)
e.start()
    

sys.exit(app.exec_())

