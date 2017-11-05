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
        # minimum positive value (bit pattern)
        self.minpos = 1
        # maximum positive value
        self.maxpos = 2**(nbits - 1) - 1
        # size of the quire register
        self.qsize = 2**ceil(log((nbits - 2) * 2**(es+2)+5, 2))
        # extra bits for worst-case summations that produce carry bits
        self.qextra = self.qsize - (nbits - 2) * 2**(es + 2)
        self.inf = 2**(nbits - 1)

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

    def get_fraction_int():
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
        
        # hidden bit is always 1
        value = 1
        for i in range(start, self.nbits+1):
            value = value * 2 + self.check_bit(x, self.nbits - i)

        # truncate zeroes
        while value % 2 == 0 and value > 0: 
            value /= 2 

        return value

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

    def round(self, x, bits):
        if bits == 0:
            return 0

        n = self.count_bits(x)
        print(n)
        # rounding needs to be done
        if bits < n:
            # overflown bits
            overflown = x & (2**(n-bits) - 1)
            # remove if overflown bits
            x -= overflown
            # check if round up
            if overflown > 2**(n-bits-1):
                x = x + 2**(n-bits)
        
        return x

    # multiply two posits
    def __mul__(self, other):
        # decode self
        sign_a = self.get_sign_bit()
        fraction_a = self.get_fraction_value()
        regime_a = self.get_regime_int()
        exponent_a = self.get_exponent_value()

        # decode other
        sign_b = self.get_sign_bit()
        fraction_b = other.get_fraction_int()
        regime_b = other.get_regime_value()
        exponent_b = other.get_fracton_value()

        sign_c = sign_a * sign_b

        # compute total scale factor
        total_power =  (2**es * (regime_a + regime_b) + exponent_a + exponent_b)
        # resulting regime value
        regime_c = total_power // 2**es
        # resulting regime 
        exponent_c = total_power % 2**es

        # determine regime length
        if regime_c < 0:
            regime_length = - regime_c + 1  
        else:
            regime_length = regime_c + 2

        if regime_length > nbits - 1:
            # overflow, round to maxpos
            if regime_c >= 0:
                return self.maxpos
            #underflow, round to minpos
            else:
                return self.minpos

        # count number of bits available for exponent and fraction
        exponent_bits = min(self.es, self.nbits - 1 - regime_length)
        fraction_bits = max(0, self.nbits - 1 - regime_length - self.es)
        
        # get fraction
        fraction_c = fraction_a * fraction_b
        
        # round results
        exponent_c = round(exponent_c, exponent_bits)

        # remove hidden bit
        fraction_c &= 2**(count_bits(fraction_c)-1) - 1
        fraction_c = round(fraction_c, fraction_bits)

        # truncate fraction
        while fraction_c % 2 == 0 and fraction_c > 0:
            fraction //= 2

        # construct posit then return
        return construct_post(sign_c, regime_c, exponent_c, fraction_c)
    
    def construct_posit(self, sign, regime, exponent, fraction):
        n = 0

        # encode regime
        if regime >= 0:
            regime_length = regime + 2
            n |= (2**regime_length-1) << (self.nbits-1-regime_length)
        else:
            regime_length = - regime + 1
            n |= 1 << (self.nbits-1-regime_length)
        
        # encode exponent
        exponent_bits = min(self.es, self.nbits - 1 - regime_length)
        n |= exponent << (self.nbits - 1 - regime_length - exponent_bits)
        
        # encode fraction
        n |= fraction

        p = Posit(self.nbits, self.es)
        p.set_bit_pattern(n)
        
        return p

    def print_bits(self, n):
        b = bin(n)[2:]
        l = len(b)
        print((self.nbits - l) * "0" + b)

    def count_bits(self, x):
        c = 0
        while x>0:
            x //= 2
            c += 1
        return c

    def __add__(self, other):
        return None        

    # get two's complement of a number
    def twos_complement(self, x):
        return self.npat - x

n = Posit(8,3)
print(n.construct_posit(0, -2, 2, 1))