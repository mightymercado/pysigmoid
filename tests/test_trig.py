env = [
    [8, 2],
    [8, 3],
    [8, 4],
    [16, 0],
    [16, 1],
    [16, 3],
    [16, 4],
    [32, 0],
    [32, 1],
    [32, 2],
    [32, 3]
]

import unittest
from math import *
from PySigmoid import Posit, Quire, set_posit_env, Math

class TestTrig(unittest.TestCase):
    def test_small_sin(self):   
        start = -10
        diff = 0.1
        for i in range(100):
            for e in env:
                set_posit_env(e[0], e[1])
                b = Math.sin(Posit(start))
                self.assertEqual(Posit(sin(float(Posit(start).get_value()))), b)
            start += diff

    def test_large_sin(self):   
        start = -1000
        diff = 100
        for i in range(100):
            for e in env:
                set_posit_env(e[0], e[1])
                b = Math.sin(Posit(start))
                self.assertEqual(Posit(sin(float(Posit(start).get_value()))), b)
            start += diff

    def test_small_cos(self):   
        start = -10
        diff = 0.1
        for i in range(100):
            for e in env:
                set_posit_env(e[0], e[1])
                b = Math.cos(Posit(start))
                self.assertEqual(Posit(cos(float(Posit(start).get_value()))), b)
            start += diff

    def test_large_cos(self):   
        start = -100
        diff = 10
        for i in range(100):
            for e in env:
                set_posit_env(e[0], e[1])
                b = Math.cos(Posit(start))
                self.assertEqual(Posit(cos(float(Posit(start).get_value()))), b)
            start += diff

    def test_small_tan(self):   
        start = -10
        diff = 0.1
        for i in range(100):
            for e in env:
                set_posit_env(e[0], e[1])
                b = Math.tan(Posit(start))
                self.assertEqual(Posit(tan(float(Posit(start).get_value()))), b)
            start += diff

    def test_large_tan(self):   
        start = -100
        diff = 10
        for i in range(100):
            for e in env:
                set_posit_env(e[0], e[1])
                b = Math.tan(Posit(start))
                self.assertEqual(Posit(tan(float(Posit(start).get_value()))), b)
            start += diff

    def test_asin(self):   
        start = 0
        diff = 0.00000001
        for i in range(2):
            for e in env:
                set_posit_env(e[0], e[1])
                b = Math.asin(Posit(start))
                Posit(asin(float(Posit(start).get_value())))
            start += diff

if __name__ == '__main__':
    unittest.main()