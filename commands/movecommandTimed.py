import commands2
import wpilib
from subsystems.drivesubsystem import DriveSubsystem


class MoveCommandTimed(commands2.CommandBase):
    def __init__(self, distance: float, heading: float, drive: DriveSubsystem, time: float) -> None:
        super().__init__()
        # Feature to add - difference tolerance per command instance. Currently uses the default from DriveSubsystem
        # Feature to add - different max speed for each command. Currently uses method of DriveSubsystem.
        self.drive = drive
        self.distance = distance * -self.drive.tpf
        self.heading = heading
        # print("distance goal", distance)
        # print("turn goal", heading)
        self.goal_threshold_ticks = 25 # I believe 50 ticks per second, confirm.
        self.addRequirements(drive)
        self.time = time
        self.timer = wpilib.Timer()

    def initialize(self) -> None:
        self.drive.resetEncoders()
        # This increases everytime the robot remains in the target
        self.in_threshold = 0
        self.drive.driveController.setSetpoint(self.distance)
        self.drive.turnController.setSetpoint(self.heading)
        self.timer.reset()
        self.timer.start()

    def execute(self) -> None:
        # self.drive.sd.putValue("Gyro Yaw", self.drive.gyro.getYaw())
        # self.drive.sd.putValue("distance goal new", self.distance)
        # self.drive.sd.putValue("turn goal", self.heading)
        # self.drive.sd.putValue("average ticks", self.drive.getAverageEncoderTicks())
        if self.distance:
            drivespeed = self.drive.driveController.calculate(self.drive.getAverageEncoderTicks(), self.distance)
            # self.drive.sd.putValue("calculated drive speed",drivespeed)
            drivespeed = self.drive.validateDriveSpeed(drivespeed)
            # self.drive.sd.putValue("final calculated drive speed",drivespeed)
        else:
            drivespeed = 0
        turnspeed = self.drive.turnController.calculate(self.drive.gyro.getYaw(), self.heading)
        turnspeed = self.drive.validateTurnSpeed(turnspeed)
        self.drive.arcadeDrive(drivespeed, turnspeed)

    def end(self, interrupted: bool) -> None:
        self.drive.arcadeDrive(0, 0)

    def isFinished(self) -> bool:
        if self.drive.turnController.atSetpoint() and \
                (not self.distance or (self.distance and self.drive.driveController.atSetpoint())):
            self.in_threshold += 1
        else:
            self.in_threshold = 0
        # self.drive.sd.putValue("self.in_threshold", self.in_threshold)
        if self.in_threshold > self.goal_threshold_ticks:
            return True
        if self.timer.get() > self.time:
            return True
        return False

