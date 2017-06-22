import abc
from math import atan2
from math import sqrt
from typing import List

from numpy import matrix

from .AngleUniverse import calculatePoint, subAngles
from .AngleUniverse import rotateAndTranslate
from .Robot import Pose
from .Robot import Robot


class RealLandmark:
    def __init__(self, name, realX, realY):
        self.name = name
        self.realX = realX
        self.realY = realY

class DetectedBase:
    def __init__(self, realLandmark: RealLandmark, localX, localY):
        self.localX = localX
        self.localY = localY
        self.realX = realLandmark.realX
        self.realY = realLandmark.realY

    def getAbsolutePosition(self, pose: Pose):
        p = rotateAndTranslate([self.localX, self.localY, 1], pose.x, pose.y, pose.orientation)
        return p[0], p[1]

    def _getRealRangeAndBearing(self, pose: Pose):
        return self._rangeAndBearing(self.realX, self.realY, pose)

    def _getEstimatedRangeAndBearing(self, pose: Pose):
        x, y = self.getAbsolutePosition(pose)
        return self._rangeAndBearing(x, y, pose)

    def calculateResidualRangeAndBearing(self, pose: Pose):
        estimatedDist, estimatedBearing = self._getEstimatedRangeAndBearing(pose)
        realDist, realBearing = self._getRealRangeAndBearing(pose)
        return matrix([[estimatedDist - realDist],
                       [subAngles(estimatedBearing, realBearing)]])

    def _rangeAndBearing(self, lx, ly, pose: Pose):
        x = lx - pose.x
        y = ly - pose.y
        dist = sqrt((x ** 2) + (y ** 2))
        bearing = subAngles(atan2(y, x), pose.orientation)
        return dist, bearing


class BaseDetector:
    def __init__(self, robot: Robot):
        self.robot = robot
        self.leftReceiver = "Left"
        self.rightReceiver = "Right"
        self.frontReceiver = "Front"
        self.leftCoord = [-0.15, 0.1]
        self.rightCoord = [-0.15, -0.1]
        self.frontCoord = [0.1, 0]
        self.base1 = RealLandmark("Base", 0.0, 0.0)
        self.base2 = RealLandmark("Base2", 3.0, -3.0)

    def detectBase(self):
        return self._detectBase(self.base1), self._detectBase(self.base2)
        #return [self._detectBase(self.base2)]

    def _detectBase(self, realLandmark: RealLandmark):
        leftDist = self.robot.sim.getDistance(realLandmark.name + self.leftReceiver)
        rightDist = self.robot.sim.getDistance(realLandmark.name + self.rightReceiver)
        frontDist = self.robot.sim.getDistance(realLandmark.name + self.frontReceiver)
        print("{}, {}, {}".format(leftDist, rightDist, frontDist))
        if leftDist == 0 or rightDist == 0 or frontDist == 0:
            return DetectedBase(realLandmark, 0, 0)
        return self.calculateBase(realLandmark, leftDist, rightDist, frontDist)

    def calculateBase(self, realLandmark, leftDist, rightDist, frontDist):
        p = calculatePoint(self.leftCoord, self.rightCoord, self.frontCoord, leftDist, rightDist, frontDist)
        return DetectedBase(realLandmark, p[0], p[1])


class IBaseDetectionListener(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def baseDetected(self, bases: List[DetectedBase]):
        raise NotImplementedError('users must define baseDetected to use this base class')

