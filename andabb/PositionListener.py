import abc

from .PoseUpdater import Pose


class IPositionListener(object, metaclass=abc.ABCMeta):
    """
    Interface for position listeners
    """

    @abc.abstractmethod
    def newPosition(self, pose: Pose):
        raise NotImplementedError('users must define newPosition to use this base class')


class PrinterPositionListerner(IPositionListener):
    def newPosition(self, pose: Pose):
        print("pose: {}".format(pose))
