from subsystems.armsubsystem import ArmSubsystem
import commands2


class dropObject(commands2.CommandBase):
    def __init__(self, arm: ArmSubsystem) -> None:
        super().__init__()
        self.arm= arm

    def initialize(self):
        pass

    def execute(self) -> None:
        self.grabbingPressed = self.arm.getGrabbingArmLimitSwitchOpenPressed()
        self.arm.setGrabbingArmSpeed(-.5)
        # speed = 0.3
        # self.angle = 90 #This is a random guess fix later
        # self.arm.setGrabbingArmAngle(self.angle,speed)

    def end(self, interrupted: bool) -> None:
        self.arm.setGrabbingArmSpeed(0)

    def isFinished(self) -> bool:
        return self.arm.getGrabbingArmLimitSwitchOpenPressed()