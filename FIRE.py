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

interfaces = FIRELIB.Group.Group()
interfaces.children['Poppy'] = FIRELIB.Poppy.Poppy("10.0.0.2","8080")
interfaces.children['Leap'] = FIRELIB.LeftIndex.LeftIndex()

systems = FIRELIB.Group.Group()
systems.children['Record'] = FIRELIB.Recorder.Recorder(['head_y','head_z',
                     'abs_x','abs_y','abs_z','bust_y','bust_x',
                     'l_shoulder_y','l_shoulder_x','l_arm_z','l_elbow_y',
                     'r_shoulder_y','r_shoulder_x','r_arm_z','r_elbow_y',
                     'l_hip_x','l_hip_z','l_hip_y','l_knee_y','l_ankle_y',
                     'r_hip_x','r_hip_z','r_hip_y','r_knee_y','r_ankle_y',
                     'r_wrist_z','r_wrist_x','l_wrist_z','l_wrist_x'])

for output in interfaces.children['Poppy'].outputs:
    interfaces.children['Poppy'].outputs[output]['present_position'].connectedTo = " "+output+" "
    systems.children['Record'].inputs[output].connectedTo = " "+output+" "

for input in interfaces.children['Poppy'].inputs:
    interfaces.children['Poppy'].inputs[input]['goal_position'].connectedTo = " "+input+"c "
    interfaces.children['Poppy'].inputs[input]['moving_speed'].connectedTo = " "+input+"vc "
    systems.children['Record'].outputs[input]['position'].connectedTo = " "+input+"c "
    systems.children['Record'].outputs[input]['speed'].connectedTo = " "+input+"vc "

interfaces.children['Leap'].outputs["index pitch"].connectedTo = " indexpitch "
interfaces.children['Leap'].outputs["index yaw"].connectedTo = " indexyaw "
interfaces.children['Poppy'].inputs["head_z"]['goal_position'].connectedTo = "-2* indexyaw "
interfaces.children['Poppy'].inputs["head_z"]['moving_speed'].connectedTo = "20"
interfaces.children['Poppy'].inputs["head_y"]['goal_position'].connectedTo = "- indexpitch "
interfaces.children['Poppy'].inputs["head_y"]['moving_speed'].connectedTo = "10"
channels = {}

e = FIRELIB.Engine.Engine(interfaces,systems,channels)
e.start()
    

sys.exit(app.exec_())

