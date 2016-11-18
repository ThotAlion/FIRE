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

mainW = QWidget()
mainLay = QHBoxLayout(mainW)
popLayP = QVBoxLayout()

interfaces = FIRELIB.Group.Group()
interfaces.inputs["activate"].connectedTo = "1"
interfaces.children['Poppy'] = FIRELIB.Robot.Robot(members,"10.0.0.101","8080")
interfaces.children['Poppy'].inputs["activate"].connectedTo = "1"
interfaces.children['Index'] = FIRELIB.LeftIndex.LeftIndex()
interfaces.children['Index'].inputs["activate"].connectedTo = "1"
interfaces.children['PoppyButtons'] = FIRELIB.Buttons.Buttons(['head to leap'],[0],'check')
interfaces.children['PoppyButtons'].inputs["activate"].connectedTo = "1"
interfaces.children['PoppyButtons'].outputs["head to leap"].connectedTo = " pleap "

systems = FIRELIB.Group.Group()
systems.inputs["activate"].connectedTo = "1"

systems.children['Ratelim'] = FIRELIB.Ratelim.Ratelim(2,50)
systems.children['Ratelim'].inputs["activate"].connectedTo = "1"

systems.children['PCSVRecorder'] = FIRELIB.CSVRecorder.CSVRecorder(members,folder = '/TAPES_CSV_DUSSELDORF/')
systems.children['PCSVRecorder'].inputs["activate"].connectedTo = "1"

mainLay.addLayout(popLayP)
poppytitle = QLabel("POPPY")
poppytitle.setStyleSheet("font-size: 30px;")
popLayP.addWidget(poppytitle)
popLayP.addWidget(interfaces.children['Poppy'])
popLayP.addWidget(interfaces.children['PoppyButtons'])
mainLay.addWidget(systems.children['PCSVRecorder'])
mainLay.setStretch(0,1)
mainLay.setStretch(1,3)
mainW.show()

for member in members:
    for art in members[member]:
        if systems.children['PCSVRecorder'].outputs.has_key(art):
            systems.children['PCSVRecorder'].outputs[art].connectedTo = " p"+art+" "
        if systems.children['PCSVRecorder'].inputs.has_key(art):
            systems.children['PCSVRecorder'].inputs[art].connectedTo = " p"+art+"m "
        interfaces.children['Poppy'].inputs[art].connectedTo = " p"+art+" "
        interfaces.children['Poppy'].outputs[art].connectedTo = " p"+art+"m "
        
systems.children['PCSVRecorder'].outputs['Number'].connectedTo = " pn "
interfaces.children['Poppy'].inputs['Number'].connectedTo = " pn "

systems.children['PCSVRecorder'].outputs['Duration'].connectedTo = " pDelta "
interfaces.children['Poppy'].inputs['Duration'].connectedTo = " pDelta "

interfaces.children['Index'].outputs['index yaw'].connectedTo = " yaw "
systems.children['Ratelim'].inputs['ch0'].connectedTo = " yaw "
systems.children['Ratelim'].outputs['ch0'].connectedTo = " yawr "
interfaces.children['Index'].outputs['index pitch'].connectedTo = " pitch "
systems.children['Ratelim'].inputs['ch1'].connectedTo = " pitch "
systems.children['Ratelim'].outputs['ch1'].connectedTo = " pitchr "

systems.children['ptete direct'] = FIRELIB.Wires.Wires(2)
systems.children['ptete direct'].inputs["activate"].connectedTo = " - pleap +1 "
systems.children['ptete direct'].inputs["ch0"].connectedTo = " phead_y "
systems.children['ptete direct'].outputs["ch0"].connectedTo = " phead_y "
systems.children['ptete direct'].inputs["ch1"].connectedTo = " phead_z "
systems.children['ptete direct'].outputs["ch1"].connectedTo = " phead_z "

systems.children['ptete laser'] = FIRELIB.Wires.Wires(2)
systems.children['ptete laser'].inputs["activate"].connectedTo = " pleap "
systems.children['ptete laser'].inputs["ch0"].connectedTo = " str(- pitchr ) "
systems.children['ptete laser'].outputs["ch0"].connectedTo = " phead_y "
systems.children['ptete laser'].inputs["ch1"].connectedTo = " str(- yawr ) "
systems.children['ptete laser'].outputs["ch1"].connectedTo = " phead_z "

# execution of FIRE engine
channels = {}
e = FIRELIB.Engine.Engine(interfaces,systems,channels)
e.start()
    

sys.exit(app.exec_())

