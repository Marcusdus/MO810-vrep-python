import argparse
import threading

import andabb.Robot as rb
from .PoseUpdater import GroundTruthPoseUpdater
from .RobotMonitor import RobotMonitor
from .Simulator import Simulator
from .WallFollower import FuzzyWallFollower
from .plotrobot import plotRobotAndObjects
from .plotrobot import plotRobot
from .AvoidObstacle import FuzzyAvoidObstacle
from .PoseUpdater import OdometryPoseUpdater

def parser():
    parser = argparse.ArgumentParser(description='Pioneer V-REP controller.')
    parser.add_argument('--controller', action='store',
                        choices=['avoid-obstacle', 'wall-follow'],
                        help='Controller to be used.')
    parser.add_argument('--odometry', action='store_true',
                        help='Use odometry to calculate the robot pose.')
    parser.add_argument('--plot-odometry-vs-gt', action='store_true',
                        help='Plot odometry vs ground-truth. Please also set --odometry.')
    return parser


def main():
    args = parser().parse_args()

    sim = Simulator()
    sim.connect()

    robot = rb.newPioonerRobot(sim)

    stopEvent = threading.Event()

    controller = None
    if args.controller == 'avoid-obstacle':
        controller = FuzzyAvoidObstacle()
    elif args.controller == 'wall-follow':
        controller = FuzzyWallFollower()

    poseUpdater = GroundTruthPoseUpdater()
    if args.odometry:
        poseUpdater = OdometryPoseUpdater()

    monitor = RobotMonitor(robot, poseUpdater, controller, stopEvent, 200)

    if args.plot_odometry_vs_gt:
        plotThread = threading.Thread(target=plotRobot, args=(robot,))
    else:
        plotThread = threading.Thread(target=plotRobotAndObjects, args=(monitor,))

    monitor.start()
    plotThread.start()

    try:
        while monitor.is_alive():
            monitor.join(timeout=1.0)
    except (KeyboardInterrupt, SystemExit):
        stopEvent.set()

    plotThread.join()
    sim.disconnect()


if __name__ == '__main__':
    main()
