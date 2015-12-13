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

mainW = QWidget()
mainLay = QHBoxLayout(mainW)

interfaces = FIRELIB.Group.Group()
interfaces.inputs["activate"].connectedTo = "1"
# no interfaces

systems = FIRELIB.Group.Group()
systems.inputs["activate"].connectedTo = "1"
systems.children["button"] = FIRELIB.Buttons.Buttons(["button 1","button 2","STOP"])
systems.children["button"].inputs["activate"].connectedTo = "1"
systems.children["disp"] = FIRELIB.Display.Display(["disp 1","disp 2"])
systems.children["disp"].inputs["activate"].connectedTo = "1"


mainLay.addWidget(systems.children["button"])
mainLay.addWidget(systems.children["disp"])
mainW.show()

# connexions
systems.children["button"].outputs["button 1"].connectedTo = " a "
systems.children["button"].outputs["button 2"].connectedTo = " b "
systems.children["disp"].inputs["disp 1"].connectedTo = " a "
systems.children["disp"].inputs["disp 2"].connectedTo = " b "

# execution of FIRE engine
channels = {}
e = FIRELIB.Engine.Engine(interfaces,systems,channels)
e.start()
    

sys.exit(app.exec_())

