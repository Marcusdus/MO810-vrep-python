import abc
from typing import List

class DetectedObject:
    def __init__(self, dist, angle):
        self.dist = dist
        self.angle = angle


class IObjectDetectionListener(object, metaclass=abc.ABCMeta):
    """
    Interface for object Detection listeners
    """
    @abc.abstractmethod
    def objectDetected(self, detectedObjs: List[DetectedObject] ):
        raise NotImplementedError('users must define objectDetected to use this base class')


class PrinterObjectDetectionListener(IObjectDetectionListener):
    def objectDetected(self, detectedObjs: List[DetectedObject] ):
        for d in detectedObjs:
            print("obj: {}, {}".format(d.dist, d.angle))
