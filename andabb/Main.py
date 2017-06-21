import argparse
import logging
import threading

import andabb.Robot as rb
from .AvoidObstacle import FuzzyAvoidObstacle
from .PoseUpdater import GroundTruthPoseUpdater
from .PoseUpdater import KalmanFilterPoseUpdater
from .PoseUpdater import OdometryPoseUpdater
from .RestServer import RestServer
from .RobotMonitor import RobotMonitor
from .Simulator import Simulator
from .WallFollower import FuzzyWallFollower
from .plotrobot import plotRobot
from .plotrobot import plotRobotAndObjects


def parser():
    parser = argparse.ArgumentParser(description='Pioneer V-REP controller.')
    parser.add_argument('--controller', action='store',
                        choices=['avoid-obstacle', 'wall-follow'],
                        help='Controller to be used.')
    parser.add_argument('--odometry', action='store_true',
                        help='Use odometry to calculate the robot pose.')
    parser.add_argument('--kalman', action='store_true',
                        help='Use Kalman filter to calculate the robot pose.')
    parser.add_argument('--plot-odometry-vs-gt', action='store_true',
                        help='Plot odometry vs ground-truth. Please also set --odometry.')
    parser.add_argument('-p', '--port', type=int, help='V-REP remote API port.', default=25000)
    parser.add_argument('-v', '--verbose', help='increase output verbosity',
                        action='store_true')
    return parser


def main():
    args = parser().parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, format='%(message)s')
    else:
        logging.basicConfig(level=logging.WARN)

    server = RestServer(host='localhost', port=8090)

    sim = Simulator(port=args.port)
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
    if args.kalman:
        poseUpdater = KalmanFilterPoseUpdater(OdometryPoseUpdater())

    monitor = RobotMonitor(robot, poseUpdater, controller, stopEvent, 200)
    if args.kalman:
        monitor.subscribeBaseDetection(poseUpdater)

    monitor.subscribeChangePosition(server)

    if args.plot_odometry_vs_gt:
        plotThread = threading.Thread(target=plotRobot, args=(robot,))
    else:
        plotThread = threading.Thread(target=plotRobotAndObjects, args=(monitor,))

    monitor.start()
    plotThread.start()
    server.start()

    try:
        while monitor.is_alive():
            monitor.join(timeout=1.0)
    except (KeyboardInterrupt, SystemExit):
        stopEvent.set()

    plotThread.join()
    sim.disconnect()


if __name__ == '__main__':
    main()
