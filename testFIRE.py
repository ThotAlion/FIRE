import FIRELIB
import time
interfaces = []
systems = []
channels = {}

interfaces.append(FIRELIB.PanTilt.PanTilt())

while True:
    for int in interfaces:
        int.deliverOutputs(channels)
    for sys in systems:
        sys.deliverOutputs(channels)
    for int in interfaces:
        int.receiveInputs(channels)
        
    time.sleep(0.02)
        


