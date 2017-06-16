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
        return pose.x + (self.distance * cos(self.angle + pose.orientation)), \
              pose.y + (self.distance * sin(self.angle + pose.orientation))
        # y = cos(self.angle) * self.distance
        # x = sin(self.angle) * self.distance
        # print("x: {}, y: {}".format(x,y))
        # pos = translateAndRotate([x, y, 1], pose.x, pose.y, - pose.orientation)
        # return pos[0], pos[1]


class BaseDetector:
    def __init__(self, robot: Robot):
        self.robot = robot
        self.leftReceiver = "DistanceLeft"
        self.rightReceiver = "DistanceRight"
        self.backReceiver = "DistanceBack"

    def detectBase(self) -> DetectedBase:
        leftDist = self.robot.sim.getDistance(self.leftReceiver)
        rightDist = self.robot.sim.getDistance(self.rightReceiver)
        backDist = self.robot.sim.getDistance(self.backReceiver)
        if leftDist == 0 or rightDist == 0 or backDist == 0:
            return DetectedBase(0, 0)
        print("base: {}, {}, {}".format(leftDist, rightDist, backDist))
        return mdetectBase(leftDist, rightDist, backDist)


def mdetectBase(leftDist, rightDist, backDist):
    angle = calculateFirstAngleFromTriangle(rightDist, WHEELS_DIST, leftDist)
    print("firstang: {}".format(degrees(angle)))
    # a2 = b2 + c2 − 2bc cosA
    rad = WHEELS_DIST / 2
    dist = sqrt(leftDist ** 2 + rad ** 2 - (2 * leftDist * rad * cos(angle)))
    sinang = (sin(angle) * rad)/leftDist
    if sinang > 1:
        sinang = 1
    elif sinang < -1:
        sinang = -1
    smallAngle = asin(sinang)
    nangle = pi - smallAngle - angle

    print(degrees(nangle))

    if 0 <= nangle <= (pi/2):
        if backDist > dist:
            nangle = (pi/2) - nangle
        else:
            nangle = (pi/2) + nangle
    else:
        if backDist > dist:
            nangle = - (nangle - (pi/2))
        else:
            nangle = (pi/2) + nangle - (2*pi)
    # dist = sin(angle) * rightDist
    return DetectedBase(dist, nangle)


class IBaseDetectionListener(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def baseDetected(self, base: DetectedBase):
        raise NotImplementedError('users must define baseDetected to use this base class')


class PrintBase(IBaseDetectionListener):
    def baseDetected(self, base: DetectedBase):
        print("base: {}".format(base.distance))
