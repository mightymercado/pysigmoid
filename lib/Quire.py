from FixedPoint import *
from Posit import Posit
class Quire(object):
    def __init__(self, nbits, es):
        self.nbits = nbits
        self.es = es
        self.fraction_bits = (4 * self.nbits - 8) * 2 ** self.es + 1 + 30
        self.integer_bits = (2 * self.nbits - 4) + 1
        self.family = FXfamily(n_bits = self.fraction_bits, n_intbits = self.integer_bits)
        self.q = FXnum(value = 0, family = self.family)
    
    # set quire to 0
    def clear(self):
        self.q = FXnum(value = 0, family = self.family)

    def add_posit_product(self, p1, p2):
        if type(p1) == Posit and type(p2) == Posit:
            a = p1.get_fixed_point_binary()
            b = p2.get_fixed_point_binary()
            self.q += a*b
        else:
            raise Exception("Arguments must be posit")

    def sub_posit_product(self, p1, p2):
        if type(p1) == Posit and type(p2) == Posit:
            a = p1.get_fixed_point_binary()
            b = p2.get_fixed_point_binary()
            self.q -= a*b
        else:
            raise Exception("Arguments must be posit")

    def to_posit(self):
        sign = int(self.q.scaledval < 0)
        scale = self.integer_bits - self.q.toBinaryString().find("1") - 1
        fraction = self.q.scaledval
        return Posit(nbits = self.nbits, es = self.es).construct_posit(sign, scale, fraction)
        
    def __add__(self, q):
        self.q = self.q + q

    def __subtract(self, q):
        self.q = self.q - q