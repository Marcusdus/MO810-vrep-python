from math import pi


def diffRadians(start, end):
    """
    Given a circle the goes from [0 to pi, -pi to 0], calculates the difference between a given start and end point.
    :param start: start angle in radians
    :param end: end angle in radians
    :return: the delta between start and end
    """
    ans = end - start
    return (ans + 2 * pi) % (2 * pi)
