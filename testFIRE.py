import FIRELIB
import time
interfaces = []
systems = []
channels = {}

L = FIRELIB.LeapMotion.LeapMotion()
P = FIRELIB.PypotCreature.PypotCreature(IP="192.168.31.102",port="8080")

L._outputs["right_index_pitch"].connectedTo = "A"
P._inputs["head_y goal_position"].connectedTo = "A*180/3"
P._inputs["head_y moving_speed"].connectedTo = "120"

interfaces.append(L)
interfaces.append(P)


while True:
    for int in interfaces:
        channels = int.deliverOutputs(channels)
    for sys in systems:
        channels = sys.deliverOutputs(channels)
    for int in interfaces:
        int.receiveInputs(channels)
        
    time.sleep(0.02)
        


