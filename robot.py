#!/usr/bin/env python3
import typing
import wpilib
import commands2
import constants
from robotcontainer import RobotContainer
from deadzone import addDeadzone
import ntcore

class MyRobot(commands2.TimedCommandRobot):
    """
    Our default robot class, pass it to wpilib.run

    Command v2 robots are encouraged to inherit from TimedCommandRobot, which
    has an implementation of robotPeriodic which runs the scheduler for you
    """

    autonomousCommand: typing.Optional[commands2.Command] = None
    
    def robotInit(self) -> None:
        self.sd = wpilib.SmartDashboard
        """
        This function is run when the robot is first started up and should be used for any
        initialization code.
        """
    
        self.container = RobotContainer()

        self.driverController = self.container.driverController
        self.operatorController = self.container.operatorController

        self.leftTalon = self.container.leftTalon
        self.leftTalon2 = self.container.leftTalon2
        self.rightTalon = self.container.rightTalon
        self.rightTalon2 = self.container.rightTalon2
        
        self.drive = self.container.drive
        
    def disabledInit(self) -> None:
        """This function is called once each time the robot enters Disabled mode."""


    def disabledPeriodic(self) -> None:
        """This function is called periodically when disabled"""

    def autonomousInit(self) -> None:
        self.drive.gyro.reset()
        """This autonomous runs the autonomous command selected by your RobotContainer class."""
        self.autonomousCommand = self.container.getAutonomousCommand()
        
        if self.autonomousCommand:
            self.autonomousCommand.schedule()

    def autonomousPeriodic(self) -> None:
        """This function is called periodically during autonomous"""


    def teleopInit(self) -> None:
        
        self.sd.putNumber("moveRestriction", constants.moveRestriction)
        self.drive.resetEncoders()
        self.time = 0
        self.moveRestriction = 1

        if self.autonomousCommand:
            self.autonomousCommand.cancel()

        # print("Starting teleop...")
        self.humancontrol = True
        self.speed = 0
        self.intake = 0
        self.outtake = 0
        self.climbMode = False
        self.direction = 0
        self.areaPost = self.container.sd.getDoubleTopic("april_area").publish()
        self.yawPost = self.container.sd.getDoubleTopic("april_yaw").publish()
        self.idPost = self.container.sd.getDoubleTopic("april_id").publish()
        self.pastDetections = []

    def teleopPeriodic(self):
        # print(wpilib.DriverStation.getAlliance())
        self.drive.gyroOut.set(self.drive.gyro.getYaw())
        
        self.drive.gyroPitchOut.set(self.drive.gyro.getPitch())

        self.sd.putNumber("gyroYaw", self.drive.gyro.getYaw())
        self.sd.putNumber("gyroPitch", self.drive.gyro.getPitch())

        # self.drive.encoderTicks.set(self.drive.)
        self.sd.putNumber("left talon", self.leftTalon.getSelectedSensorPosition())
        self.sd.putNumber("right talon", self.rightTalon.getSelectedSensorPosition())
        
        self.drive.encoderRightOut.set(self.rightTalon.getSelectedSensorPosition())
        self.drive.encoderLeftOut.set(self.leftTalon.getSelectedSensorPosition())

        if self.driverController.getRightBumper() or self.driverController.getLeftBumper():
            self.moveRestriction = .5
        else:
            self.moveRestriction = 1
            
        self.leftX = addDeadzone(self.driverController.getLeftX() * self.moveRestriction) #* (self.sd.getNumber("moverestriction", constants.moveRestriction))) #/2 is to slow down the robot
        self.leftY = addDeadzone(self.driverController.getLeftY() * self.moveRestriction) #* (self.sd.getNumber("moverestriction", constants.moveRestriction)))
        self.rightX = addDeadzone(self.driverController.getRightX() * self.moveRestriction) #* (self.sd.getNumber("moverestriction", constants.moveRestriction)))
        
        self.moving = self.leftX != 0 or self.leftY != 0 or self.rightX != 0
        self.drive.driveMecanum( -self.leftY, self.leftX, self.rightX)

        if self.driverController.getStartButton():
            self.drive.gyro.reset()
    
    def testInit(self) -> None:
        # Cancels all running commands at the start of test mode
        commands2.CommandScheduler.getInstance().cancelAll()

if __name__ == "__main__":
    wpilib.run(MyRobot)