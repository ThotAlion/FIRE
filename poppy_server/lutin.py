import time
import numpy as np
from pypot.primitive import LoopPrimitive

class Lutin(LoopPrimitive):

    """ Primitive used to radio control the robot

    """

    def __init__(self, robot, freq):
        LoopPrimitive.__init__(self, robot, freq)
        self.freq = freq
        self.properties.append("present_pose")
        self.properties.append("goal_pose")
        self.number = "-1"

    def setup(self):
        a=1

    def update(self):
        t = time.time()
        # allocate the present_pose register
        a = {}
        p = {}
        for mot in self.robot.motors:
            p[mot.name] = np.round(mot.present_position*100)/100
            a[mot.name] = str(p[mot.name])
        self.present_pose = a
        
        # pilot robot function of goal_pose register
        b = self.goal_pose.copy()
        
        if b["Number"]==self.number:
            # during a pose
            for mot in b:
                if mot == "Number":
                    self.number = b["Number"]
                elif mot == "Duration":
                    temp = 1
                else:
                    m = getattr(self.robot,mot)
                    if b[mot][0] == "M":
                        if m.present_position<=m.lower_value:
                            m.compliant = False
                            m.goal_position = m.lower_value
                        elif m.present_position>=m.upper_value:
                            m.compliant = False
                            m.goal_position = m.upper_value
                        else:
                            m.compliant = True
                    elif b[mot][0] == "P":
                        m.compliant = False
                        m.goal_position = m.present_position
                    elif b[mot][0] == "K":
                        m.compliant = False
                        m.goal_position = self.p0[mot]
                    else:
                        m.compliant = False
                        m.goal_position = float(b[mot])
        else:
            # pose change
            self.p0 = p
            self.t0 = t
            self.v0 = self.v
            self.duration = float(b["duration"])
            self.number = b["Number"]
                
            

    


class MovePlayer(LoopPrimitive):

    """ Primitive used to play a :class:`~pypot.primitive.move.Move`.

    The playing can be :meth:`~pypot.primitive.primitive.Primitive.start` and :meth:`~pypot.primitive.primitive.Primitive.stop` by using the :class:`~pypot.primitive.primitive.LoopPrimitive` methods.

    .. warning:: the primitive is run automatically the same framerate than the move record.
        The play_speed attribute change only time lockup/interpolation
    """

    def __init__(self, robot, move=None, play_speed=1.0, move_filename=None, start_max_speed=50, **kwargs):
        self.move = move
        self.backwards = False
        if move_filename is not None:
            with open(move_filename, 'r') as f:
                self.move = Move.load(f)
        self.play_speed = play_speed if play_speed != 0 and isinstance(play_speed, float) else 1.0
        framerate = self.move.framerate if self.move is not None else 50.0
        self.start_max_speed = start_max_speed if start_max_speed != 0 else np.inf
        for key, value in kwargs.items():
            setattr(self, key, value)
        LoopPrimitive.__init__(self, robot, framerate)

    def setup(self):
        if self.move is None:
            raise AttributeError("Attribute move is not defined")
        self.period = 1.0 / self.move.framerate
        self.positions = self.move.positions()
        self.__duration = self.duration()
        if self.play_speed < 0:
            self.play_speed = - self.play_speed
            self.backwards = not self.backwards
        if self.play_speed == 0:
            self.play_speed = 1.0

        # Quick fix for limiting too fast movements at the play start
        max_goto_time = 0
        if self.backwards:
            position = self.positions[self.__duration]
        else:
            position = self.positions[0]
        for motor, value in position.iteritems():
            motor = getattr(self.robot, motor)
            motor.compliant = False
            delta_angle = abs(motor.present_position - value[0])
            if delta_angle > 5:
                goto_time = delta_angle / self.start_max_speed
                motor.goto_position(value[0], goto_time)
                max_goto_time = goto_time if goto_time > max_goto_time else max_goto_time

        time.sleep(max_goto_time)

    def update(self):
        if self.elapsed_time < self.__duration:
            if self.backwards:
                position = self.positions[(self.__duration - self.elapsed_time) * self.play_speed]
            else:
                position = self.positions[self.elapsed_time * self.play_speed]

            for motor, value in position.iteritems():
                # TODO: Ask pierre if its not a fgi to turn off the compliance
                getattr(self.robot, motor).compliant = False
                getattr(self.robot, motor).goal_position = value[0]
        else:
            self.stop()

    def duration(self):

        if self.move is not None:
            return (len(self.move.positions()) / self.move.framerate) / self.play_speed
        else:
            return 1.0
