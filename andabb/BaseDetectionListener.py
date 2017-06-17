import abc
import logging
from math import asin
from math import cos
from math import degrees
from math import pi
from math import sin
from math import sqrt

from .AngleUniverse import calculateFirstAngleFromTriangle, NoTriangleException, addDelta, calculatePoint
from .AngleUniverse import translateAndRotate, rotateAndTranslate
from .PoseUpdater import Pose
from .Robot import Robot
from .Robot import WHEELS_DIST


class DetectedBase:
    def __init__(self, x, y, leftDist=0, rightDist=0, backDist=0):
        #self.distance = distance
        self.angle = 1
        self.distance = 1
        # in radians
        self.x = x
        self.y = y
        self.left = leftDist
        self.right = rightDist
        self.back = backDist

    def getAbsolutePosition(self, pose: Pose):
        # return [pose.x + ((self.distance + (WHEELS_DIST / 2)) * cos(self.angle + pose.orientation)),
        #        pose.y + ((self.distance + (WHEELS_DIST / 2)) * sin(self.angle + pose.orientation))]
        #return pose.x + (self.distance * cos(self.angle + pose.orientation)), \
        #      pose.y + (self.distance * sin(self.angle + pose.orientation))
        # y = cos(self.angle) * self.distance
        # x = sin(self.angle) * self.distance
        # print("x: {}, y: {}".format(x,y))
        #pos = rotateAndTranslate([self.x, self.y, 1], pose.x, pose.y, pose.orientation)
        #print("pos: {}".format(pos))
        #return pos[0], pos[1]
        a = rotateAndTranslate([-0.15, 0.1, 1], pose.x, pose.y, pose.orientation)
        b = rotateAndTranslate([-0.15, -0.1, 1], pose.x, pose.y, pose.orientation)
        c = rotateAndTranslate([0.15, 0, 1], pose.x, pose.y, pose.orientation)
        #print(a)
        #print(b)
        #print(c)
        p = calculatePoint(a, b, c, self.left, self.right, self.back)
        #print("other: {}".format(p))
        return p[0], p[1]


class BaseDetector:
    def __init__(self, robot: Robot):
        self.robot = robot
        self.leftReceiver = "t1"
        self.rightReceiver = "t2"
        self.backReceiver = "t0"

    def detectBase(self) -> DetectedBase:
        leftDist = self.robot.sim.getDistance(self.leftReceiver)
        rightDist = self.robot.sim.getDistance(self.rightReceiver)
        backDist = self.robot.sim.getDistance(self.backReceiver)
        if leftDist == 0 or rightDist == 0 or backDist == 0:
            return DetectedBase(0, 0)
        print("base: {}, {}, {}".format(leftDist, rightDist, backDist))
        p = calculatePoint([-0.15, 0.1], [-0.15, -0.1], [0.15, 0], leftDist, rightDist, backDist)
        print("Point: {}".format(p))
        return mdetectBase(leftDist, rightDist, backDist)

def mdetectBase(leftDist, rightDist, backDist):
    #p = calculatePoint([0.445, WHEELS_DIST/2], [0.0445, -WHEELS_DIST/2], [-0.127, 0], leftDist, rightDist, backDist)
    p = calculatePoint([-0.15, 0.1], [-0.15, -0.1], [0.15, 0], leftDist, rightDist, backDist)
    print("Point: {}".format(p))
    return DetectedBase(p[0], p[1], leftDist, rightDist, backDist)
    # rad = WHEELS_DIST / 2
    #
    # diff = abs(abs(leftDist - rightDist) - WHEELS_DIST)
    # if diff <= 0.06:
    #     if leftDist > rightDist:
    #         return DetectedBase(rad+rightDist, -(pi/2))
    #     else:
    #         return DetectedBase(rad + leftDist, (pi / 2))
    #
    # try:
    #     angle = calculateFirstAngleFromTriangle(rightDist, WHEELS_DIST, leftDist)
    # except NoTriangleException:
    #     if leftDist > rightDist:
    #         return DetectedBase(rad+rightDist, -(pi/2))
    #     else:
    #         return DetectedBase(rad + leftDist, (pi / 2))
    #
    # print("firstang: {}".format(degrees(angle)))
    # # a2 = b2 + c2 − 2bc cosA
    #
    # dist = sqrt(leftDist ** 2 + rad ** 2 - (2 * leftDist * rad * cos(angle)))
    # sinang = (sin(angle) * rad)/leftDist
    # if sinang > 1:
    #     sinang = 1
    #     print("HERE")
    # elif sinang < -1:
    #     sinang = -1
    #     print("--here--")
    # smallAngle = asin(sinang)
    # nangle = pi - smallAngle - angle
    #
    # print(degrees(nangle))
    #
    # if 0 <= nangle <= (pi/2):
    #     if backDist > dist:
    #         nangle = (pi/2) - nangle
    #     else:
    #         nangle = (pi/2) + nangle
    # else:
    #     if backDist > dist:
    #         nangle = - (nangle - (pi/2))
    #     else:
    #         nangle = (pi/2) + nangle - (2*pi)
    # # dist = sin(angle) * rightDist
    # return DetectedBase(dist, nangle)


class IBaseDetectionListener(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def baseDetected(self, base: DetectedBase):
        raise NotImplementedError('users must define baseDetected to use this base class')


class PrintBase(IBaseDetectionListener):
    def baseDetected(self, base: DetectedBase):
        print("base: {}".format(base.distance))
