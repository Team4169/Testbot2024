import commands2
import wpilib
import wpilib.drive
import ctre
import constants
import ntcore
import wpimath.controller
import navx
import rev
import math
from wpimath.geometry import Rotation2d 
class DriveSubsystem(commands2.SubsystemBase):
    def __init__(self, leftTalon, leftTalon2, rightTalon, rightTalon2) -> None:
        super().__init__()

        self.leftTalon = leftTalon
        self.leftTalon2 = leftTalon2
        self.rightTalon = rightTalon
        self.rightTalon2 = rightTalon2

        self.tpf = 4600/5
        self.maxDriveSpeed = 0.4
        self.maxTurnSpeed = 0.2

        #~ smartdashboard
        self.sd = ntcore.NetworkTableInstance.getDefault().getTable("SmartDashboard")

        self.posInitSD = self.sd.getIntegerTopic("posInit").subscribe(1)
        self.posEndSD = self.sd.getIntegerTopic("posEnd").subscribe(1)
        #self.targetSD = self.sd.getIntegerTopic("Target").subscribe(1)
        
        #self.target = self.targetSD.get()-1
        self.target = 1


        # Create PID Controller for Turning
        self.TurnkI = self.sd.getDoubleTopic("TurnkI").subscribe(0.0)
        self.TurnkP = self.sd.getDoubleTopic("TurnkP").subscribe(0.032)
        self.TurnkD = self.sd.getDoubleTopic("TurnkD").subscribe(0.0)
        self.turnController = wpimath.controller.PIDController(self.TurnkP.get(0.032), self.TurnkI.get(0), self.TurnkD.get(0))
        self.turnController.enableContinuousInput(-180.0, 180.0)
        self.turnController.setTolerance(10.0)

        # Create PID Controller for Drive
        self.DrivekP = self.sd.getDoubleTopic("DrivekP").subscribe(0.02)
        self.DrivekI = self.sd.getDoubleTopic("DrivekI").subscribe(0.02)
        self.DrivekD = self.sd.getDoubleTopic("DrivekD").subscribe(0.0005)
        self.driveController = wpimath.controller.PIDController(self.DrivekP.get(0.02), self.DrivekI.get(0.02), self.DrivekD.get(0.0005))
        self.driveController.setTolerance(-0.1 * self.tpf)

        #driver contstants for balancing
        self.balanceSensitivitySub = self.sd.getDoubleTopic("balanceSensitivity").subscribe(-2.0)
        # self.encoderTicks = self.sd.getDoubleTopic("encoder ticks").subscribe(0)

        # gyro
        self.gyro = navx.AHRS(wpilib.SerialPort.Port.kUSB1)
        self.gyroOut = self.sd.getDoubleTopic("Gyro Yaw").publish()
        
        self.gyroPitchOut = self.sd.getDoubleTopic("Gyro Pitch").publish()
        
        # The robot's drive
        self.rightTalon2.setInverted(True)
        self.rightTalon.setInverted(True)

        #encoders
        self.encoderLeftOut = self.sd.getDoubleTopic("Left Encoder").publish()
        self.encoderRightOut = self.sd.getDoubleTopic("Right Encoder").publish()
        self.drive = wpilib.drive.MecanumDrive(
            self.leftTalon,
            self.leftTalon2,
            self.rightTalon,
            self.rightTalon2,
        )

    def driveMecanum(self, x, y, z, angle=Rotation2d(0.0)):   
        self.drive.driveCartesian(x, y, z, angle)

    def resetEncoders(self) -> None:
        self.leftTalon.setSelectedSensorPosition(0, 0, 10)
        self.rightTalon.setSelectedSensorPosition(0, 0, 10)
        """Resets the drive encoders to currently read a position of 0."""

    def getAverageEncoderDistance(self) -> float:
        """Gets the average distance of the TWO encoders."""
        # self.sd.putValue("Left Encoder Value", self.leftTalon.getSelectedSensorPosition())
        # self.sd.putValue("Right Encoder Value", self.rightTalon.getSelectedSensorPosition())
        return (self.leftTalon.getSelectedSensorPosition()  / self.tpf)

    def getAverageEncoderTicks(self) -> float:
        """Gets the average distance of the TWO encoders."""
        # self.sd.putValue("Left Encoder Value", self.leftTalon.getSelectedSensorPosition())
        # self.sd.putValue("Right Encoder Value", self.rightTalon.getSelectedSensorPosition())
        return self.leftTalon.getSelectedSensorPosition() * -1


    def validateDriveSpeed(self, speed):
        if speed > self.maxDriveSpeed:
            return self.maxDriveSpeed
        if speed < -1 * self.maxDriveSpeed:
            return -1 * self.maxDriveSpeed
        return speed

    def validateTurnSpeed(self, turnSpeed):
        if turnSpeed > self.maxTurnSpeed:
            return self.maxTurnSpeed
        if turnSpeed < -1 * self.maxTurnSpeed:
            return -1 * self.maxTurnSpeed
        return turnSpeed
    
    def getDistanceAuto(self,cone:bool):
        y = constants.startPos[self.posInitSD.get()-1] + constants.cubeToConeDistance
        b = constants.endPos[self.posEndSD.get()-1] + constants.cubeToConeDistance
        if cone:
            y+= constants.cubeToConeDistance
            b+= constants.cubeToConeDistance

        a = constants.balanceDistance
        driveDistance = math.sqrt((abs(y - b) ** 2 + a ** 2))
        return driveDistance
    
    def getAngleAuto(self,cone:bool):
        y = constants.startPos[self.posInitSD.get()] + constants.cubeToConeDistance
        b = constants.endPos[self.posEndSD.get()] + constants.cubeToConeDistance
        if cone:
            y += constants.cubeToConeDistance
            b += constants.cubeToConeDistance
        a = constants.balanceDistance
        angle = math.atan(abs(y - b) / a)
        return angle

