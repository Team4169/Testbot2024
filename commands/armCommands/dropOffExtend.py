from subsystems.armsubsystem import ArmSubsystem
import commands2
from .setExtendingArm import setExtendingArm


class dropOffExtend(commands2.CommandBase):
    def __init__(self, distance, height, arm: ArmSubsystem) -> None:
        super().__init__()
        self.percent = distance
        # self.height = height
        self.arm= arm

    def initialize(self):
        pass

    def execute(self) -> None:
        # d = self.arm.dropOffExtentionAuto(self.distance,self.height)
        # self.percent = (20/d) * 100
        speed = 0.3 #expirement with this
        self.arm.setExtendingArmPercentWithAuto(self.percent,speed)

    def end(self, interrupted: bool) -> None:
        self.arm.setGrabbingArmSpeed(0)

    def isFinished(self) -> bool:
        return (abs(self.percent -self.arm.extendingArmEncoderPercent) <= self.arm.tolerance) or self.arm.getExtendingArmLimitSwitchMaxPressed()