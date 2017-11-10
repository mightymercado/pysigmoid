from math import ceil, log
from fractions import Fraction
from decimal import Decimal, getcontext
from ctypes import c_ulonglong, c_double
import BitUtils

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
        self.qsize = BitUtils.nextPowerOfTwo((nbits - 2) * 2**(es+2)+5)
        # extra bits for worst-case summations that produce carry bits
        self.qextra = self.qsize - (nbits - 2) * 2**(es + 2)
        self.inf = 2**(nbits - 1)
        
    def float_to_int(self, n):
        return c_ulonglong.from_buffer(c_double(n)).value

    def set_bit_pattern(self, x):
        # given a strings of 0's and 1's, set the Posit to that value
        if type(x) == str and len(x) == self.nbits:
            self.number = int(x, 2)
        elif self.nbits >= BitUtils.countBits(x):
            self.number = x

    def set_float(self, x):
        # 64-bit floating point
        if type(x) == float:
            if x == 0:
                self.number = 0
            else:
                n = self.float_to_int(x)
                sign = n >> 63
                exponent = ((n & (2**63-1)) >> 52) - 1023  # remove sign then shift
                fraction = (2**52) + (n & (2**52-1))
                self.number = self.construct_posit(sign, exponent, fraction).number
        else:
            raise "Not Float"

    def set_int(self, x):
        if type(x) == int:
            sign = 0 if x >= 0 else 1
            exponent = BitUtils.countBits(x) - 1
            fraction = x
            self.number = self.construct_posit(sign, exponent, fraction).number
        else:
            raise "Not integer"

    def set_string(self, x):
        if type(x) == str:
            dot_index = x.find('.')
            if dot_index == -1:
                self.set_int(int(x))
            else:
                # count number of fractional digits
                fdig = len(x) - 1 - dot_index
                # get fraction
                fraction = int(x[:dot_index] + x[dot_index+1:])
                exponent = BitUtils.countBits(fraction) - 1 - fdig
                five = 5**fdig
                self.number = (self.construct_posit(0, exponent, fraction) / self.construct_posit(0, five.bit_length() - 1, five)).number
        else:
            return "Not string"
        
    def is_valid(self):
        # check if a number is a valid posit of nbits
        return 0 <= self.number and self.number < self.npat

    def get_sign_bit(self, x):
        # extract the sign bit, returns 0 or 1
        return x >> (self.nbits - 1)

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

    # multiply two posits
    def __mul__(self, other):
        if self.number == 0 or self.number == self.inf:
            return self
        elif other.number == 0 or other.number == self.inf:
            return other

        sign_a, regime_a, exponent_a, fraction_a = self.decode()
        sign_b, regime_b, exponent_b, fraction_b = other.decode()

        sign_c = sign_a * sign_b

        # compute total scale factor
        scale_c =  (2**self.es * (regime_a + regime_b) + exponent_a + exponent_b)
        fraction_c = fraction_a * fraction_b
        fa = BitUtils.floorLog2(fraction_a)
        fb = BitUtils.floorLog2(fraction_b)
        fc = BitUtils.floorLog2(fraction_c)
        if fc > fa + fb:
            scale_c += 1

        # construct posit then return
        return self.construct_posit(sign_c, scale_c, fraction_c)
    
    def construct_posit(self, sign, scale, fraction):
        n = 0
        # regime = floor(scale / self.es)
        regime = scale >> self.es
        # exponent = scale % 2**es 
        exponent = scale & BitUtils.createMask(self.es, 0)

        # number of bits written for regime
        regime_length = regime + 2 if regime >= 0 else - regime + 1

        # overflow to maxpos underflow to minpos
        if regime_length >= self.nbits:
            p = Posit(self.nbits, self.es)
            p.set_bit_pattern(self.maxpos if regime >= 0 else self.minpos)
            return p

        # encode regime
        if regime >= 0:
            n |= BitUtils.createMask(regime_length - 1, self.nbits - regime_length)
        else:
            n = BitUtils.setBit(n, self.nbits - 1 - regime_length)

        # count number of bits available for exponent and fraction
        exponent_bits = min(self.es, self.nbits - 1 - regime_length)
        fraction_bits = self.nbits - 1 - regime_length - exponent_bits
      
        # remove trailing zeroes
        fraction = BitUtils.removeTrailingZeroes(fraction)
        # length of fraction bits, -1 is for hidden bit
        fraction_length = BitUtils.countBits(fraction) - 1
        
        # remove hidden bit
        fraction &= 2**(BitUtils.countBits(fraction)-1) - 1

        # trailing_bits = number of bits available for exponent + fraction
        trailing_bits = self.nbits - 1 - regime_length
        # exp_frac = concatenate exponent + fraction without trailing zeroes
        exp_frac = BitUtils.removeTrailingZeroes(exponent << (fraction_length) | fraction)
        
        # exp_frac_bits = minimum number of bits needed to represent exp_frac
        # exponent only
        if fraction_length == 0:
            exp_frac_bits = self.es - BitUtils.countTrailingZeroes(exponent)
        # exponent plus fraction
        else:
            exp_frac_bits = self.es + fraction_length
        
        # rounding needs to be done
        if trailing_bits < exp_frac_bits:
            # get overflow bits
            overflown = exp_frac & BitUtils.createMask(exp_frac_bits - trailing_bits, 0)
            # truncate trailing bits, encode to number
            n |= exp_frac >> (exp_frac_bits - trailing_bits)
            # perform round to even rounding by adding last bit to overflown bit
            # tie-breaking
            if overflown == (1 << (exp_frac_bits - trailing_bits - 1)):
                # check last bit
                if BitUtils.checkBit(exp_frac, exp_frac_bits - trailing_bits - 2):
                    n += 1
            # round to next higher value
            elif overflown > (1 << (exp_frac_bits - trailing_bits - 1)):
                n += 1
            # round to next lower value
            else:
                None
        else:
            n |= exp_frac << (trailing_bits - exp_frac_bits)
            
        p = Posit(self.nbits, self.es)
        p.set_bit_pattern(n)
        
        return p


    def __add__(self, other):
        if self.number == 0:
            return other
        elif other.number == 0:
            return self
        elif self.number == self.inf or other.number == self.inf:
            return self.inf

        sign_a, regime_a, exponet_a, fraction_a = self.decode()
        sign_b, regime_b, exponet_b, fraction_b = other.decode()

        # align fraction bits
        fraction_a, fraction_b = BitUtils.align(fraction_a, fraction_b)

        # fraction length 
        fraction_length = BitUtils.countBits(fraction_a)

        # compute total scale factor
        scale_a = 2**self.es * regime_a + exponent_a
        scale_b = 2**self.es * regime_b + exponent_b

        scale_c = max(scale_a, scale_b)
        diff = scale_a - scale_b 

        # shift fraction bits 
        if scale_a > scale_b:
            fraction_a <<= scale_b - scale_a
        elif scale_a < scale_b:
            fraction_b <<= scale_a - scale_b

        # get fraction
        fraction_c = fraction_a + fraction_b

        # check for carry bit
        if BitUtils.countBits(fraction_c) > fraction_length:
            scale_c += 1

        fraction_c = BitUtils.removeTrailingZeroes(fraction_c)
        
        # construct posit then return
        return self.construct_posit(0, scale_c, fraction_c)

    def get_value(self):
        if self.number == 0:
            return "0"
        elif self.number == self.inf:
            return "inf"

        sign, regime, exponent, fraction = self.decode() 

        f = Decimal(fraction)
        n = BitUtils.countBits(fraction) - 1

        # 500 digits of precision
        getcontext().prec = 500
        return ((-1)**sign * Decimal(2)**Decimal(2**self.es * regime + exponent - n) * Decimal(f))

    def __str__(self):
        return self.get_value().__str__()

    def get_reciprocal(self):
        r = Posit(self.nbits, self.es)
        r.number = BitUtils.unsetBit(BitUtils.twosComplement(self.number, self.nbits), self.nbits - 1)
        return r

    def decode(self):
        # TODO: decode without twos complement
        x = self.number

        # exception values
        if x == 0:
            return None
        elif x == self.inf:
            return None
        
        # determine sign and decode
        sign = BitUtils.checkBit(x, self.nbits - 1)
        
        if sign == 1:
            x = BitUtils.twosComplement(x, self.nbits)

        # decode regime length and regime sign
        regime_sign = BitUtils.checkBit(x, self.nbits - 2) 
        if regime_sign == 0:
            regime_length = self.nbits - BitUtils.lastSetBit(x) - 1
        else:
            regime_length = self.nbits - BitUtils.lastUnsetBit(x) - 1
        
        # determine lengths
        exponent_length = min(self.es, self.nbits - 1 - regime_length)
        fraction_length = self.nbits - 1 - regime_length - exponent_length
        
        # determine actual values
        regime = - regime_length + 1 if regime_sign == 0 else regime_length - 2
        exponent = BitUtils.extractBits(x, exponent_length, fraction_length) << (self.es - exponent_length)
        
        fraction = BitUtils.removeTrailingZeroes(BitUtils.setBit(BitUtils.extractBits(x, fraction_length, 0), fraction_length))

        return (sign, regime, exponent, fraction)

    def __truediv__(self, other):
        # this algorithm is not yet hardware friendly
        fraction = other.decode()[3] 
        # reciprocation is accurate for powers of two
        if fraction & (fraction - 1) ==  0:
            return self * other.get_reciprocal()

        if self.number == 0 or self.number == self.inf:
            return self
        elif other.number == 0 or other.number == self.inf:
            return self.inf

        sign_a, regime_a, exponent_a, fraction_a = self.decode()
        sign_b, regime_b, exponent_b, fraction_b = other.decode()

        sign_c = sign_a * sign_b

        # compute total scale factor
        scale_c =  (2**self.es * (regime_a - regime_b) + exponent_a - exponent_b)
        fraction_a, fraction_b = BitUtils.align(fraction_a, fraction_b)
        if fraction_a < fraction_b:
            fraction_a <<= 256
        elif fraction_a >= fraction_b:
            fraction_b <<= 256

        fraction_c = fraction_a // fraction_b
        fa = BitUtils.floorLog2(fraction_a)
        fb = BitUtils.floorLog2(fraction_b)
        fc = BitUtils.floorLog2(fraction_c)
        if fa - fb > fc:
            scale_c -= 1
            
        # construct posit then return
        return self.construct_posit(sign_c, scale_c, fraction_c)

    def __neg__(self):
        # negate a number
        p = Posit(self.nbits, self.es)
        p.set_bit_pattern(twos_complement(self.number))
        return p

    def __sqrt__(self):
        return None

from random import randint

p = Posit(64,3)

for i in range(1,1000):
    x = randint(1,100000)
    y = randint(2,100000)
    z = x / y
    px = Posit(64, 3)
    py = Posit(64, 3)
    pz = Posit(64, 3)
    px.set_int(x)
    py.set_int(y)
    pz = x / y
    print(z)
    print(pz)