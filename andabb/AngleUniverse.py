from math import acos
from math import cos
from math import isclose
from math import pi
from math import sin

import numpy as np
from numpy import dot
from numpy import linalg

from scipy.optimize import lsq_linear

limit = 2 * pi


def calculateDelta(start, end, spinRightOrientation: bool = True):
    """
    Given a start position, an end position and the orientation of the spin, calculates the absolute delta angle.
    Note: only able to calculate delta in 360 universe. 
    :param start: the start position in radians [180, -180[
    :param end: the end position in radians [180, -180[
    :param spinRightOrientation: if the spin is turning right this should be True
    :return: the absolute delta difference
    """
    if isclose(end, start, abs_tol=0.00001):
        return 0

    end = convertNegativePiUniverseTo360(end)
    start = convertNegativePiUniverseTo360(start)

    ans = abs(end - start)
    if spinRightOrientation:
        if start < end:
            return limit - ans
        return ans
    if start > end:
        return limit - ans
    return ans


def addDelta(start, delta):
    """
    Given a start position and a delta, calculates the end position in the universe [180,-180[. 
    :param start: the start position in radians [180,-180[
    :param delta: the delta in radians
    :return: the end position in radians [180,-180[
    """
    ans = (start + delta) % limit
    if ans > pi:
        return ans - limit
    return ans

def addAngles(alpha, beta):
    a = to360Universe(alpha)
    b = to360Universe(beta)
    c = a + b
    return to180Universe(c)

def subAngles(alpha, beta):
    a = to360Universe(alpha)
    b = to360Universe(beta)
    c = a - b
    return to180Universe(c)

def to180Universe(alpha):
    alpha = alpha % (2 * pi)
    if alpha > pi:
        return alpha - (2 * pi)
    return alpha

def to360Universe(alpha):
    if alpha < 0:
        return (2 * pi) + alpha
    return alpha

def convertNegativePiUniverseTo360(angle):
    return (limit + angle) % limit


def calculateFirstAngleFromTriangle(a, b, c):
    '''
    Calculates A angle given the triangle sides.
    :param a: the length of the opposite side of angle A
    :param b: the length of adjacent side to A
    :param c: the length of adjacent side to A
    :return: the angle in radians
    '''
    cosineVal = ((b ** 2) + (c ** 2) - (a ** 2)) / (2 * b * c)
    if cosineVal > 1 or cosineVal < -1:
        raise NoTriangleException()
    return acos(cosineVal)


class NoTriangleException(ValueError):
    pass


def translateMatrix(dx, dy):
    return [[1, 0, dx], [0, 1, dy], [0, 0, 1]]


def rotateMatrix(alpha):
    return [[cos(alpha), -sin(alpha), 0], [sin(alpha), cos(alpha), 0], [0, 0, 1]]


def rotate(orignalP, alpha):
    r = rotateMatrix(alpha)
    return dot(r, orignalP)


def translate(originalP, dx, dy):
    t = translateMatrix(dx, dy)
    return dot(t, originalP)


def rotateAndTranslate(originalP, dx, dy, alpha):
    b1 = rotate(originalP, alpha)
    return translate(b1, dx, dy)


def translateAndRotate(originalP, dx, dy, alpha):
    b1 = translate(originalP, dx, dy)
    return rotate(b1, alpha)


def calculatePoint(a, b, c, da, db, dc):
    # np.array([(1, -1, 2), (0, 1, -1), (0, 0, 1)])
    m = np.array([
        (2 * (b[0] - a[0]), 2 * (b[1] - a[1])),
        (2 * (c[0] - a[0]), 2 * (c[1] - a[1]))
    ])
    #print(m)
    return linalg.solve(m, np.array(
        [-(((a[0] ** 2) - (b[0] ** 2)) + ((a[1] ** 2) - (b[1] ** 2)) - ((da ** 2) - (db ** 2))),
         -(((a[0] ** 2) - (c[0] ** 2)) + ((a[1] ** 2) - (c[1] ** 2)) - ((da ** 2) - (dc ** 2)))]))
    # return lsq_linear(m, np.array(
    #     [-(((a[0] ** 2) - (b[0] ** 2)) + ((a[1] ** 2) - (b[1] ** 2)) - ((da ** 2) - (db ** 2))),
    #      -(((a[0] ** 2) - (c[0] ** 2)) + ((a[1] ** 2) - (c[1] ** 2)) - ((da ** 2) - (dc ** 2)))])).x
