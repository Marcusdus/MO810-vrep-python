import math
from math import pi

def rotate(x, y, theta):
    '''
    Returns point (X',Y') equal to (X,Y) rotated by angle theta in radians
    '''   
    return math.cos(theta)*x + math.sin(theta)*y, -math.sin(theta)*x + math.cos(theta)*y


def convertEulerToDegrees(eulerOrientation):
    '''
    See https://github.com/originholic/dqn-vrep/blob/master/env_vrep.py
    :return Angles in degrees
    '''
    # Convert Euler angles to pitch, roll, yaw
    rollRad, pitchRad = rotate(eulerOrientation[0], eulerOrientation[1], eulerOrientation[2])
    pitchRad = -pitchRad
    yawRad   = -eulerOrientation[2]

    baseRad = [yawRad,rollRad,pitchRad]

    # The correct angle is in degreeAng[0]
    return [math.degrees(x) for x in baseRad]
    