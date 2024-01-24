import commands2
import math

from subsystems.drivesubsystem import DriveSubsystem


class movecommandSpeed(commands2.CommandBase):
    def __init__(self, distance: float, maxspeed: float, drive: DriveSubsystem) -> None:
        super().__init__()
        # Feature to add - difference tolerance per command instance. Currently uses the default from DriveSubsystem
        # Feature to add - different max speed for each command. Currently uses method of DriveSubsystem.
        self.drive = drive
        self.targetTicks = distance * self.drive.tpf
        # print("distance goal", distance)
        # print("turn goal", heading)
        self.goal_threshold_ticks = 100 # I believe 50 ticks per second, confirm.
        # self.addRequirements(drive)
        self.maxspeed = maxspeed

    def initialize(self) -> None:
        self.drive.resetEncoders()
        # This increases everytime the robot remains in the target
        # self.drive.driveController.setSetpoint(self.distance)
        # self.drive.turnController.setSetpoint(self.heading)

    def execute(self) -> None:
        self.currDistance = self.drive.rightTalon.getSelectedSensorPosition()
        self.distanceToTarget =  self.currDistance - self.targetTicks
        self.distanceToTargetFeet = self.distanceToTarget / self.drive.tpf
        k = 3
        sign = abs(self.distanceToTarget)/self.distanceToTarget
        #self.speed = self.drive.maxDriveSpeed
        self.speed = 0.5 * self.maxspeed * (math.tanh((4 * (self.distanceToTargetFeet) - sign * k)/5) + sign * 1)
        if self.distanceToTargetFeet >= -0.2 and self.distanceToTargetFeet <= 0.2:
            self.speed = 0

        if abs(self.speed) < 0.15 and self.speed != 0:
            if self.speed < 0:
                self.speed = -0.15
            else:
                self.speed = 0.15
                
        # print('we done furreal')
        # self.drive.sd.putValue("Gyro Yaw", self.drive.gyro.getYaw())
        # self.drive.sd.putValue("distance goal new", self.distance)
        # self.drive.sd.putValue("turn goal", self.heading)
        # self.drive.sd.putValue("average ticks", self.drive.getAverageEncoderTicks())
        # turnCorrention = self.drive.gyro.getYaw() * -1 / 180
        
        self.drive.driveMecanum(self.speed,0,0)

    def end(self, interrupted: bool) -> None:
        self.drive.driveMecanum(0, 0, 0)
            


    def isFinished(self) -> bool:
        # self.arm.shouldMove = True
        return (abs(self.drive.rightTalon.getSelectedSensorPosition() - self.targetTicks) < abs(self.goal_threshold_ticks))