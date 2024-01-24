from subsystems.armsubsystem import ArmSubsystem
import commands2
from .setRotatingArm import setRotatingArm

class dropOffAngle(commands2.CommandBase):
    def __init__(self, distance, height, arm: ArmSubsystem) -> None:
        super().__init__()
        self.angle = distance
        # self.height = height
        self.arm = arm

    def initialize(self):
        # self.arm.shouldMove = True
        print('in dropoff')
        

    def execute(self) -> None:
        speed = 0.3
        # self.angle = self.arm.dropOffAngleAuto(self.distance, self.height)
        # print(self.angle)
        self.arm.setRotatingArmAngle(self.angle, speed)

    def end(self, interrupted: bool) -> None:
        self.arm.setRotatingArmSpeed(0)

    def isFinished(self) -> bool:
        # self.drive.
        print(abs(self.angle -self.arm.rotatingArmEncoderDegrees))
        return (abs(self.angle -self.arm.rotatingArmEncoderDegrees) <= self.arm.tolerance)