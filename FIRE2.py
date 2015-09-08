import sys
import FIRELIB2
import time
from PyQt4.QtGui import *
from PyQt4.QtCore import *

interfaces = FIRELIB2.Group.Group()
interfaces.children['Poppy'] = FIRELIB2.Poppy.Poppy("192.168.1.20","8080")
# interfaces.children['Record'] = FIRELIB2.Recorder.Recorder(arti_list = ['head_y','head_z',
                     # 'abs_x','abs_y','abs_z','bust_y','bust_x',
                     # 'l_shoulder_y','l_shoulder_x','l_arm_z','l_elbow_y',
                     # 'r_shoulder_y','r_shoulder_x','r_arm_z','r_elbow_y',
                     # 'l_hip_x','l_hip_z','l_hip_y','l_knee_y','l_ankle_y',
                     # 'r_hip_x','r_hip_z','r_hip_y','r_knee_y','r_ankle_y',])

interfaces.children['Poppy'].outputs['r_knee_y']['present_position'].connectedTo = 'a'
interfaces.children['Poppy'].inputs['r_knee_y']['goal_position'].connectedTo = 'a'

styleFile = QFile("FIRELIB\styleSheet.txt")
styleFile.open(styleFile.ReadOnly)
style = str(styleFile.readAll())
app = QApplication(sys.argv)
app.setStyleSheet(style)

f = {}

interfaces.start()
time.sleep(1)



while True:
    f = interfaces.setOutputs(f)
    interfaces.getInputs(f)
    time.sleep(0.02)
    

sys.exit(app.exec_())

