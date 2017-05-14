from typing import List

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def createSensorAtecendent(name: str):
    sensor = ctrl.Antecedent(np.arange(0, 2.01, 0.01), name)
    sensor['very close'] = fuzz.trapmf(sensor.universe, [0, 0, 0.15, 0.27])
    sensor['close'] = fuzz.trimf(sensor.universe, [0.25, 0.3, 0.35])
    sensor['almost close'] = fuzz.trimf(sensor.universe, [0.33, 0.4, 0.45])
    sensor['in range'] = fuzz.trimf(sensor.universe, [0.43, 0.55, 0.75])
    sensor['far'] = fuzz.trapmf(sensor.universe, [0.7, 0.9, 2, 2])
    return sensor


def createDeltaAtecendent(name: str):
    # not being used right now
    sensor = ctrl.Antecedent(np.arange(-2.0, 2.01, 0.001), name)
    sensor['stable'] = fuzz.trimf(sensor.universe, [-0.01, 0, 0.01])
    sensor['going far'] = fuzz.trimf(sensor.universe, [-0.5, -0.3, -0.005])
    sensor['going very far'] = fuzz.trapmf(sensor.universe, [-2, -2, -0.6, -0.4])
    sensor['getting near'] = fuzz.trimf(sensor.universe, [0.005, 0.3, 0.5])
    sensor['getting very near'] = fuzz.trapmf(sensor.universe, [0.4, 0.6, 2, 2])
    return sensor


def createLinearSpeedConsequent():
    speed = ctrl.Consequent(np.arange(-0.1, 0.3, 0.01), 'linearSpeed')
    speed['back'] = fuzz.trimf(speed.universe, [-0.1, -0.03, 0])
    speed['stop'] = fuzz.trimf(speed.universe, [-0.01, 0, 0.01])
    speed['slow'] = fuzz.trimf(speed.universe, [0.03, 0.09, 0.15])
    speed['fast'] = fuzz.trimf(speed.universe, [0.2, 0.3, 0.4])
    speed.defuzzify_method = 'centroid'
    return speed


def createAngularSpeedConsequent():
    angularSpeed = ctrl.Consequent(np.arange(-0.9, 0.91, 0.01), 'angularSpeed')
    angularSpeed['verySharpRight'] = fuzz.trapmf(angularSpeed.universe, [-0.9, -0.9, -0.5, -0.45])
    angularSpeed['sharpRight'] = fuzz.trimf(angularSpeed.universe, [-0.5, -0.35, -0.2])
    angularSpeed['right'] = fuzz.trimf(angularSpeed.universe, [-0.3, -0.1, 0.0])
    angularSpeed['straight'] = fuzz.trimf(angularSpeed.universe, [-0.1, 0.0, 0.1])
    angularSpeed['left'] = fuzz.trimf(angularSpeed.universe, [0.0, 0.1, 0.3])
    angularSpeed['sharpLeft'] = fuzz.trimf(angularSpeed.universe, [0.2, 0.35, 0.5])
    angularSpeed['verySharpLeft'] = fuzz.trapmf(angularSpeed.universe, [0.45, 0.5, 0.9, 0.9])

    angularSpeed.defuzzify_method = 'centroid'
    return angularSpeed


def createRules(rightfrontSensor: ctrl.Antecedent,
                sideSensor: ctrl.Antecedent,
                diagSensor: ctrl.Antecedent,
                linearSpeed: ctrl.Consequent,
                angularSpeed: ctrl.Consequent):
    rules = [
        ctrl.Rule(rightfrontSensor['in range'], linearSpeed['slow']),
        ctrl.Rule(rightfrontSensor['in range'], angularSpeed['straight']),

        ctrl.Rule(rightfrontSensor['close'] | rightfrontSensor['almost close'], linearSpeed['stop']),
        ctrl.Rule((rightfrontSensor['close'] | rightfrontSensor['almost close']), angularSpeed['verySharpLeft']),

        ctrl.Rule(rightfrontSensor['very close'], linearSpeed['back']),
        ctrl.Rule(rightfrontSensor['very close'],
                  angularSpeed['verySharpLeft']),

        ctrl.Rule(sideSensor['almost close'], angularSpeed['right']),
        ctrl.Rule(sideSensor['almost close'], linearSpeed['slow']),

        ctrl.Rule(sideSensor['close'], angularSpeed['straight']),
        ctrl.Rule(sideSensor['close'], linearSpeed['fast']),

        ctrl.Rule(sideSensor['very close'], angularSpeed['left']),
        ctrl.Rule(sideSensor['very close'], linearSpeed['slow']),

        ctrl.Rule(sideSensor['in range'], linearSpeed['fast']),
        ctrl.Rule(sideSensor['in range'], angularSpeed['sharpRight']),

        ctrl.Rule(sideSensor['far'] & rightfrontSensor['far'], angularSpeed['verySharpRight']),
        ctrl.Rule(sideSensor['far'] & rightfrontSensor['far'], linearSpeed['stop']),

        # Hack: this makes things more stable
        ctrl.Rule(diagSensor['in range'], angularSpeed['left']),

    ]

    return rules


class FuzzyWallFollower:
    # TODO add option follow left or right wall
    def __init__(self):
        self.sideSensor = createSensorAtecendent('sideSensor')
        self.rightFrontSensor = createSensorAtecendent('rightFrontSensor')
        self.diagSensor = createSensorAtecendent('diagSensor')

        self.linearCsq = createLinearSpeedConsequent()
        self.angularCsq = createAngularSpeedConsequent()

        self.rules = createRules(self.rightFrontSensor,
                                 self.sideSensor,
                                 self.diagSensor,
                                 self.linearCsq, self.angularCsq)

        self.ctrl = ctrl.ControlSystem(self.rules)
        self.sys = ctrl.ControlSystemSimulation(self.ctrl)
        self.previousMeasurement = None

    def compute(self, sensorsReadings: List[float]):
        return self.computeDelta(sensorsReadings[7], sensorsReadings[5], sensorsReadings[4])

    def computeDelta(self, sideSensor, diagSensor, rightFrontSensor):
        # print("[{}, {}, {}, {}, {}]".format(delta, sideSensor, diagSensor, leftFrontSensor, rightFrontSensor))

        self.sys.input['sideSensor'] = sideSensor
        self.sys.input['diagSensor'] = diagSensor
        self.sys.input['rightFrontSensor'] = rightFrontSensor

        self.sys.compute()
        return self.sys.output['linearSpeed'], self.sys.output['angularSpeed']
