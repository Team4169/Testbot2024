#from subsystems.climbingsubsystem import ClimbingSubsystem
import commands2


class DoNothing(commands2.CommandBase):
    def __init__(self) -> None:
        super().__init__()


    def initialize(self):
        pass

    def execute(self) -> None:
        pass

    def end(self, interrupted: bool) -> None:
        pass
