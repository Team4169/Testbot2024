import commands2

from subsystems.drivesubsystem import DriveSubsystem
import robotcontainer as container

import math

import constants

class balanceCommand(commands2.CommandBase):
    def __init__(self, drive: DriveSubsystem) -> None:
        super().__init__()
        self.drive = drive

    def initialize(self):
        pass

    def execute(self) -> None:
        self.drive.balanceSensitivitySub.get()
        self.gyroRad = self.drive.gyro.getYaw() * (math.pi / 180)
        self.pitchAngle = self.drive.gyro.getPitch()
        self.speed = constants.maxBalanceSpeed * 2 / (1 + math.e ** (-constants.balanceSensitivity * (self.pitchAngle / constants.maxBalanceAngle))) - constants.maxBalanceSpeed  # min(max(-abs(self.pitchAngle) + , 0), 1)

        self.drive.leftTalon.set(self.speed)
        self.drive.rightTalon.set(self.speed)
        self.drive.leftTalon2.set(self.speed)
        self.drive.rightTalon2.set(self.speed)
        #!important we should just get the arm function for balancing

    def end(self, interrupted: bool) -> None:
        pass

    def isFinished(self) -> bool:
        return False
    #Dont want function to terminate unil Auto is over




