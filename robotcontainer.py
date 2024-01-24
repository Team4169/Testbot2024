import wpilib
import ntcore
import ctre
import commands2
import commands2.button
import constants
from subsystems.drivesubsystem import DriveSubsystem

class RobotContainer:
    """
    This class is where the bulk of the robot should be declared. Since Command-based is a
    "declarative" paradigm, very little robot logic should actually be handled in the :class:`.Robot`
    periodic methods (other than the scheduler calls). Instead, the structure of the robot (including
    subsystems, commands, and button mappings) should be declared here.
    """

    def __init__(self) -> None:

        self.driverController = wpilib.XboxController(constants.kDriverControllerPort)
        self.operatorController = wpilib.XboxController(constants.kArmControllerPort)

        self.leftTalon = ctre.WPI_TalonSRX(constants.leftTalon)
        self.leftTalon2 = ctre.WPI_TalonSRX(constants.leftTalon2)
        self.rightTalon = ctre.WPI_TalonSRX(constants.rightTalon)
        self.rightTalon2 = ctre.WPI_TalonSRX(constants.rightTalon2)

        self.coastBool=False

        # The robot's subsystems

        self.drive = DriveSubsystem(leftTalon=self.leftTalon,
                                    leftTalon2=self.leftTalon2,
                                    rightTalon=self.rightTalon,
                                    rightTalon2=self.rightTalon2)

        inst = ntcore.NetworkTableInstance.getDefault()
        self.sd = inst.getTable("SmartDashboard")
        
        #chooser
        self.chooser = wpilib.SendableChooser()
        self.shuffle = wpilib.SmartDashboard

    def getAutonomousCommand(self) -> commands2.Command:
        return self.chooser.getSelected()
        # return self.coneToBalance