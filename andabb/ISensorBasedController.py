import abc
from typing import List


class ISensorBasedController(object, metaclass=abc.ABCMeta):
    """
    Sensor based controller interface. 
    This class represents controllers that take sensors as inputs. 
    """

    @abc.abstractmethod
    def compute(self, sensorReadings: List[float]):
        """
        
        :param sensorReadings: list of sensor readings. 
                               Where 0 is the sensor at 90 degrees and 7 is the sensor at -90 degrees.
        :return: the linear and angular speed. 
        """
        raise NotImplementedError('This method must be implemented')
