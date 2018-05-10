import unittest
from math import *
from PySigmoid import Posit, Quire, set_posit_env, Math

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

class TestMath(unittest.TestCase):
    def test_log(self):   
        start = 10
        diff = 0.1
        for i in range(100):
            for e in env:
                set_posit_env(e[0], e[1])
                b = Math.log(Posit(start))
                self.assertEqual(Posit(log(float(Posit(start).get_value()))), b)
            start += diff

    def test_sqrt(self):
        start = 10
        diff = 0.1
        for i in range(100):
            for e in env:
                set_posit_env(e[0], e[1])
                b = Math.sqrt(Posit(start))
                self.assertEqual(Posit(sqrt(float(Posit(start).get_value()))), b)
            start += diff

    def test_pow(self):
        i = 10.0
        while i < 10:
            j = -10.0
            while j < 10.0:
                for e in env:
                    set_posit_env(e[0], e[1])
                    b = Posit(i) ** Posit(j)
                    self.assertEqual(Posit(float(Posit(i).get_value()) ** float(Posit(j).get_value())), b)
                j+=0.1
            i+=0.1