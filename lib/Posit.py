from math import ceil, log
from fractions import Fraction
from decimal import *

class Posit:
    def __init__(self, nbits, es):
        self.number = 0
        # number of bits
        self.nbits = nbits
        # max number of exponent bits
        self.es = es
        # number of bit patterns
        self.npat = 2**nbits
        # useed
        self.useed = 2**2**es
        # minimum positive value
        self.minpos = self.useed**(-nbits+2)
        # maximum positive value
        self.maxpos = self.useed**(nbits - 2)
        # size of the quire register
        self.qsize = 2**ceil(log((nbits - 2) * 2**(es+2)+5, 2))
        # extra bits for worst-case summations that produce carry bits
        self.qextra = self.qsize - (nbits - 2) * 2**(es + 2)

    def set_bit_pattern(self, x):
        # given a strings of 0's and 1's, set the Posit to that value
        if type(x) == str:
            self.number = int(x, 2)
        else:
            self.number = x

    def is_valid(self):
        # check if a number is a valid posit of nbits
        return 0 <= self.number and self.number < npat

    def get_sign_bit(self, x):
        # extract the sign bit, returns 0 or 1
        return x >> (self.nbits - 1)

    def check_bit(self, x, i):
        # check if the xth bit is 0
        return int((x & 2**i) > 0)

    def get_regime_value(self):
        # store number in separate variable
        x = self.number
        # check sign bit
        sign = self.get_sign_bit(self.number)
        # decode two's complement if sign is 1
        if sign == 1:
            x = self.twos_complement(x)
        
        # the first bit in regime bit
        first = self.check_bit(x, self.nbits-2)
        
        # the run length of the regime bits
        length = 1
        for i in range(self.nbits-3, -1, -1):
            if first == self.check_bit(x, i): 
                length += 1
            else:
                break
        
        if first == 0:  
            return - length
        else:
            return length - 1
        
    def get_exponent_value(self):
        # store number in separate variable
        x = self.number
        # check sign bit
        sign = self.get_sign_bit(self.number)
        # decode two's complement if sign is 1
        if sign == 1:
            x = self.twos_complement(x)
        
        regime_value = self.get_regime_value()
        
        if regime_value < 0:
            regime_length = -regime_value + 1
        else:
            regime_length = regime_value + 2
        
        # start of exponent
        start = 1 + regime_length
        exponent = 0
        power = 2**(self.es - 1)
        
        # compute value of exponent
        for i in range(start, self.nbits):
            exponent += power * self.check_bit(x, self.nbits - 1 - i)
            power //= 2
        
        return exponent

    def to_signed_int(self, x):
        sign = get_sign_bit()
        if sign == 1:
            x = - twos_complement(x)
        return x

    def __gt__(self, other):
        return to_signed_int(self.number) > to_signed_int(other.number)

    def __lt__(self, other):
        return to_signed_int(self.number) < to_signed_int(other.number)

    def __eq__(self, other):
        return self.number == other.number

    def get_fraction_integer():
        # store number in separate variable
        x = self.number
        # check sign bit
        sign = self.get_sign_bit(self.number)
        # decode two's complement if sign is 1
        if sign == 1:
            x = self.twos_complement(x)
       
        # get regime_value 
        regime_value = self.get_regime_value()
        
        # use regime_value to compute regime_length
        if regime_value < 0:
            regime_length = - regime_value + 1
        else:
            regime_length = regime_value + 2

        # start of fraction
        start = nbits - 2 - regime_length - self.es
        
        return (2**self.nbits - 1)

    def get_fraction_fraction(self):
        # store number in separate variable
        x = self.number
        # check sign bit
        sign = self.get_sign_bit(self.number)
        # decode two's complement if sign is 1
        if sign == 1:
            x = self.twos_complement(x)
        
        # get regime_value 
        regime_value = self.get_regime_value()
        
        # use regime_value to compute regime_length
        if regime_value < 0:
            regime_length = -regime_value + 1
        else:
            regime_length = regime_value + 2

        # start of fraction
        start = 1 + regime_length + self.es + 1
        # initial fraction value is 1 because hidden bit is always 1
        value = Fraction(1, 1)
        power = 2
        for i in range(start, self.nbits+1):
            value += Fraction(1, power) * self.check_bit(x, self.nbits - i)
            power *= 2

        return value

    # check if a number is infinite
    def isInf(self, x):
        return x == 2**(nbits-1) - 1

    # add two posits
    def __mul__(self, other):
        fraction_a = self.get_fraction_value()
        regime_a = self.get_regime_value()
        exponent_a = self.get_exponent_value()
        fraction_b = other.get_fraction_value()
        regime_b = other.get_regime_value()
        exponent_b = other.get_fracton_value()

        # compute total scale factor
        total_power =  (2**es * (regime_a + regime_b) + exponent_a + exponent_b)
        # resulting regime value
        regime_c = total_power // 2**es
        # resulting regime 
        exponent_c = total_power % 2**es
        if regime_c < 0:
            regime_length = - regime_c + 1  
        else:
            regime_length = regime_c + 2

        
        fraction_bits = self.nbits - 1 - self.es - regime_length
        
    def __add__(self, other):
        

    # get two's complement of a number
    def twos_complement(self, x):
        return self.npat - x

n = Posit(16,3)
n.set_bit_pattern("0000110111011101")
print(n.get_fraction_value())