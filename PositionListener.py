import abc

class IPositionListener(object, metaclass=abc.ABCMeta):
    """
    Interface for position listeners
    """
    @abc.abstractmethod
    def newPosition(self, coord ):
        raise NotImplementedError('users must define newPosition to use this base class')

class PrinterPositionListerner(IPositionListener):
    def newPosition(self, coord ):
        print("{0:.2f},{0:.2f}".format(coord[0], coord[1]))

