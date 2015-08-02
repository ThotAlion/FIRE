# FIRE
## Introduction
The purpose of FIRE application is to control one or several robots from preporgrammed choregraphy to underactuated optimal control. The main objectives are :
- give confidence to the programmer (fast, transparent, easily verified, simple)
- master complexity (the threshold where the system is too complex to be controlled but be very far)
- master optimal control (the big advantage of FIRE)

## Architecture
### The flow
To manage very complex robots architecture, the structure of the control software must be very light and simple. This garantees a confidence from the programmer to its program, even under "FIRE" conditions. To do so, FIRE is composed around 4 classes :
- The interface : an interface is a component which delivers data to the software (from sensors for instance) and which receives data to export them in the real word (motor command). It can be considered as a robot. The structure of an interface is very linked to the electronic architecture of the robot but to get rid of this aspect during programmation (but it must be transparent!!)
- The system : it is the inverse of the interface since it receives inputs to produce outputs. It is like a function.
- The channel : it is a variable within a dictionnary, between interfaces and systems
- The connexion : each interface or system has a list of connexions. A connexion is a register to know which channel is connected to which input or output of the system or interface. It can be a channel but also a constant or a formula using channels (very useful to perform simple controls)

With a dictionnary of interfaces, systems, channels, it is possible to design a complete working robot program.

### Synchronous
FIRE is based on a synchronous language. That is to say, every n milliseconds, several mini operations are done. There is no "event" known for asynchronous languages but the coputation period is so small that we do not care on the date of the event.

### Graphical programming
This architecture is very useful for graphical programming. But it is very dangerous to present the new architecture as a graph (like Simulink). The software developed by FIRE are to be easily verified. The strategies to use are "synoptic interface" and as far as possible "one click view". It is dangerous to hide crucial control parameters to the programmer typically if we want to use local optimal control.

## Interface library
## System library

