import threading

import andabb.Robot as rb
from .PoseUpdater import GroundTruthPoseUpdater
from .RobotDummyDriver import RobotDummyDriver
from .RobotMonitor import RobotMonitor
from .Simulator import Simulator
from .plotrobot import plotRobotAndObjects
from .WallFollower import FuzzyWallFollower

def main():
    sim = Simulator()
    sim.connect()

    stopEvent = threading.Event()

    robot = rb.newPioonerRobot(sim)
    monitor = RobotMonitor(robot, GroundTruthPoseUpdater(), FuzzyWallFollower(), stopEvent, 200)
    #driver = RobotDummyDriver(robot, stopEvent)
    #monitor.subscribeToFrontObjectDetection(driver)

    monitor.start()
    #driver.start()

    plotThread = threading.Thread(target=plotRobotAndObjects, args=(monitor,))
    plotThread.start()

    try:
        while monitor.is_alive():
            monitor.join(timeout=1.0)
            #driver.join(timeout=1.0)
    except (KeyboardInterrupt, SystemExit):
        stopEvent.set()

    plotThread.join()
    sim.disconnect()


if __name__ == '__main__':
    main()
