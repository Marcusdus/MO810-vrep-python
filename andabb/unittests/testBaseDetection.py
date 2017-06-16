import unittest
from math import radians
from math import degrees

from andabb.BaseDetectionListener import mdetectBase
from andabb.Robot import Pose


class BaseDectition(unittest.TestCase):
    def test0degrees(self):
        print("0 degrees")
        print("------ x neg")
        base = mdetectBase(2.8216536045074463, 2.82124924659729, 3.0575215816497803)
        print("angle: {}".format(degrees(base.angle)))
        print(base.distance)
        print(base.getAbsolutePosition(Pose(-3, 0, radians(0))))
        print("-------- x pos")
        base = mdetectBase(2.909715414047241, 2.909170627593994, 2.8032491207122803)
        print("angle: {}".format(degrees(base.angle)))
        print(base.distance)
        print(base.getAbsolutePosition(Pose(3, 0, radians(0))))
        # print("-------- y neg")
        # base = mdetectBase(2.769779682159424, 3.10078763961792, 2.95050311088562)
        # print("angle: {}".format(degrees(base.angle)))
        # print(base.distance)
        # print(base.getAbsolutePosition(Pose(0, -3, radians(0))))
        # print("-------- y pos")
        # base = mdetectBase(2.1001908779144287, 1.7691807746887207, 1.9502599239349365)
        # print("angle: {}".format(degrees(base.angle)))
        # print(base.distance)
        # print(base.getAbsolutePosition(Pose(0, 2, radians(0))))
        print("-------- 2; 4")
        base = mdetectBase(4.52399206161499, 4.226256370544434, 4.341597080230713)
        print("angle: {}".format(degrees(base.angle)))
        print(base.distance)
        print(base.getAbsolutePosition(Pose(2, 4, radians(0))))
        #1.0913840532302856, 0.949657142162323, 0.9203619360923767

    def test4q0d(self):
        print("-------- -0.5; 1")
        base = mdetectBase(1.148566722869873, 0.8365228176116943, 1.1035438776016235)
        print("angle: {}".format(degrees(base.angle)))
        print(base.distance)
        print(base.getAbsolutePosition(Pose(-0.5, 1, radians(0))))
        print("-------- -5; 1")
        base = mdetectBase(4.9440131187438965, 4.8806891441345215, 5.145285129547119)
        print("angle: {}".format(degrees(base.angle)))
        print(base.distance)
        b = base.getAbsolutePosition(Pose(-5, 1, radians(0)))
        self.assertAlmostEqual(b[0], 0, delta=0.9)
        self.assertAlmostEqual(b[1], 0, delta=0.9)
        print(b)

    def test3q0d(self):
        print("-------- -5; -4")
        base = mdetectBase(6.120367527008057, 6.3297505378723145, 6.417346000671387)
        print("angle: {}".format(degrees(base.angle)))
        print(base.distance)
        b = base.getAbsolutePosition(Pose(-5, -4, radians(0)))
        self.assertAlmostEqual(b[0], 0, delta=0.9)
        self.assertAlmostEqual(b[1], 0, delta=0.9)
        print(b)


    def test2q0d(self):
        print("-------- 3; -2")
        base = mdetectBase(3.408524513244629, 3.591799020767212, 3.4178686141967773)
        print("angle: {}".format(degrees(base.angle)))
        print(base.distance)
        b = base.getAbsolutePosition(Pose(3, -2, radians(0)))
        self.assertAlmostEqual(b[0], 0, delta=0.9)
        self.assertAlmostEqual(b[1], 0, delta=0.9)
        print(b)

    def test1q0d(self):
        print("-------- 2; 4")
        base = mdetectBase(4.5238800048828125, 4.226135730743408, 4.341493129730225)
        print("angle: {}".format(degrees(base.angle)))
        print(base.distance)
        b=base.getAbsolutePosition(Pose(2, 4, radians(0)))
        self.assertAlmostEqual(b[0], 0, delta=0.9)
        self.assertAlmostEqual(b[1], 0, delta=0.9)
        print(b)

    def test1q270d(self):
        print("-------- 2; 4")
        base = mdetectBase(4.3587727546691895, 4.209290027618408, 4.500675678253174)
        print("angle: {}".format(degrees(base.angle)))
        print(base.distance)
        print(base.getAbsolutePosition(Pose(2, 4, radians(-90))))


    def testSimple(self):
        base = mdetectBase(2.5872, 2.6025, 2.4)
        print("angle: {}".format(degrees(base.angle)))
        print(base.distance)
        print(base.getAbsolutePosition(Pose(-2.77, -0.19, radians(0.212))))
        print("---------")
        base = mdetectBase(3.0938, 3.1065, 2.9)
        print("angle: {}".format(degrees(base.angle)))
        print(base.distance)
        print(base.getAbsolutePosition(Pose(-3.2743e+00,-1.9018e-01, radians(+2.1712e-01))))
        print("---------")
        base = mdetectBase(0.76, 0.81, 0.8)
        print("angle: {}".format(degrees(base.angle)))
        print(base.distance)
        print(base.getAbsolutePosition(Pose(8.5595e-01,-1.7715e-01, radians(9.9883e-02))))
        print("---------")
        base = mdetectBase(4.21, 4.11, 4.15)
        print("angle: {}".format(degrees(base.angle)))
        print(base.distance)
        print(base.getAbsolutePosition(Pose(3.9878e+00, -1.1479e+00, radians(-1.1524e+02))))
        print("---------")
        base = mdetectBase(4.347, 4.287, 4.029)
        print("angle: {}".format(degrees(base.angle)))
        print(base.distance)
        print(base.getAbsolutePosition(Pose(4.2576e+00, -5.7513e-01, radians(-1.1512e+02))))
        print("--------- -90 degrees")
        base = mdetectBase(3.100490093231201, 2.7694857120513916, 2.9502198696136475)
        print("angle: {}".format(degrees(base.angle)))
        print(base.distance)
        print(base.getAbsolutePosition(Pose(3, 0, radians(-90))))
        print("--------- -180 degrees")
        base = mdetectBase(2.8216991424560547, 2.8214941024780273, 3.057680130004883)
        print("angle: {}".format(degrees(base.angle)))
        print(base.distance)
        print(base.getAbsolutePosition(Pose(3, 0, radians(-180))))
        print("--------- 0 degrees")
        base = mdetectBase(2.909715414047241, 2.909170627593994, 2.8032491207122803)
        print("angle: {}".format(degrees(base.angle)))
        print(base.distance)
        print(base.getAbsolutePosition(Pose(3, 0, radians(0))))
        print("--------- 90 degrees")
        base = mdetectBase(2.769486904144287, 3.1004951000213623, 2.9502170085906982)
        print("angle: {}".format(degrees(base.angle)))
        print(base.distance)
        print(base.getAbsolutePosition(Pose(3, 0, radians(90))))

        #6.357882022857666, 6.026913166046143, 6.172853946685791
        #6.349362850189209, 6.0195441246032715, 6.207071304321289
        base = mdetectBase(6.349362850189209, 6.0195441246032715, 6.207071304321289)
        print("angle: {}".format(degrees(base.angle)))
        print(base.distance)
        print(base.getAbsolutePosition(Pose(-6.26, 0.18, radians(82.752))))