#
# The constants module is a convenience place for teams to hold robot-wide
# numerical or boolean constants. Don't use this for any other purpose!
#

import math
import wpilib

# Motors
leftTalon = 3
leftTalon2 = 7
rightTalon = 9
rightTalon2 = 4

moveRestriction = .75
# Arm motors

extendingArmID = 11 
rotatingArmID = 12 
grabbingArmID = 13

# Arm encoders
grabbingArmEncoderPort = 0
positiveTicksPerDeg = 173/360
negativeTicksPerDeg = 221500/360

#todo: find the degrees that this should be 
startingRotatingDegrees = 50

#! extending arm give negative power as "foreward"
extendingArmRevPerArmPercent = -103.47 / 100
rotatingArmRevPerArmDegree = - 59 / 68 # / 360


# *Arm pickup systems
testDistance  = 21 #! this would be in place for the actual distance from the AI code
cameraDistanceFromArm = 20  #in meters (20 is inches), (39.37 is inches per meter)
pivotDistanceFromGround = 5.957 # in inches
armPickupHeight = 3.427 # in inches
maxArmLength = 68 # in inches
minArmLength = 35 # in inches
lowerArmAngleLimit = -7



# Autonomous
kAutoDriveDistanceInches = 60
kAutoBackupDistanceInches = 20
kAutoDriveSpeed = 0.2

# Operator Interface
kDriverControllerPort = 0
kArmControllerPort = 1

# Physical parameters
kDriveTrainMotorCount = 2
kTrackWidth = 0.381 * 2
kGearingRatio = 8
kWheelRadius = 0.0508

# kEncoderResolution = -


#SnowVeyor
intake = 10
outtake = 12

# Climbing
liftArm = 5
rotateArm = 4


liftArmSlowSpeed = .1
liftArmFastSpeed = .5
liftArmCloseToBottomTicks = -100
liftArmCloseToTopTicks = -500

rotateArmSlowSpeed = .05
rotateArmFastSpeed = .1
rotateArmCloseToRobotTicks = 50
rotateArmCloseToBackTicks = 100

deadzone = .1

maxBalanceAngle = 15
balanceSensitivity = -2.2
maxBalanceSpeed = .3

#Bottom (leftmost) cube drop off is origin
startPos = [0,67,133] # 0 67 133
endPos = [37,68,110] # 37 68 96
balanceDistance = 31
cubeToConeDistance = 22.8
dropOffDistance = 58 #Test This Distance
cubeTargetHeights = [2,23,35]
coneTargetHeights = [2,37,50]
