from copy import *
from FixedPoint import *
class Quire(object):
    def __init__(self, number = 0, nbits = None, es = None):
        if nbits != None and es != None:
            self.nbits = nbits
            self.es = es
        elif type(number) == Posit:
            self.nbits = number.nbits
            self.es = number.es
        elif type(Quire.NBITS) is not int or type(Quire.ES) is not int:
            raise Exception("Set posit envrionemnt first using set_posit_env(nbits, es)")
        else:
            self.nbits = Quire.NBITS
            self.es = Quire.ES

        self.fraction_bits = (2 * self.nbits - 4) * 2 ** self.es + 1
        self.integer_bits = (2 * self.nbits - 4) * 2 ** self.es + 1 + 30

        if type(number) == Posit:
            self.family = FXfamily(n_bits = self.fraction_bits, n_intbits = self.integer_bits)
            if number.number == 0:
                self.q = FXnum(0, family=self.family)
            elif number.number == number.inf:
                raise Exception("Cannot convert to fixed point")

            sign, regime, exponent, fraction = number.decode() 

            f = FXnum(fraction, family=self.family)
            n = countBits(fraction) - 1

            self.q = ((-1)**sign * FXnum(2, family=self.family)**Decimal(2**self.es * regime + exponent - n) * FXnum(f, family = self.family))
        elif type(number) == int:
            self.family = FXfamily(n_bits = self.fraction_bits, n_intbits = self.integer_bits)
            self.q = FXnum(val = number, family= self.family)
        else:
            raise "Unsupported conversion to quire"
    
    # set quire to 0
    def clear(self):
        self.q = FXnum(val = 0, family = self.family)

    def add_posit_product(self, p1, p2):
        if type(p1) == Posit and type(p2) == Posit:
            self.q += Quire(p1) * Quire(p2)
        else:
            raise Exception("Arguments must be posit")

    def sub_posit_product(self, p1, p2):
        if type(p1) == Posit and type(p2) == Posit:
            self.q -= Quire(p1) * Quire(p2)
        else:
            raise Exception("Arguments must be posit")

    def set_int(self, n):
        if type(n) == int:
            self.q = FXnum(val = n, family = self.family)
        else:
            raise "Not int"

    def __add__(self, other):
        ret = deepcopy(self)
        ret.q += other.q
        return ret

    def __sub__(self, other):
        ret = deepcopy(self)
        ret.q -= other.q
        return ret

    def __mul__(self, other):
        ret = deepcopy(self)
        ret.q *= other.q
        return ret

    def __pow__(self, other):
        ret = deepcopy(self)
        ret.q = ret.q**other.q
        return ret

    def __truediv__(self, other):
        ret = deepcopy(self)
        ret.q /= other.q
        return ret

    def __str__(self):
        return self.q.__str__()

    def reduce2PI(self):
        sign = -1 if self.q.scaledval < 0 else 1
        self.q.scaledval = abs(self.q.scaledval)
        y = copy(self.q)
        t = y / (2 * self.family.pi)
        t.scaledval &= onesComplement((1 << self.fraction_bits) - 1, self.integer_bits + self.fraction_bits)
        self.q = (y - t * (2 * self.family.pi))
        self.q = sign * self.q

from .Posit import *
from .BitUtils import *
