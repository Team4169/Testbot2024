import commands2
import wpilib
import wpilib.drive
import constants
import ntcore
import rev
import math

class ArmSubsystem(commands2.SubsystemBase):
    def __init__(self, extendingArm, rotatingArm, grabbingArm, extendingArmLimitSwitchMin, extendingArmLimitSwitchMax, rotatingArmLimitSwitchMin, rotatingArmLimitSwitchMax, grabbingArmLimitSwitchOpen, grabbingArmLimitSwitchClosed, extendingArmEncoder, rotatingArmEncoder, grabbingArmEncoder) -> None:
        super().__init__()
        # commands2.SubsystemBase.__init__(self)
        # ~ smartdashboard
        self.sd = ntcore.NetworkTableInstance.getDefault().getTable("SmartDashboard")
        
        #* Arm motors
        self.extendingArm = extendingArm
        self.rotatingArm = rotatingArm
        self.grabbingArm = grabbingArm

        #* limit switches
        self.extendingArmLimitSwitchMin = extendingArmLimitSwitchMin
        self.extendingArmLimitSwitchMax = extendingArmLimitSwitchMax
        self.rotatingArmLimitSwitchMin = rotatingArmLimitSwitchMin
        self.rotatingArmLimitSwitchMax = rotatingArmLimitSwitchMax
        self.grabbingArmLimitSwitchOpen = grabbingArmLimitSwitchOpen
        self.grabbingArmLimitSwitchClosed = grabbingArmLimitSwitchClosed

        #~ smartDashboard limit switches
        self.extendingArmLimitSwitchMinVal = self.sd.getDoubleTopic("ExtendArmLimitMin").publish()
        self.extendingArmLimitSwitchMaxVal = self.sd.getDoubleTopic("ExtendArmLimitMax").publish()
        self.rotatingArmLimitSwitchMinVal = self.sd.getDoubleTopic("RotArmLimitMin").publish()
        self.rotatingArmLimitSwitchMaxVal = self.sd.getDoubleTopic("RotArmLimitMax").publish()
        self.grabbingArmLimitSwitchOpenVal = self.sd.getDoubleTopic("GrabbingLimitOpen").publish()
        self.grabbingArmLimitSwitchClosedVal = self.sd.getDoubleTopic("GrabbingLimitClosed").publish()
        self.extindingArmPercentVal = self.sd.getDoubleTopic("extendingPercent").publish()

        #* encoders
        self.extendingArmEncoder = extendingArmEncoder
        self.rotatingArmEncoder = rotatingArmEncoder
        self.grabbingArmEncoder = grabbingArmEncoder

        self.grabbingArmEncoderDegrees = 0.0
        self.previousGrabbingArmEncoderTicks = 0.0

        #~ smartDashboard encoders

        self.grabbingDegrees = self.sd.getDoubleTopic("grabbingDegrees").publish()
        self.extendingArmRevolutions = self.sd.getDoubleTopic("ExtendArmRevs").publish()
        self.rotatingArmRevolutions = self.sd.getDoubleTopic("RotArmRevs").publish()
        self.rotatingArmEncoderDegreesVal = self.sd.getDoubleTopic("RotArmDegrees").publish()

        
        self.rotatingArmEncoderDegrees = self.rotatingArmEncoder.getPosition() / constants.rotatingArmRevPerArmDegree
        self.extendingArmEncoderPercent = self.extendingArmEncoder.getPosition() / constants.extendingArmRevPerArmPercent


        # self.left1.setSelectedSensorPosition(0, 0, 10)
        # self.right2.setSelectedSensorPosition(0, 0, 10)
        self.shouldMove = False
        self.shouldMoveVal = self.sd.getBooleanTopic("shouldMove").publish()
        """Resets the drive encoders to currently read a position of 0."""
#* periodic functions
    def updateDegreesAndPercent(self):
        self.rotatingArmEncoderDegrees = self.rotatingArmEncoder.getPosition() / constants.rotatingArmRevPerArmDegree
        self.extendingArmEncoderPercent = self.extendingArmEncoder.getPosition() / constants.extendingArmRevPerArmPercent
    

# * Extending Arm functions
    def getExtendingArmLimitSwitchMinPressed(self) -> bool:
        """Gets if the limit switch is pressed"""
        return self.extendingArmLimitSwitchMin.get()
    
    def getExtendingArmLimitSwitchMaxPressed(self) -> bool:
        """Gets if the limit switch is pressed"""
        return self.extendingArmLimitSwitchMax.get()
    
    # limit Switch gaurds https://docs.google.com/spreadsheets/d/1Ywz5rC-dYjaaNjmlx7t1RDW8TRrBJ6oTPnMUaNfTfJ0/edit#gid=1791774740
    def setExtendingArmSpeed(self, speed):
        """Sets the speed of the extending arm"""
        if self.getExtendingArmLimitSwitchMaxPressed() and speed < 0:
            self.extendingArm.set(0)
        elif self.getExtendingArmLimitSwitchMinPressed() and speed > 0:
            self.extendingArm.set(0)
            self.resetExtendingArmEncoder()
        else:
            self.extendingArm.set(speed)
    #condition spreadsheet https://docs.google.com/spreadsheets/d/1Ywz5rC-dYjaaNjmlx7t1RDW8TRrBJ6oTPnMUaNfTfJ0/edit#gid=0
    def setExtendingArmSpeedWithAuto(self, speed):
        """Sets the speed of the extending arm"""
        #& if the rotating arm is between -7 and 24 degrees
         #& if the extending arm is greater than 75% of the way out
        # print(self.rotatingArmEncoderDegrees >= constants.lowerArmAngleLimit, self.rotatingArmEncoderDegrees <= 24, self.extendingArmEncoderPercent > 70)
        if self.rotatingArmEncoderDegrees <= 24 and \
            self.extendingArmEncoderPercent > 72:
                print("should move down")
                self.shouldMove = True
                #& move down to 75 % extension
                self.setExtendingArmPercentWithAuto(69, .25) 
        else:
            self.shouldMove = False
            self.setExtendingArmSpeed(speed)

    # def setExtendingArmPercent(self, percent, speed):
    #     speed = abs(speed)
    #     """Sets the angle of the extending arm"""
    #     self.tolerance = 0
    #     if percent - self.tolerance > self.extendingArmEncoderPercent:
    #         self.setExtendingArmSpeed(speed)
    #     elif percent + self.tolerance < self.extendingArmEncoderPercent:
    #         self.setExtendingArmSpeed(-speed)
    #     else:
    #         self.setExtendingArmSpeed(0)
    
    #^ test this code, it will automatically apply limits on the extending arm
    
    def setExtendingArmPercentWithAuto(self, percent, speed):   
        speed = -abs(speed)
        self.tolerance = .5
        """Sets the angle of the extending arm"""
        if percent - self.tolerance > self.extendingArmEncoderPercent:
            self.setExtendingArmSpeed(speed)
        elif percent + self.tolerance < self.extendingArmEncoderPercent:
            self.setExtendingArmSpeed(-speed)
        else:
            self.setExtendingArmSpeed(0)

    def resetExtendingArmEncoder(self):
        """Resets the extending arm encoder"""
        self.extendingArmEncoder.setPosition(0)

    def zeroExtendingArm(self):
        """Zeroes the extending arm"""
        if self.getExtendingArmLimitSwitchMinPressed():
            self.resetExtendingArmEncoder()
            self.setExtendingArmSpeed(0)
        else: 
            self.setExtendingArmSpeed(.1)
    
# * Rotating Arm functions
    def getRotatingArmLimitSwitchMinPressed(self) -> bool:
        """Gets if the limit switch is pressed"""
        return self.rotatingArmLimitSwitchMin.get()
    
    def getRotatingArmLimitSwitchMaxPressed(self) -> bool:
        """Gets if the limit switch is pressed"""
        return self.rotatingArmLimitSwitchMax.get()
    
    def setSpeed(self, speed):
        self.rotatingArm.set(speed)
    
    def setRotatingArmSpeed(self, speed):
        """Sets the speed of the Rotating arm"""
        if self.getRotatingArmLimitSwitchMaxPressed() and speed < 0:
            self.rotatingArm.set(0)
        elif self.getRotatingArmLimitSwitchMinPressed() and speed > 0:
            self.rotatingArm.set(0)
            self.resetRotatingArmEncoder()
        else:
            self.rotatingArm.set(speed)

    def setRotatingArmSpeedWithAuto(self, speed):
        """Sets the speed of the Rotating arm"""
        if (self.rotatingArmEncoderDegrees > 65 and speed < 0 ):
            self.setRotatingArmSpeed(0)
        # elif (self.rotatingArmEncoderDegrees <  constants.lowerArmAngleLimit and speed > 0):
        #     self.setRotatingArmAngle(-6, .1)
        else:
            self.setRotatingArmSpeed(speed)
  
    def setRotatingArmAngle(self, angle, speed):
        new_speed = -abs(speed)
        """Sets the angle of the Rotating arm"""
        self.tolerance = .5
        if angle - self.tolerance > self.rotatingArmEncoderDegrees:
            self.setRotatingArmSpeed(new_speed)
        elif angle + self.tolerance < self.rotatingArmEncoderDegrees:
            self.setRotatingArmSpeed(-new_speed)
        else:
            self.setRotatingArmSpeed(0)
    
    def resetRotatingArmEncoder(self):
        self.rotatingArmEncoder.setPosition(constants.lowerArmAngleLimit * constants.rotatingArmRevPerArmDegree) # ! we may not be able to set the encoder to negative degrees

    def initializeDegreesOnStart(self):
        self.rotatingArmEncoder.setPosition(constants.startingRotatingDegrees * constants.rotatingArmRevPerArmDegree) # ! we may not be able to set the encoder to negative degrees

    def zeroRotatingArm(self):
        """Zeroes the Rotating arm"""
        if self.getRotatingArmLimitSwitchMinPressed():
            self.resetRotatingArmEncoder()
            self.setRotatingArmSpeed(0)
        else: 
            self.setRotatingArmSpeed(.2)

    
# * Grabbing Arm functions
    def getGrabbingArmLimitSwitchClosedPressed(self) -> bool:
        """Gets if either limit switch is pressed"""
        return self.grabbingArmLimitSwitchClosed.get()
    
    def getGrabbingArmLimitSwitchOpenPressed(self) -> bool:
        """Gets if either limit switch is pressed"""
        return self.grabbingArmLimitSwitchOpen.get()
    
    def setGrabbingArmSpeedWithLimitSwitches(self, speed):
        """Sets the speed of the grabbing arm"""
        if self.getGrabbingArmLimitSwitchClosedPressed() and speed > 0:
            self.grabbingArm.set(0)
        elif self.getGrabbingArmLimitSwitchOpenPressed() and speed < 0:
            self.grabbingArm.set(0)
            self.resetGrabbingArmEncoder()
        else:
            self.grabbingArm.set(speed)
    
    def setGrabbingArmSpeed(self, speed):
        """for some reason the encoder ticks are significantly different when going down versus when going up"""
        # & Sets the speed
        self.setGrabbingArmSpeedWithLimitSwitches(speed)
        #& Updates the current encoder location
        self.current = self.grabbingArmEncoder.get()
        #& Updates the smartdashboard
        # //self.realTicks.set(self.grabbingArmEncoder.get())
        # //self.previousTicks.set(self.previousGrabbingArmEncoderTicks)
        #& gets the difference in ticks from the previous location
        self.diff = self.current - self.previousGrabbingArmEncoderTicks
        #& converts the diff into degrees depending on direction of travel
        if speed < 0:
            self.grabbingArmEncoderDegrees += self.diff / constants.negativeTicksPerDeg
        elif speed > 0:
            self.grabbingArmEncoderDegrees -= self.diff / constants.positiveTicksPerDeg
        #& changes current
        self.previousGrabbingArmEncoderTicks = self.current

    def setGrabbingArmAngle(self, angle, speed):
        new_speed = -abs(speed)
        self.tolerance = .5 #? should this be in the constants file?
        if angle - self.tolerance > self.grabbingArmEncoderDegrees:
            self.setGrabbingArmSpeed(new_speed)
        elif angle + self.tolerance < self.grabbingArmEncoderDegrees:
            self.setGrabbingArmSpeed(-new_speed)
        else:
            self.setGrabbingArmSpeed(0)
    
    def grabCube(self):
        self.setGrabbingArmAngle(119, .75)
    
    def grabCone(self):
        self.setGrabbingArmAngle(88 , .75)

    #^ test this function

    def zeroGrabbingArm(self):
        if self.getGrabbingArmLimitSwitchOpenPressed():
            self.resetGrabbingArmEncoder()
            self.setGrabbingArmSpeed(0)
        else: 
            self.setGrabbingArmSpeed(-.1)
    
    def resetGrabbingArmEncoder(self) -> None:
        self.grabbingArmEncoder.reset()
        self.grabbingArmEncoderDegrees = 67.5
        self.previousGrabbingArmEncoderTicks = 0