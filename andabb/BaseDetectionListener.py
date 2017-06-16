import abc
import logging
from math import asin
from math import cos
from math import degrees
from math import pi
from math import sin
from math import sqrt

from .AngleUniverse import calculateFirstAngleFromTriangle
from .AngleUniverse import translateAndRotate
from .PoseUpdater import Pose
from .Robot import Robot
from .Robot import WHEELS_DIST


class DetectedBase:
    def __init__(self, distance, angle):
        self.distance = distance
        self.angle = angle
        # in radians

    def getAbsolutePosition(self, pose: Pose):
        # return [pose.x + ((self.distance + (WHEELS_DIST / 2)) * cos(self.angle + pose.orientation)),
        #        pose.y + ((self.distance + (WHEELS_DIST / 2)) * sin(self.angle + pose.orientation))]
        # return pose.x + (self.distance * cos(addDelta(self.angle, pose.orientation))), \
        #       pose.y + (self.distance * sin(addDelta(self.angle, pose.orientation)))
        y = cos(self.angle) * self.distance
        x = sin(self.angle) * self.distance
        print("x: {}, y: {}".format(x,y))
        pos = translateAndRotate([x, y, 1], pose.x, pose.y, - pose.orientation)
        return pos[0], pos[1]


class BaseDetector:
    def __init__(self, robot: Robot):
        self.robot = robot
        self.leftReceiver = "DistanceLeft"
        self.rightReceiver = "DistanceRight"
        self.frontReceiver = "DistanceFront"

    def detectBase(self) -> DetectedBase:
        leftDist = self.robot.sim.getDistance(self.leftReceiver)
        rightDist = self.robot.sim.getDistance(self.rightReceiver)
        frontDist = self.robot.sim.getDistance(self.frontReceiver)
        logging.debug("Base distance: {}, {}, {}".format(leftDist, rightDist, frontDist))

        if leftDist == 0 or rightDist == 0:
            return DetectedBase(0, 0)

        angle = calculateFirstAngleFromTriangle(rightDist, WHEELS_DIST, leftDist)
        rad = WHEELS_DIST / 2
        dist = sqrt(leftDist ** 2 + rad ** 2 - (2 * leftDist * rad * cos(angle)))
        nangle = asin((sin(angle) * leftDist) / dist)
        nangle = pi - nangle
        if dist > frontDist:
            return DetectedBase(dist, pi-nangle)
        return DetectedBase(dist, 0)


def mdetectBase(leftDist, rightDist, frontDist):
    angle = calculateFirstAngleFromTriangle(rightDist, WHEELS_DIST, leftDist)
    print("firstang: {}".format(degrees(angle)))
    # a2 = b2 + c2 − 2bc cosA
    rad = WHEELS_DIST / 2
    dist = sqrt(leftDist ** 2 + rad ** 2 - (2 * leftDist * rad * cos(angle)))
    smallAngle = asin((sin(angle) * rad)/leftDist)
    nangle = pi - smallAngle - angle
    #nangle = pi - nangle
    print(degrees(nangle))
    if dist > frontDist:
        return DetectedBase(dist, -nangle)
    # dist = sin(angle) * rightDist
    return DetectedBase(dist, nangle)


class IBaseDetectionListener(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def baseDetected(self, base: DetectedBase):
        raise NotImplementedError('users must define baseDetected to use this base class')


class PrintBase(IBaseDetectionListener):
    def baseDetected(self, base: DetectedBase):
        print("base: {}".format(base.distance))
