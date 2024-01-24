import commands2

import constants

from .drivedistance import DriveDistance
from .movecommand import MoveCommand
from subsystems.drivesubsystem import DriveSubsystem
#from subsystems.snowveyorsubsystem import SnowveyorSubsystem
from .reset_gyro import ResetGyro
import ntcore
import rev
#from .SnowVeyerCommands.pickUp import pickUp
#from .SnowVeyerCommands.dropOff import dropOff


class MoveForwardToVisionTarget(commands2.CommandBase):
    """
    An auto command that spins a motor based on limelight target detection
    """

    def __init__(self, drive: DriveSubsystem, motor): #def __init__(self, drive: DriveSubsystem, snowveyor: SnowveyorSubsystem):
        super().__init__()
        self.drive = drive
        self.tx = 0
        self.ty = 0
        self.ta = 0
        self.ts = 0
        self.tv = 0
        self.neoMotor = motor
        self.ticks = 0 #note: reset this every time the program runs
        self.tickgoal = 500 # 10 seconds at 50 tps

    def execute(self) -> None:
        # table = NetworkTables.getTable("limelight")
        self.tx = table.getNumber('tx', None)
        self.ty = table.getNumber('ty', None)
        self.ta = table.getNumber('ta', None)
        self.ts = table.getNumber('ts', None)
        self.tv = table.getNumber('tv', None)
        print(f"Ta:{self.ta}, type:{type(self.ta)}")
        # self.drive.sd.putValue("ta", str(self.ta))
        #TV: anything is being detected
        if self.tv == 1:
            self.neoMotor.set(0)

            #self.drive.arcadeDrive(0.5,0)
            #Try this again to see if driving is choppy^

            if self.ta < 1:

                print("Driving UwU")
                self.drive.arcadeDrive(0.7, 0)
            else:
                print("not driving :(")
                self.drive.arcadeDrive(0, 0)
            #
            #
            # else:
            #     self.drive.arcadeDrive(0,0)
            # if self.tx < -1:
            #     pass
            #     # turn the robot right
            # elif self.tx > 1:
            #     pass
            #     # turn the robot left
        else:
            self.neoMotor.set(0.1)
            self.drive.arcadeDrive(0, 0)

    def isFinished(self) -> bool:
        self.ticks += 1
        if self.ticks >= self.tickgoal:
            self.neoMotor.set(0)
            self.ticks = 0
            return True
        return False
