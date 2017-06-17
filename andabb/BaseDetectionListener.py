import abc
import logging

from .AngleUniverse import calculatePoint
from .AngleUniverse import rotateAndTranslate
from .PoseUpdater import Pose
from .Robot import Robot


class DetectedBase:
    def __init__(self, localX, localY):
        self.localX = localX
        self.localY = localY

    def getAbsolutePosition(self, pose: Pose):
        p = rotateAndTranslate([self.localX, self.localY, 1], pose.x, pose.y, pose.orientation)
        logging.debug("Global pos: {}".format(p))
        return p[0], p[1]


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
