import abc
from . import Robot


class Pose:
    def __init__(self, x=0, y=0, orientation=0):
        self.x = x
        self.y = y
        self.orientation = orientation

    def __str__(self):
        return "[{:.2f}, {:.2f}, {:.3f} rad]".format(self.x, self.y, self.orientation)


class IPoseUpdater(object, metaclass=abc.ABCMeta):
    """
    Pose Updater strategy.
    """

    @abc.abstractmethod
    def update(self, robot: Robot):
        """
        This method returns the actual object pose.  
        :return: the object pose
        """
        raise NotImplementedError('This method must be implemented')


class GroundTruthPoseUpdater(IPoseUpdater):

    def update(self, robot: Robot):
        position = robot.sim.getObjectPosition(robot.handle)
        orientation = robot.sim.getObjectOrientation(robot.handle)
        return Pose(position[0], position[1], orientation[2])
