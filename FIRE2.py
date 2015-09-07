import sys
import FIRELIB2
import time

interfaces = FIRELIB2.Group.Group()
interfaces.children['Poppy'] = FIRELIB2.Poppy.Poppy("192.168.1.20","8080")

interfaces.children['Poppy'].outputs['r_knee_y']['present_position'].connectedTo = 'a'
interfaces.children['Poppy'].inputs['r_knee_y']['goal_position'].connectedTo = 'a'
interfaces.children['Poppy'].inputs['r_knee_y']['compliant'].connectedTo = '0'

f = {}

interfaces.start()
time.sleep(1)

while True:
    f = interfaces.setOutputs(f)
    interfaces.getInputs(f)
    time.sleep(0.02)

