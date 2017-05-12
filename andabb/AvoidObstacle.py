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


def createLinearSpeedConsequent():
    speed = ctrl.Consequent(np.arange(-0.1, 0.3, 0.01), 'linearSpeed')
    speed['back'] = fuzz.trimf(speed.universe, [-0.1, -0.03, 0])
    speed['stop'] = fuzz.trimf(speed.universe, [-0.01, 0, 0.01])
    speed['slow'] = fuzz.trimf(speed.universe, [0.03, 0.09, 0.15])
    speed['fast'] = fuzz.trapmf(speed.universe, [0.1, 0.2, 0.3, 0.3])
    speed.defuzzify_method = 'centroid'
    return speed


def createAngularSpeedConsequent():
    angularSpeed = ctrl.Consequent(np.arange(-0.5, 0.51, 0.01), 'angularSpeed')
    angularSpeed.automf(7, "quant", ["verySharpRight", "sharpRight", "right", "straight", "left", "sharpLeft", "verySharpLeft"])
    angularSpeed.defuzzify_method = 'mom'
    return angularSpeed


def createRules(frontSensors: List[ctrl.Antecedent],
                leftSensors: List[ctrl.Antecedent],
                rightSensors: List[ctrl.Antecedent],
                linearSpeed: ctrl.Consequent,
                angularSpeed: ctrl.Consequent):
    rules = [

        # Front sensors far
        ctrl.Rule(frontSensors[0]['far'] & frontSensors[1]['far'], angularSpeed['straight']),
        ctrl.Rule(frontSensors[0]['far'] & frontSensors[1]['far'], linearSpeed['fast']),

        # Front sensors within range
        ctrl.Rule(frontSensors[0]['within_range'] | frontSensors[1]['within_range'], linearSpeed['slow']),
        ctrl.Rule(frontSensors[0]['within_range'] | frontSensors[1]['within_range'], angularSpeed['straight']),

        # Front sensors close
        ctrl.Rule(frontSensors[0]['close'] | frontSensors[1]['close'], linearSpeed['stop']),
        ctrl.Rule(frontSensors[0]['close'] | frontSensors[1]['close'], angularSpeed['left']),
        #ctrl.Rule(frontSensors[0]['close'], angularSpeed['left']),
        #ctrl.Rule(frontSensors[1]['close'], angularSpeed['right']),

        # Front sensors very close
        ctrl.Rule(frontSensors[0]['very close'] | frontSensors[1]['very close'], linearSpeed['back']),
        ctrl.Rule(frontSensors[0]['very close'] | frontSensors[1]['very close'], angularSpeed['sharpLeft']),
        # ctrl.Rule(frontSensors[0]['very close'], angularSpeed['left']),
        # ctrl.Rule(frontSensors[1]['very close'], angularSpeed['right']),
    ]
    for sensor in leftSensors:
        rules.append(ctrl.Rule(sensor['close'], angularSpeed['sharpRight']))
        rules.append(ctrl.Rule(sensor['very close'], angularSpeed['verySharpRight']))
        rules.append(ctrl.Rule(sensor['far'], angularSpeed['left']))

    for sensor in rightSensors:
        rules.append(ctrl.Rule(sensor['close'], angularSpeed['sharpLeft']))
        rules.append(ctrl.Rule(sensor['very close'], angularSpeed['verySharpLeft']))
        rules.append(ctrl.Rule(sensor['far'], angularSpeed['right']))

    return rules


class FuzzyAvoidObstacle:
    def __init__(self):
        sensors = []
        for i in range(0, 8):
            sensors.append(createSensorAtecendent('sensor' + str(i)))

        self.linearCsq = createLinearSpeedConsequent()
        self.angularCsq = createAngularSpeedConsequent()

        self.rules = createRules([sensors[3], sensors[4]],
                                 [sensors[0], sensors[1], sensors[2]],
                                 [sensors[5], sensors[6], sensors[7]],
                                 self.linearCsq, self.angularCsq)

        self.ctrl = ctrl.ControlSystem(self.rules)
        self.sys = ctrl.ControlSystemSimulation(self.ctrl)
        self.sensors = sensors

    def compute(self, sensorsReadings: List[float]):
        print(sensorsReadings)
        for i in range(0, 8):
            self.sys.input['sensor' + str(i)] = sensorsReadings[i]

        self.sys.compute()
        return self.sys.output['linearSpeed'], self.sys.output['angularSpeed']
