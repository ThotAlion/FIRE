import sys
import FIRELIB2
import time

interfaces = FIRELIB2.Group.Group()
interfaces.children['Poppy'] = FIRELIB2.Poppy.Poppy("192.168.1.20","8080")

f = {}

interfaces.start()

while True:
    f = interfaces.setOutputs(f)
    interfaces.getInputs(f)
    time.sleep(1)

