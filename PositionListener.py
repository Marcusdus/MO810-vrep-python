import abc
from vrepUtil import convertEulerToDegrees

class IPositionListener(object, metaclass=abc.ABCMeta):
    """
    Interface for position listeners
    """
    @abc.abstractmethod
    def newPosition(self, coord, orientation ):
        raise NotImplementedError('users must define newPosition to use this base class')


class PrinterPositionListerner(IPositionListener):
    def newPosition(self, coord, orientation ):
        print("{0:.2f},{0:.2f}".format(coord[0], coord[1]))
        # The correct angle is in ang[0]
        print("ang: {}".format(convertEulerToDegrees(orientation)))

