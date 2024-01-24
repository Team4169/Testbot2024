import commands2


from .dropOffExtend import dropOffExtend
from .dropOffAngle import dropOffAngle
from .dropObject import dropObject

from subsystems.armsubsystem import ArmSubsystem

class dropOff(commands2.SequentialCommandGroup):
    """
    A complex auto command that drives forward, releases a hatch, and then drives backward.
    """

    def __init__(self, distance,height, arm:ArmSubsystem):
        super().__init__(
            # Drive forward the specified distance
            dropOffAngle(distance,height,arm),
            dropOffExtend(distance, height, arm),
            dropObject(arm)
            )