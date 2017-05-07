import abc
from time import time
from math import cos
from math import sin
from math import degrees
from math import pi

from andabb.AngleUniverse import calculateDelta
from andabb.AngleUniverse import addDelta

WHEELS_DIST = 0.381
WHEELS_RAD = 0.0975


class Pose:
    def __init__(self, x=0, y=0, orientation=0):
        self.x = x
        self.y = y
        self.orientation = orientation

    def isZero(self):
        if self.x == 0 and self.y == 0 and self.orientation == 0:
            return True
        return False

    def __str__(self):
        return "[{:.2f}, {:.2f}, {:.3f} rad]".format(self.x, self.y, degrees(self.orientation))


class IPoseUpdater(object, metaclass=abc.ABCMeta):
    """
    Pose Updater strategy.
    """

    @abc.abstractmethod
    def update(self, robot):
        """
        This method returns the actual object pose.  
        :return: the object pose
        """
        raise NotImplementedError('This method must be implemented')


class GroundTruthPoseUpdater(IPoseUpdater):
    def update(self, robot):
        position = robot.sim.getObjectPosition(robot.handle)
        orientation = robot.sim.getObjectOrientation(robot.handle)
        p = Pose(position[0], position[1], orientation[2])
        print("GT pose: {}".format(p))

        return Pose(position[0], position[1], orientation[2])


class OdometryPoseUpdater(IPoseUpdater):
    def __init__(self):
        self.lastPose = Pose()
        self.lastTimestamp = time()
        self.lastRightEncoder = 0
        self.lastLeftEncoder = 0
        self.leftWheelClockWise = False
        self.rightWheelClockWise = False
        self.start = True

    def update(self, robot):
        now = time()

        encoderLeft = robot.sim.getJointPosition(robot.motorHandle[0])
        encoderRight = robot.sim.getJointPosition(robot.motorHandle[1])
        forceLeft = robot.sim.getJointForce(robot.motorHandle[0])
        forceRight = robot.sim.getJointForce(robot.motorHandle[1])

        if self.start:
            self.lastPose = robot.gtPose
            print("Start pose: {}".format(robot.gtPose))
            self.lastTimestamp = now
            self.lastRightEncoder = encoderLeft
            self.lastLeftEncoder = encoderRight
            self.start = self.lastPose.isZero()

            return self.lastPose

        timeDelta = now - self.lastTimestamp
        print("Encoder r {}, l {}, deltaT {}".format(degrees(encoderRight), degrees(encoderLeft), timeDelta))
        #print("Force r {}, l {}".format(forceRight, forceLeft))

        deltaEncoderRight = calculateDelta(self.lastRightEncoder, encoderRight, self.rightWheelClockWise)
        deltaEncoderLeft = calculateDelta(self.lastLeftEncoder, encoderLeft,  self.leftWheelClockWise)
        print("delta Encoder r {}, l {}".format(degrees(deltaEncoderRight), degrees(deltaEncoderLeft)))

        # Hack: trying to check if the orientation of the spin changed
        # FIXME needs verification
        if deltaEncoderRight > pi:
            deltaEncoderRight = (2*pi) - deltaEncoderRight
            self.rightWheelClockWise = not self.rightWheelClockWise
        if deltaEncoderLeft > pi:
            deltaEncoderLeft = (2*pi) - deltaEncoderLeft
            self.leftWheelClockWise = not self.leftWheelClockWise
        print("delta Encoder r {}, l {}".format(degrees(deltaEncoderRight), degrees(deltaEncoderLeft)))

        # TODO check this
        vR = speed(deltaEncoderRight, timeDelta, not self.rightWheelClockWise)
        vL = speed(deltaEncoderLeft, timeDelta, not self.leftWheelClockWise)

        print("vR {}, vL{}".format(vR, vL))

        deltaTheta = (vR - vL) * (timeDelta / WHEELS_DIST)
        deltaSpace = (vR + vL) * (timeDelta / 2)

        print("deltaSpace {}, deltaTheta{}".format(deltaSpace, degrees(deltaTheta)))

        x = self.lastPose.x + (deltaSpace * cos(addDelta(self.lastPose.orientation, deltaTheta / 2)))
        y = self.lastPose.y + (deltaSpace * sin(addDelta(self.lastPose.orientation, deltaTheta / 2)))
        theta = addDelta(self.lastPose.orientation, deltaTheta)

        self.lastTimestamp = now
        self.lastPose = Pose(x, y, theta)
        self.lastRightEncoder = encoderRight
        self.lastLeftEncoder = encoderLeft

        print("odometry {}".format(self.lastPose))
        return self.lastPose


def speed(angDelta, timeDelta, forward: bool):
    if forward:
        return WHEELS_RAD * (angDelta / timeDelta)
    return -(WHEELS_RAD * (angDelta / timeDelta))
