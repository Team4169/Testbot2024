import commands2

from subsystems.drivesubsystem import DriveSubsystem


class ResetGyro(commands2.CommandBase):
    def __init__(self, drive: DriveSubsystem) -> None:
        super().__init__()
        self.drive = drive

    def initialize(self) -> None:
        self.drive.gyro.reset()

    def execute(self) -> None:
        pass

    def end(self, interrupted: bool) -> None:
        pass

    def isFinished(self) -> bool:
        return True

