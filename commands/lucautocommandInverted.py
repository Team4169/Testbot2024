import commands2

import constants

from .drivedistance import DriveDistance
from .movecommand import MoveCommand
from subsystems.drivesubsystem import DriveSubsystem
#from subsystems.snowveyorsubsystem import SnowveyorSubsystem
from .reset_gyro import ResetGyro
from .SnowVeyerCommands.PickUp import pickUp
from .SnowVeyerCommands.DropOff import dropOff

class LucAutoCommand2(commands2.SequentialCommandGroup):
    """
    A complex auto command that drives forward, releases a hatch, and then drives backward.
    """

    def __init__(self, drive: DriveSubsystem, snowveyor: SnowveyorSubsystem):
        super().__init__(
            # Drive forward the specified distance
            ResetGyro(drive),
            MoveCommand(3.6666667, 0, drive),
            MoveCommand(0, -65, drive),
            MoveCommand(0.75, -65, drive),
            dropOff(1.5, -1, snowveyor),
            MoveCommand(-0.75, -65, drive),
            MoveCommand(0, 130, drive),
            MoveCommand(6.42, 130, drive),
            pickUp(1, 1, snowveyor),
            MoveCommand(0, -50, drive),
            MoveCommand(6.42, -50, drive),
            MoveCommand(0, -67.5, drive),
            MoveCommand(1, -67.5, drive),
            dropOff(1.5, -1, snowveyor),
            MoveCommand(-1, -67.5, drive),
            # DriveDistance(
            #     constants.kAutoDriveDistanceInches, constants.kAutoDriveSpeed, drive
            # ),
            # # Drive backward the specified distance
            # DriveDistance(
            #     constants.kAutoBackupDistanceInches, -constants.kAutoDriveSpeed, drive
            # ),
        )
