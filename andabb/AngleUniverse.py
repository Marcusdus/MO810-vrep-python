from math import pi


class AngleUniverse:
    def __init__(self):
        self.limit = 2 * pi

    def calculateDelta(self, start, end, spinRightOrientation: bool):
        """
        Given a start position, an end position and the orientation of the spin, calculates the absolute delta angle.
        Note: only able to calculate delta in 360 universe. 
        :param start: the start position in radians [180, -180[
        :param end: the end position in radians [180, -180[
        :param spinRightOrientation: if the spin is turning right this should be True
        :return: the absolute delta difference
        """
        ans = abs(self.convertNegativePiUniverseTo360(end) - self.convertNegativePiUniverseTo360(start))
        if spinRightOrientation:
            return self.limit - ans
        return ans

    def addDelta(self, start, delta):
        """
        Given a start position and a delta, calculates the end position in the universe [180,-180[. 
        :param start: the start position in radians [180,-180[
        :param delta: the delta in radians
        :return: the end position in radians [180,-180[
        """
        ans = (start + delta) % self.limit
        if ans > pi:
            return ans - self.limit
        return ans

    def convertNegativePiUniverseTo360(self, angle):
        return (self.limit + angle) % self.limit
