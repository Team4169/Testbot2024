from subsystems.armsubsystem import ArmSubsystem
import commands2
import constants

from subsystems.armsubsystem import ArmSubsystem

class setExtendingArm(commands2.CommandBase):
    def __init__(self, distance, arm: ArmSubsystem) -> None:
        super().__init__()
        self.distance = distance
        self.arm = arm

    def initialize(self):
        pass

    def execute(self) -> None:
        self.distance-=constants.minArmLength
        if self.distance<0:
            self.distance = 0

        self.percent = (self.distance/(constants.maxArmLength-constants.minArmLength)) * 100
        if self.percent > 100:
            self.percent = 100
        speed = 0.3 #expirement with this
        self.arm.setExtendingArmPercentWithAuto(self.percent,speed)

    def end(self, interrupted: bool) -> None:
        self.arm.setGrabbingArmSpeed(0)

    def isFinished(self) -> bool:
        return (abs(self.percent - self.arm.extendingArmEncoderPercent) <= self.arm.tolerance)