import commands2

import constants

from .drivedistance import DriveDistance
from .movecommand import MoveCommand
from subsystems.drivesubsystem import DriveSubsystem
#from subsystems.snowveyorsubsystem import SnowveyorSubsystem
from .reset_gyro import ResetGyro
#from .SnowVeyerCommands.pickUp import pickUp
#from .SnowVeyerCommands.dropOff import dropOff

class LucAutoCommand(commands2.SequentialCommandGroup):
    """
    A complex auto command that drives forward, releases a hatch, and then drives backward.
    """

    def __init__(self, drive: DriveSubsystem): #def __init__(self, drive: DriveSubsystem, snowveyor: SnowveyorSubsystem):
        super().__init__(
            # Drive forward the specified distance
            ResetGyro(drive),
            MoveCommand(5, 0, drive),
            # MoveCommand(0, 120, drive),
            # MoveCommand(5, 120,drive),
            # MoveCommand(0,240, drive),
            # MoveCommand(5,240, drive),

            #MoveCommand(5, 360, drive)
        )
