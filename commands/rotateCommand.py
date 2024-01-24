import commands2
import math

from subsystems.drivesubsystem import DriveSubsystem


class rotateCommand(commands2.CommandBase):
    def __init__(self, angle: float, maxspeed: float, drive: DriveSubsystem) -> None:
        super().__init__()
        # Feature to add - difference tolerance per command instance. Currently uses the default from DriveSubsystem
        # Feature to add - different max speed for each command. Currently uses method of DriveSubsystem.
        self.drive = drive
        self.targetAngle = angle
        # print("distance goal", distance)
        # print("turn goal", heading)
        self.goal_threshold_angle = 1 # I believe 50 ticks per second, confirm.
        # self.addRequirements(drive)
        self.maxspeed = maxspeed

    def initialize(self) -> None:
        self.drive.resetEncoders()
        # This increases everytime the robot remains in the target
        # self.drive.driveController.setSetpoint(self.distance)
        # self.drive.turnController.setSetpoint(self.heading)

    def execute(self) -> None:
        self.currAngle = self.drive.gyro.getYaw()
        self.distanceToTarget =  self.currAngle - self.targetAngle
        k = 3
        sign = abs(self.distanceToTarget)/self.distanceToTarget
        #self.speed = self.drive.maxDriveSpeed
        self.speed = 0.3 #* self.maxspeed * (math.tanh((4 * (self.distanceToTarget) - sign * k)/5) + sign * 1)
        if self.distanceToTarget >= -1 and self.distanceToTarget <= 1:
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
        self.drive.driveMecanum(0,0,self.speed)

    def end(self, interrupted: bool) -> None:
        self.drive.driveMecanum(0, 0, 0)
            


    def isFinished(self) -> bool:
        # self.arm.shouldMove = True
        print(abs(self.drive.rightTalon.getSelectedSensorPosition() - self.targetAngle))
        return (self.drive.gyro.getPitch() < -11 or (abs(self.currAngle - self.targetAngle) < abs(self.goal_threshold_angle))) 