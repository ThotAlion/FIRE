# FIRE
## Introduction
The purpose of FIRE is to program a robot as if it was a cartoon character by pose to pose. The interface is here to tune a sequence of poses and play it. The architecture is modular so that we can add others robots. The graphical user interface uses PyQt4 and the model/view programming technology.

## Architecture
FIRE is dataflow synchronous control program. That is to say, several function are executed 50 times a second to deliver data in channels. Each function is named block since the interface is made by connexions to the channels.
The architecture is made as simple as possible.

## Main files
In the FIRELIB, are three main files : Block.py (41 lines), Connexion.py (37 lines) and Engine.py (35 lines)
The philosophy is "less code lines, less errors".
A block is a system which reads inputs to create outputs, like a function, but the inputs and outputs are connexions. The purpose of a connexion is to link blocks between them using channels.
The Engine is the structure which makes live the blocks.
All the other files in FIRELIB are inherited objects from blocks.
Notice there are two types of blocks : Interfaces and Systems.
An interface is a block which is connected to the real world. It reads sensors to create channels that can be read by the others blocks
A system is a block which operates its inputs to creates outputs.

## Blocks
### Group
The group is a block which can contain others blocks. This block has a list of "children" which are called in the order of declaration. Notice the list of Interfaces and Systems are Groups
### Robot
This block is an interface with a robot connected via ZMQ server to the BRAIN server (see poppy server folder)
It gives to the robot an order via a meta-order using pose language :
 - "M" : the motor is shutdown but within its limits
 - "P" : the motor is shutdown but sluggish and within its limits
 - "L-10" : the motor goes to the consign (here -10) with the initial speed taken from the previous pose
 - "S80" : the motor goes to the consign (here 80) and finishes at a zero speed with the initial speed taken from the previous pose
 - "K" : the motor is blocked to its current position
 - "I50" : the motor is set to the consign (here 50) instantaneously
### Poppy (and uniPoppy)
This is an old version of the Robot block dedicated to Poppy robot.
### CSVRecorder (Recorder is an old version)
This block is a player and an editor of choregraphies to produce CSV files editable in Excel.
### FiniteStateMachine
This block is designed to manage all the other blocks using a mosaic screen. It is useful to have visibility during a show.
### LeftIndex
This block is an interface with the Leap Motion to recup the left index pitch and yaw.
### CSVPlayer
This block is a simplification of CSVRecorder the editor and graphic interface are remove. The block just plays a CSV when activated.
### xboxPad
This block is an interface to xbox pad (under construction)


## How to use FIRE with Poppy
To pilot Poppy with FIRE, Poppy must be connected to the controlling computer by IP protocol (WIFI or Ethernet).
On Poppy computer, a server must be installed for remote purpose.
This server is in the "poppy_server" directory in the repository.
Take care netifaces is installed on Poppy. If not type in a shell :
sudo pip install netifaces
netifaces is a library used here to get the IP adress of Poppy.
Then, the full_poppy.json file must be updated, the one in this repositery considers there are wrist on your robot which is not usual. Take care of each name and ID of each motor.
The pypot version used here must be modified also : the REST API must be enhanced to manage fast remote access.
The modification is described in this commit :
https://github.com/ThotAlion/pypot/commit/c9813aca1a53a784ff85e5de4b17ea794192c4cb

Then, you can launch the server in a shell:
python serverZMP.py &

On the control computer, before executing FIRE.py, modify the IP adress (I could do it in the GUI but FIRE must be operationnal 3s after launch)
Then execute FIRE.py, your robot is ready for "cartooning"

### Cartooning interface
Two windows open when you launch FIRE :
- Poppy control : this window allows you to control articulations and which is set "Mou". "Mou" means that the motor is shutdown and no torque is applied.
- Recorder control : this window allows to program the robot by pose to pose.

The recorder control is divided in three columns :
- The last column discribes the objectives of each motor of your robot. Each line has the name of the motor, the nature of the objective and the consign. The nature available are :
 - "M" : the motor is shutdown
 - "PM" : the motor is shutdown but sluggish
 - "L" : the motor goes to the consign linearly to get the consign according to the pose duration
 - "S" : the motor goes to the consign with a zero initial speed and a zero final speed (cubic interpolation)
 - "K" : the motor is blocked to its initial position
- The second column manages the list of poses.
- The first is the tape column. The buutons Load and Save are here to manage and load the tapes you already did. The list below is not yet implemented


