from math import degrees

from bottle import Bottle

from .PositionListener import IPositionListener
from .Robot import Pose


class RestServer(IPositionListener):
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._app = Bottle()
        self._route()
        self._lastPose = Pose()

    def _route(self):
        self._app.route('/pose', method="GET", callback=self._getPose)

    def start(self):
        self._app.run(host=self._host, port=self._port)

    def _getPose(self):
        orientation = self._lastPose.orientation
        return "{}, {}, {}, {}".format(self._lastPose.x, self._lastPose.y, orientation, degrees(orientation))

    def newPosition(self, pose: Pose):
        self._lastPose = pose
