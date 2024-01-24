import commands2

import constants

from .drivedistance import DriveDistance
from .movecommand import MoveCommand
from subsystems.drivesubsystem import DriveSubsystem
#from subsystems.snowveyorsubsystem import SnowveyorSubsystem
from .reset_gyro import ResetGyro
import ntcore
import rev
import photonvision
from robotcontainer import photonCamera
#from .SnowVeyerCommands.pickUp import pickUp
#from .SnowVeyerCommands.dropOff import dropOff


class MoveForwardToAprilTag(commands2.CommandBase):
    """
    An auto command that moves the robot to the apriltag specified if in view
    """

    def __init__(self, drive: DriveSubsystem, tagID):
        super().__init__()
        self.drive = drive
        self.tagID = tagID
        self.range = 0


    def execute(self) -> None:
        result = photonCamera.getLatestResult()
        targets = result.targets
        target = 0
        for i in targets:
            if i.getFiducialId() == self.tagID:
                target = i
                break
        if target == 0:
            self.drive.driveMecanum(0, 0, 0)
        else:
            self.range = photonvision.PhotonUtils.calculateDistanceToTargetMeters(
                constants.cameraHeight,constants.targetHeight,constants.cameraPitch.Units.degreesToRadians(target.getPitch()))
            forwardSpeed = -self.drive.driveController.calculate(range, 1)
            rotationSpeed = -self.drive.turnController.calculate(target.getYaw(), 0)
            self.drive.driveMecanum(forwardSpeed,0,rotationSpeed)


    def isFinished(self) -> bool:
        if self.range <= 1:
            self.drive.driveMecanum(0,0,0)
            return True
        return False

