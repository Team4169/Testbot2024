import commands2
import constants
from .armCommands.dropOff import dropOff
from .armCommands.setExtendingArm import setExtendingArm
from .armCommands.setRotatingArm import setRotatingArm
from .balanceCommand import balanceCommand

from .movecommandSpeed import movecommandSpeed
from .armCommands.dropObject import dropObject
from .armCommands.dropOffAngle import dropOffAngle
from .armCommands.dropOffExtend import dropOffExtend
from .MoveTillGyro import moveTillGyro


from subsystems.drivesubsystem import DriveSubsystem
from subsystems.armsubsystem import ArmSubsystem
from .reset_gyro import ResetGyro
from commands2 import ParallelCommandGroup
#from .SnowVeyerCommands.pickUp import pickUp
#from .SnowVeyerCommands.dropOff import dropOff

'''
1.Holding Cube
2.Extend arm and deposit cube
3.Un Extend
4.Turn around
5.Drive to Balance
6.Face streight
7.Get up and balance 

'''


class cubeToBalanceAuto(commands2.SequentialCommandGroup):
    """
    An auto that drops off cone and goes onto balance
    """

    def __init__(self, drive: DriveSubsystem, arm: ArmSubsystem):
        super().__init__(
            # movecommandSpeed(0.16,.5,drive),
            # dropOffAngle(constants.dropOffDistance,constants.cubeTargetHeights[2],arm),
            dropOffAngle(28, 0, arm),
            dropOffExtend(98,0, arm),
            dropObject(arm),
            ParallelCommandGroup(dropOffExtend(1,0,arm),dropOffAngle(40,0,arm),moveTillGyro(-14,.5,drive))
            
            
            # dropOff(constants.dropOffDistance,constants.cubeTargetHeights[2], arm),
            # movecommandSpeed(-12,.3,drive)
            #rotateCommand(180, .3 , drive),
            # ResetGyro(drive),
            # dropOff(constants.dropOffDistance,constants.cubeTargetHeights[drive.target], arm),
            # setExtendingArm(0,arm),
            # setRotatingArm(0,arm),
            # MoveCommand(-5,0,drive),
            # MoveCommand(0,180, drive),
            # ResetGyro(drive),
            # MoveCommand(0,drive.getAngleAuto(False),drive),
            # MoveCommand(drive.getDistanceAuto(False)/12,0,drive),
            # MoveCommand(0,-drive.getAngleAuto(False),drive),
            # MoveCommand(0.5,0,drive),
            # balanceCommand(drive)
        )
