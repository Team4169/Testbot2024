import commands2
import constants
import os
from .armCommands.dropOff import dropOff
from .armCommands.setExtendingArm import setExtendingArm
from .armCommands.setRotatingArm import setRotatingArm

from .balanceCommand import balanceCommand

from .movecommand import MoveCommand
from .movecommandSpeed import movecommandSpeed
from subsystems.drivesubsystem import DriveSubsystem
from subsystems.armsubsystem import ArmSubsystem
from .MoveTillGyro import moveTillGyro
from .reset_gyro import ResetGyro
from .resetEncoders import ResetEncoders
from .rotateCommand import rotateCommand

'''
1.Holding Cone
2.Extend arm and deposit cone
3.Un Extend
4.Turn around
5.Drive to Balance
6.Face streight
7.Get up and balance 

'''
#variable = __import__('module').class.variable 



class simpleAuto(commands2.SequentialCommandGroup):
    """
    An auto that drops off cone and goes onto balance
    """
    
    def __init__(self, drive: DriveSubsystem, arm: ArmSubsystem):
        super().__init__ (
            ResetEncoders(drive),
            ResetGyro(drive),
            # movecommandSpeed(0.16,.5,drive),
            # dropOff(constants.dropOffDistance,constants.cubeTargetHeights[2], arm),
            # movecommandSpeed(-12,.3,drive)
            #rotateCommand(180, .3 , drive),
            
            moveTillGyro(1.5,1,drive),
            moveTillGyro(-14,.3,drive),
            

            # balanceCommand(drive)

            # MoveCommand(-5, 0, drive)
            # ResetGyro(drive),
            # moveTillGyro(drive, arm),
            # balanceCommand(drive)
            #dropOff(constants.dropOffDistance,constants.coneTargetHeights[drive.target], arm),
            #setExtendingArm(0,arm),
            # setRotatingArm(0,arm),
            # MoveCommand(-5,0,drive),
            # MoveCommand(0,180, drive),
            # ResetGyro(drive),
            # MoveCommand(0,drive.getAngleAuto(True),drive),
            # MoveCommand(drive.getDistanceAuto(True)/12,0,drive),
            # MoveCommand(0,-drive.getAngleAuto(True),drive),
            # MoveCommand(0.5,0,drive),
            # balanceCommand(drive)
            )
