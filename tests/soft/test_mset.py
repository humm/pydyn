"""Test the code of MotorSet"""

import unittest
import time

import env
from pydyn.ios.fakeio import fakecom
from pydyn.dynamixel import controller
from pydyn.msets.mset import MotorSet

class TestFake(unittest.TestCase):

    def setUp(self):
        self.mcom = fakecom.FakeCom()
        self.mcom._add_motor(3,  'AX-12')
        self.mcom._add_motor(17, 'AX-12')
        self.ctrl = controller.DynamixelController(self.mcom)
        mids = self.ctrl.discover_motors(verbose=False)
        self.ctrl.load_motors(mids)
        self.ctrl.start()

    def tearDown(self):
        self.ctrl.close()

    def test_get(self):
        ms = MotorSet(motors=self.ctrl.motors)
        self.assertEqual(len(ms.position), len(self.ctrl.motors), 2)

        with self.assertRaises(AttributeError):
            ms.does_not_exist

    def test_set(self):
        ms = MotorSet(motors=self.ctrl.motors)
        ms.goal_position_bytes = 150
        time.sleep(0.05)
        self.assertEqual(ms.motors[0].goal_position_bytes, 150)
        self.assertEqual(ms.motors[1].goal_position_bytes, 150)

        ms.position_bytes = (100, 200)
        time.sleep(0.05)
        self.assertEqual(ms.motors[0].goal_position_bytes, 100)
        self.assertEqual(ms.motors[1].goal_position_bytes, 200)

        with self.assertRaises(AttributeError):
            ms.does_not_exist = 100

    def test_properties(self):
        ms = MotorSet(motors=self.ctrl.motors)
        ms.zero_pose = -150
        ms.pose = 0
        time.sleep(0.05)
        self.assertEqual(ms.pose, (0.0, 0.0))

if __name__ == '__main__':
    unittest.main()