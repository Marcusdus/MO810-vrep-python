import abc
import logging
from math import atan2
from math import sqrt, degrees

from numpy import matrix

from .AngleUniverse import calculatePoint, addDelta
from .AngleUniverse import rotateAndTranslate
from .Robot import Pose
from .Robot import Robot


class DetectedBase:
    def __init__(self, localX, localY):
        self.localX = localX
        self.localY = localY
        self.realX = 0
        self.realY = 0

    def getAbsolutePosition(self, pose: Pose):
        #print("Here pose {}".format(pose))
        p = rotateAndTranslate([self.localX, self.localY, 1], pose.x, pose.y, pose.orientation)
        logging.debug("Global pos: {}".format(p))
        return p[0], p[1]

    def _getRealRangeAndBearing(self, pose: Pose):
        return self._rangeAndBearing(self.realX, self.realY, pose)

    def _getEstimatedRangeAndBearing(self, pose: Pose):
        x, y = self.getAbsolutePosition(pose)
        return self._rangeAndBearing(x, y, pose)

    def calculateResidualRangeAndBearing(self, pose:Pose):
        estimatedDist, estimatedBearing = self._getEstimatedRangeAndBearing(pose)
        realDist, realBearing = self._getRealRangeAndBearing(pose)
        return matrix([[estimatedDist - realDist],
                       [addDelta(estimatedBearing, -realBearing)]])

    def _rangeAndBearing(self, lx, ly, pose: Pose):
        x = lx - pose.x
        y = ly - pose.y
        dist = sqrt((x ** 2) + (y ** 2))
        bearing = addDelta(atan2(y, x), -pose.orientation)
        #print(atan2(y, x))
        #bearing = atan2(y, x) - pose.orientation
        logging.debug("range and bearing {}, {} degrees, {}".format(dist, degrees(bearing), bearing))
        return dist, bearing


class BaseDetector:
    def __init__(self, robot: Robot):
        self.robot = robot
        self.leftReceiver = "distance1"
        self.rightReceiver = "distance2"
        self.frontReceiver = "distance0"
        self.leftCoord = [-0.15, 0.1]
        self.rightCoord = [-0.15, -0.1]
        self.frontCoord = [0.1, 0]

    def detectBase(self) -> DetectedBase:
        leftDist = self.robot.sim.getDistance(self.leftReceiver)
        rightDist = self.robot.sim.getDistance(self.rightReceiver)
        frontDist = self.robot.sim.getDistance(self.frontReceiver)
        if leftDist == 0 or rightDist == 0 or frontDist == 0:
            return DetectedBase(0, 0)
        return self.calculateBase(leftDist, rightDist, frontDist)

    def calculateBase(self, leftDist, rightDist, frontDist):
        logging.debug("base: {}, {}, {}".format(leftDist, rightDist, frontDist))
        p = calculatePoint(self.leftCoord, self.rightCoord, self.frontCoord, leftDist, rightDist, frontDist)
        logging.debug("Point: {}".format(p))
        return DetectedBase(p[0], p[1])


class IBaseDetectionListener(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def baseDetected(self, base: DetectedBase):
        raise NotImplementedError('users must define baseDetected to use this base class')


class PrintBase(IBaseDetectionListener):
    def baseDetected(self, base: DetectedBase):
        print("base: {}".format(base.distance))
