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

mainW = QWidget()
mainLay = QHBoxLayout(mainW)
popLay = QVBoxLayout()
mainLay.addLayout(popLay)

interfaces = FIRELIB.Group.Group()
interfaces.inputs["activate"].connectedTo = "1"
interfaces.children['Poppy'] = FIRELIB.Robot.Robot(members,"10.0.0.6","8080")
interfaces.children['Poppy'].inputs["activate"].connectedTo = "1"
interfaces.children['Mommy'] = FIRELIB.Robot.Robot(members,"10.0.0.7","8080")
interfaces.children['Mommy'].inputs["activate"].connectedTo = "1"
interfaces.children['Index'] = FIRELIB.LeftIndex.LeftIndex()
interfaces.children['Index'].inputs["activate"].connectedTo = "1"
# interfaces.children['pad'] = FIRELIB.xboxPad.xboxPad(0)
# interfaces.children['pad'].inputs["activate"].connectedTo = "1"


systems = FIRELIB.Group.Group()
systems.inputs["activate"].connectedTo = "1"
systems.children['Alarm'] = FIRELIB.SoundPlayer.SoundPlayer("Sounds/alarm.wav")
systems.children['Alarm'].inputs["activate"].connectedTo = "1"
# systems.children['Machine'] = FIRELIB.FiniteStateMachine.FiniteStateMachine("MACHINES/machine.csv")
# systems.children['Machine'].inputs["activate"].connectedTo = "0"

systems.children['CSVRecorder1'] = FIRELIB.CSVRecorder.CSVRecorder(members)
systems.children['CSVRecorder1'].inputs["activate"].connectedTo = "1"
systems.children['CSVRecorder2'] = FIRELIB.CSVRecorder.CSVRecorder(members)
systems.children['CSVRecorder2'].inputs["activate"].connectedTo = "1"

popLay.addWidget(interfaces.children['Poppy'])
popLay.addWidget(interfaces.children['Mommy'])
mainLay.addWidget(systems.children['CSVRecorder1'])
mainLay.addWidget(systems.children['CSVRecorder2'])
mainW.show()

for member in members:
    for art in members[member]:
        interfaces.children['Poppy'].inputs[art].connectedTo = " "+art+"1 "
        interfaces.children['Poppy'].outputs[art].connectedTo = " "+art+"1m "
        interfaces.children['Mommy'].inputs[art].connectedTo = " "+art+"2 "
        interfaces.children['Mommy'].outputs[art].connectedTo = " "+art+"2m "
        if systems.children['CSVRecorder1'].outputs.has_key(art):
            systems.children['CSVRecorder1'].outputs[art].connectedTo = " "+art+"1 "
        if systems.children['CSVRecorder1'].inputs.has_key(art):
            systems.children['CSVRecorder1'].inputs[art].connectedTo = " "+art+"1m "
        if systems.children['CSVRecorder2'].outputs.has_key(art):
            systems.children['CSVRecorder2'].outputs[art].connectedTo = " "+art+"2 "
        if systems.children['CSVRecorder2'].inputs.has_key(art):
            systems.children['CSVRecorder2'].inputs[art].connectedTo = " "+art+"2m "
            
systems.children['CSVRecorder1'].outputs['Number'].connectedTo = " n1 "
interfaces.children['Poppy'].inputs['Number'].connectedTo = " n1 "

systems.children['CSVRecorder2'].outputs['Number'].connectedTo = " n2 "
interfaces.children['Mommy'].inputs['Number'].connectedTo = " n2 "

systems.children['CSVRecorder1'].outputs['Duration'].connectedTo = " Delta1 "
interfaces.children['Poppy'].inputs['Duration'].connectedTo = " Delta1 "

systems.children['CSVRecorder2'].outputs['Duration'].connectedTo = " Delta2 "
interfaces.children['Mommy'].inputs['Duration'].connectedTo = " Delta2 "

# interfaces.children['pad'].outputs['button A'].connectedTo = " buttonA "
# systems.children['Alarm'].inputs['play'].connectedTo = " buttonA "

# execution of FIRE engine
channels = {}
e = FIRELIB.Engine.Engine(interfaces,systems,channels)
e.start()
    

sys.exit(app.exec_())

