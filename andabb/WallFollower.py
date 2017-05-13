from typing import List

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def createSensorAtecendent(name: str):
    sensor = ctrl.Antecedent(np.arange(0, 2.01, 0.01), name)
    sensor['very close'] = fuzz.trapmf(sensor.universe, [0, 0, 0.2, 0.3])
    sensor['close'] = fuzz.trimf(sensor.universe, [0.2, 0.3, 0.5])
    sensor['within_range'] = fuzz.trimf(sensor.universe, [0.3, 0.6, 0.9])
    sensor['far'] = fuzz.trapmf(sensor.universe, [0.8, 0.9, 2, 2])
    return sensor


def createDeltaAtecendent(name: str):
    sensor = ctrl.Antecedent(np.arange(-2.0, 2.01, 0.01), name)
    sensor['stable'] = fuzz.trimf(sensor.universe, [-0.15, 0, 0.15])
    sensor['going far'] = fuzz.trimf(sensor.universe, [-0.5, -0.3, -0.1])
    sensor['going very far'] = fuzz.trapmf(sensor.universe, [-2, -2, -0.6, -0.4])
    sensor['getting near'] = fuzz.trimf(sensor.universe, [0.1, 0.3, 0.5])
    sensor['getting very near'] = fuzz.trapmf(sensor.universe, [0.4, 0.6, 2, 2])
    return sensor


def createLinearSpeedConsequent():
    speed = ctrl.Consequent(np.arange(-0.1, 0.3, 0.01), 'linearSpeed')
    speed['back'] = fuzz.trimf(speed.universe, [-0.1, -0.03, 0])
    speed['stop'] = fuzz.trimf(speed.universe, [-0.01, 0, 0.01])
    speed['slow'] = fuzz.trimf(speed.universe, [0.03, 0.09, 0.15])
    speed['fast'] = fuzz.trimf(speed.universe, [0.19, 0.2, 0.21])
    speed.defuzzify_method = 'centroid'
    return speed


def createAngularSpeedConsequent():
    angularSpeed = ctrl.Consequent(np.arange(-0.5, 0.51, 0.01), 'angularSpeed')
    angularSpeed.automf(7, "quant",
                        ["verySharpRight", "sharpRight", "right", "straight", "left", "sharpLeft", "verySharpLeft"])
    angularSpeed.defuzzify_method = 'centroid'
    return angularSpeed


def createRules(leftFrontSensor: ctrl.Antecedent,
                rightfrontSensor: ctrl.Antecedent,
                sideSensor: ctrl.Antecedent,
                deltaSide: ctrl.Antecedent,
                linearSpeed: ctrl.Consequent,
                angularSpeed: ctrl.Consequent):
    # FIXME add option follow left or right
    rules = [

        ctrl.Rule(deltaSide['stable'] & (~sideSensor['far']), angularSpeed['straight']),
        # ctrl.Rule(deltaSide['stable'], linearSpeed['fast']),

        ctrl.Rule(deltaSide['going far'] & (~sideSensor['far']), angularSpeed['right']),
        # ctrl.Rule(deltaSide['going far'], linearSpeed['slow']),

        ctrl.Rule(deltaSide['going very far'] & (~sideSensor['far']), angularSpeed['sharpRight']),
        ctrl.Rule(deltaSide['going very far'] & (~sideSensor['far']), linearSpeed['stop']),

        ctrl.Rule(deltaSide['getting near'], angularSpeed['left']),
        # ctrl.Rule(deltaSide['getting near'], linearSpeed['slow']),

        ctrl.Rule(deltaSide['getting very near'] & (~sideSensor['far']), angularSpeed['sharpLeft']),
        ctrl.Rule(deltaSide['getting very near'] & (~sideSensor['far']), linearSpeed['stop']),

        # Front sensors far
        ctrl.Rule(leftFrontSensor['far'] | rightfrontSensor['far'], linearSpeed['fast']),
        # ctrl.Rule(leftFrontSensor['far'] | rightfrontSensor['far'], angularSpeed['straight']),


        # Front sensors within range
        ctrl.Rule(leftFrontSensor['within_range'] | rightfrontSensor['within_range'], linearSpeed['slow']),
        ctrl.Rule(leftFrontSensor['within_range'] | rightfrontSensor['within_range'], angularSpeed['left']),

        # Front sensors close
        ctrl.Rule(leftFrontSensor['close'] | rightfrontSensor['close'], linearSpeed['stop']),
        ctrl.Rule(leftFrontSensor['close'] | rightfrontSensor['close'], angularSpeed['sharpLeft']),

        # Front sensors very close
        ctrl.Rule(leftFrontSensor['very close'] | rightfrontSensor['very close'], linearSpeed['back']),
        ctrl.Rule(leftFrontSensor['very close'] | rightfrontSensor['very close'], angularSpeed['sharpLeft']),

        ctrl.Rule(sideSensor['very close'], angularSpeed['sharpLeft']),
        ctrl.Rule(sideSensor['within_range'], angularSpeed['sharpRight']),
        ctrl.Rule(sideSensor['far'], angularSpeed['verySharpRight']),
        ctrl.Rule(sideSensor['far'], linearSpeed['stop']),

    ]

    return rules


class FuzzyWallFollower:
    def __init__(self):
        self.sideSensor = createSensorAtecendent('sideSensor')
        self.leftFrontSensor = createSensorAtecendent('leftFrontSensor')
        self.rightFrontSensor = createSensorAtecendent('rightFrontSensor')
        self.deltaSide = createDeltaAtecendent('deltaSideSensor')

        self.linearCsq = createLinearSpeedConsequent()
        self.angularCsq = createAngularSpeedConsequent()

        self.rules = createRules(self.leftFrontSensor,
                                 self.rightFrontSensor,
                                 self.sideSensor,
                                 self.deltaSide,
                                 self.linearCsq, self.angularCsq)

        self.ctrl = ctrl.ControlSystem(self.rules)
        self.sys = ctrl.ControlSystemSimulation(self.ctrl)
        self.previousMeasurement = None

    def compute(self, sensorsReadings: List[float]):
        if self.previousMeasurement is None:
            delta = 0
        else:
            delta = sensorsReadings[7] - self.previousMeasurement
        self.previousMeasurement = sensorsReadings[7]

        return self.computeDelta(delta, sensorsReadings[7], sensorsReadings[3], sensorsReadings[4])

    def computeDelta(self, delta, sideSensor, leftFrontSensor, rightFrontSensor):
        print("[{}, {}, {}, {}]".format(delta, sideSensor, leftFrontSensor, rightFrontSensor))

        self.sys.input['sideSensor'] = sideSensor
        self.sys.input['deltaSideSensor'] = delta
        self.sys.input['leftFrontSensor'] = leftFrontSensor
        self.sys.input['rightFrontSensor'] = rightFrontSensor

        self.sys.compute()
        return self.sys.output['linearSpeed'], self.sys.output['angularSpeed']
