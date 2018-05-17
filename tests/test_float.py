import unittest
from v8cffi import shortcuts
from PySigmoid import Posit, set_posit_env

shortcuts.set_up()
class TestFloat(unittest.TestCase):
    def test_small_cast(self):
        ctx = shortcuts.get_context()
        ctx.load_libs(['../PySigmoid/posit-javascript/js/decimallookupv2.js'])
        start = 1.5
        diff = 0.0001
        for i in range(10000):
            res = eval(ctx.run_script('convertDToP("{}")'.format(str(start))))  
            for j in res:
                nbits = j["ps"]
                es = j["es"]
                set_posit_env(nbits, es)
                a, b = bin(Posit(start).number)[2:], bin(int(j["posit"], 2))[2:]
                self.assertEqual(a, b)
            start += diff

    def test_large_cast(self):
        ctx = shortcuts.get_context()
        ctx.load_libs(['../PySigmoid/posit-javascript/js/decimallookupv2.js'])
        start = 1231239123.1928282
        diff = 123123.298383
        for i in range(10000):
            res = eval(ctx.run_script('convertDToP("{}")'.format(str(start))))  
            for j in res:
                nbits = j["ps"]
                es = j["es"]
                set_posit_env(nbits, es)
                a, b = bin(Posit(start).number)[2:], bin(int(j["posit"], 2))[2:]
                self.assertEqual(a, b)
            start += diff

if __name__ == '__main__':
    unittest.main()