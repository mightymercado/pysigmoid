from math import ceil, log
from fractions import Fraction
from decimal import Decimal, getcontext
from ctypes import c_ulonglong, c_double

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
        
    def float_to_int(self, n):
        return c_ulonglong.from_buffer(c_double(n)).value

    def set_bit_pattern(self, x):
        # given a strings of 0's and 1's, set the Posit to that value
        if type(x) == str and len(x) == self.nbits:
            self.number = int(x, 2)
        elif self.nbits >= self.count_bits(x):
            self.number = x

    def set_float(self, x):
        if type(x) == float:
            n = self.float_to_int(x)
            sign = n >> 63
            exponent = ((n & (2**63-1)) >> 52) - 1023  # remove sign then shift
            fraction = (2**52) + (n & (2**52-1))
            self.number = self.construct_posit(sign, exponent, fraction).number

    def is_valid(self):
        # check if a number is a valid posit of nbits
        return 0 <= self.number and self.number < self.npat

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
        sign = self.get_sign_bit(self.number)
        if sign == 1:
            x = - twos_complement(x)
        return x

    def __gt__(self, other):
        return self.to_signed_int(self.number) > self.to_signed_int(other.number)

    def __lt__(self, other):
        return self.to_signed_int(self.number) < self.to_signed_int(other.number)

    def __eq__(self, other):
        return self.number == other.number

    def get_fraction_int(self):
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
        start = 2 + regime_length + self.es
        
        # hidden bit is always 1
        value = 1
        for i in range(start, self.nbits+1):
            value = value * 2 + self.check_bit(x, self.nbits - i)

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
        start = 2 + regime_length + self.es
        # initial fraction value is 1 because hidden bit is always 1
        value = Fraction(1, 1)
        power = 2
        for i in range(start, self.nbits+1):
            value += Fraction(1, power) * self.check_bit(x, self.nbits - i)
            power *= 2

        return value

    def round(self, x, bits):
        # impelementation of round to nearest even
        if bits == 0:
            return 0

        n = self.count_bits(x)
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
        sign_a = self.get_sign_bit(self.number)
        fraction_a = self.get_fraction_int()
        regime_a = self.get_regime_value()
        exponent_a = self.get_exponent_value()

        # decode other
        sign_b = self.get_sign_bit(self.number)
        fraction_b = other.get_fraction_int()
        regime_b = other.get_regime_value()
        exponent_b = other.get_exponent_value()

        sign_c = sign_a * sign_b

        # compute total scale factor
        scale_c =  (2**self.es * (regime_a + regime_b) + exponent_a + exponent_b)

        # construct posit then return
        return self.construct_posit(sign_c, scale_c, fraction_c)
    
    def construct_posit(self, sign, scale, fraction):
        n = 0

        # resulting regime value
        regime = scale // 2**self.es
        # resulting regime 
        exponent = scale - regime * 2**self.es

        # encode regime
        if regime >= 0:
            regime_length = regime + 2
        else:
            regime_length = - regime + 1

        # overflow to maxpos underflow to minpos
        if regime_length >= self.nbits:
            p = Posit(self.nbits, self.es)
            if regime >= 0:
                p.set_bit_pattern(self.maxpos)
            else:
                p.set_bit_pattern(self.minpos)
            return p

        if regime >= 0:
            n |= (2**(regime_length-1)-1) << (self.nbits-regime_length)
        else:
            n |= 1 << (self.nbits-1-regime_length)

        # count number of bits available for exponent and fraction
        exponent_bits = min(self.es, self.nbits - 1 - regime_length)
        fraction_bits = max(0, self.nbits - 1 - regime_length - self.es)
        
        # round results
        exponent = self.round(exponent, exponent_bits)

        # round, +1 is for hidden bit
        fraction = self.round(fraction, fraction_bits+1)

        # truncate fraction after rounding
        while fraction % 2 == 0 and fraction > 0:
            fraction //= 2

        # length of fraction bits, -1 is for hidden bit
        fraction_length = self.count_bits(fraction) - 1
        # remove hidden bit
        fraction &= 2**(self.count_bits(fraction)-1) - 1
        
        
        
        # encode exponent
        exponent_bits = min(self.es, self.nbits - 1 - regime_length)
        n |= exponent << (self.nbits - 1 - regime_length - exponent_bits)
        self.print_bits(n)
        # encode fraction
        n |= fraction << (self.nbits - 1 - regime_length - exponent_bits - fraction_length)
        p = Posit(self.nbits, self.es)
        p.set_bit_pattern(n)
        self.print_bits(n)

        return p

    def print_bits(self, n):
        b = bin(n)[2:]
        l = len(b)
        print((self.nbits - l) * "0" + b)

    def count_bits(self, x):
        if x == 0:
            return 1
        c = 0
        while x > 0:
            x //= 2
            c += 1
        return c

    def __add__(self, other):
        # TODO: negative numbers

        # decode self
        sign_a = self.get_sign_bit(self.number)
        fraction_a = self.get_fraction_int()
        regime_a = self.get_regime_value()
        exponent_a = self.get_exponent_value()

        # decode other
        sign_b = self.get_sign_bit(self.number)
        fraction_b = other.get_fraction_int()
        regime_b = other.get_regime_value()
        exponent_b = other.get_exponent_value()

        while fraction_a % 2 == 0 and fraction_b % 2 == 0 and fraction_b > 0 and fraction_a > 0:
            fraction_a //= 2
            fraction_b //= 2

        # compute total scale factor
        scale_a = 2**self.es * regime_a + exponent_a
        scale_b = 2**self.es * regime_b + exponent_b
        scale_c = min(scale_a, scale_b) + 1
        diff = scale_a - scale_b
        if diff >= 0:
            fraction_b *= 2**abs(diff)
        else:
            fraction_a *= 2**abs(diff)
        
        # get fraction
        fraction_c = fraction_a + fraction_b
        
        # construct posit then return
        return self.construct_posit(0, scale_c, fraction_c)

    # get two's complement of a number
    def twos_complement(self, x):
        return self.npat - x

    def __str__(self):
        sign = self.get_sign_bit(self.number)
        exponent = self.get_exponent_value()
        regime = self.get_regime_value()
        fraction = self.get_fraction_fraction()
        
        k = 0
        # remove powers of two in denominator
        w = fraction.denominator
        while w > 0 and w % 2 == 0:
            w //= 2
            k += 1
        # remove powers of two in numerator
        w = fraction.numerator
        while w > 0 and w % 2 == 0:
            w //= 2
            k -= 1
            
        # 100 digits of precision
        getcontext().prec = 100
        return ((-1)**sign * Decimal(2)**Decimal(2**self.es*regime+exponent-k) * Decimal(w)).__str__()

    def get_reciprocal(self):
        r = Posit(self.nbits, self.es)
        r.number = self.twos_complement(n.number) ^ 2**(self.nbits - 1)
        return r

    def __truediv__(self, other):
        return self * other.get_reciprocal()

    def __neg__(self):
        # negate a number
        p = Posit(self.nbits, self.es)
        p.set_bit_pattern(twos_complement(self.number))
        return p

n = Posit(16,3)
n.set_float(2.5234)
print(n)
# m = Posit(16,3)