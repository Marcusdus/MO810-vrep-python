import logging
from math import pi
from math import degrees
from time import time

from andabb.AngleUniverse import calculateDelta
from .Simulator import Simulator

WHEELS_RAD = 0.0975


class Wheel:
    def __init__(self, sim: Simulator, name: str):
        self.sim = sim
        self.motorHandle = sim.getHandle(name)
        self.lastEncoderPosition = 0
        self.lastTimestamp = time()
        self.clockwiseSpin = False
        self.speed = 0

    def calculateSpeed(self):
        now = time()

        delta = self.getDeltaAngle()
        timeDelta = now - self.lastTimestamp
        self.lastTimestamp = now

        speed = WHEELS_RAD * (delta / timeDelta)

        if self.clockwiseSpin:
            return -speed
        return speed

    def getDeltaAngle(self):
        encoder = self.sim.getJointPosition(self.motorHandle)
        delta = calculateDelta(self.lastEncoderPosition, encoder, self.clockwiseSpin)

        self.lastEncoderPosition = encoder
        # Hack: spin orientation change
        if delta > pi:
            delta = (2 * pi) - delta
            self.clockwiseSpin = not self.clockwiseSpin

        logging.debug("Encoder {}, delta {}".format(degrees(encoder), delta))
        return delta

    def setSpeed(self, speed):
        self.speed = speed * WHEELS_RAD
        self.sim.setJointTargetVelocity(self.motorHandle, speed)

        if self.speed > 0:
            self.clockwiseSpin = False
        else:
            self.clockwiseSpin = True

    def stop(self):
        self.setSpeed(0)
