from copy import *
from math import *
from fractions import Fraction
from decimal import Decimal, getcontext
from ctypes import c_ulonglong, c_double
from .BitUtils import *
from FixedPoint import *

class Posit(object):
    def __init__(self, number = 0, nbits = None, es = None):
        if nbits != None and es != None:
            self.nbits = nbits
            self.es = es
        elif type(Posit.NBITS) is not int or type(Posit.ES) is not int:
            raise Exception("Set posit envrionemnt first using set_posit_env(nbits, es)")
        else:
            self.nbits = Posit.NBITS
            self.es = Posit.ES

        self.number = 0
        # number of bit patterns
        self.npat = 2**self.nbits
        # useed
        self.useed = 2**2**self.es
        # minimum positive value (bit pattern)
        self.minpos = 1
        # maximum positive value
        self.maxpos = 2**(self.nbits - 1) - 1
        self.inf = 2**(self.nbits - 1)
        self.zero = 0

        if type(number) == Quire:
            sign = int(number.q.scaledval < 0)
            if sign == 1:
                number.q = -number.q
            scale = number.integer_bits - number.q.toBinaryString().find("1")
            if scale > 0:
                scale -= 1
            fraction = number.q.scaledval
            self.number = Posit(nbits = self.nbits, es = self.es).construct_posit(sign, scale, fraction).number
        elif type(number) == str:
            self.set_string(number)
        elif type(number) == int:
            self.set_int(number)
        else:
            self.set_float(float(number))
        
    def float_to_int(self, n):
        '''
            Input: Float
            Returns the equivalent integer bit pattern of the 64-bit float
        '''
        if type(n) == float:
            return c_ulonglong.from_buffer(c_double(n)).value
        else:
            raise "Not float"

    def set_bit_pattern(self, x):
        '''
            Input: String of 1's and 0's of length at most nbits
            Sets the number to a bit pattern
        '''
        if type(x) == str:
            if x.count("1") + x.count("0") == len(x):
                if len(x) <= self.nbits:
                    self.number = int(x, 2)
                else:
                    raise "String length exceeds number of bits"
            else:
                raise "String must contain only 1 and 0's"
        elif type(x) == int:
            if countBits(x) <= self.nbits:
                self.number = x
            else:
                raise "Integer exceeds number of bits"
        else:
            raise "Not string or int"

    def set_float(self, x):
        '''
            Input: Float
            Map float to posit
            Cases -> Action
                (1) negative or positive zero -> return zero posit
                (2) +-inf or NaN -> return posit infinity
                (3) normal float -> round to nearest representable posit
        '''
        if type(x) == float:
            # (1) negative or positive zero -> return zero posit 
            if x == 0:
                self.number = self.zero
            # (2) +-inf or NaN -> return posit infinity
            elif isinf(x) or isnan(x):
                self.number = self.inf
            # (3) normal float
            else:
                # convert to integer
                n = self.float_to_int(x)
                # to get sign bit, shift 63 times to the right
                sign = n >> 63
                # to get exponent bits, remove sign, shift, then subtract bias
                exponent = ((n & ((1 << 63) - 1)) >> 52) - 1023  
                # to get fractions bits, mask fraction bits and then OR the hidden bit
                fraction = (1 << 52) | (n & ((1 << 52) - 1))
                # given the decoded values, construct a posit
                self.number = self.construct_posit(sign, exponent, fraction).number
        else:
            raise "Not Float"

    def set_int(self, x):
        '''
            Input: Integer
            Returns nearest representable posit to the input integer
        '''
        if type(x) == int:
            if x == 0:
                self.number = 0
            else:
                sign = 0 if x >= 0 else 1
                if sign == 1:
                    x = abs(x)
                exponent = countBits(x) - 1
                fraction = x
                self.number = self.construct_posit(sign, exponent, fraction).number
        else:
            raise "Not an integer"

    def set_string(self, x):
        if type(x) == str:
            if len(x) == 0:
                return "Empty string"
            dot_index = x.find('.')
            sign = int(x[0] == "-")
            if dot_index == -1:
                self.set_int(int(x))
            elif dot_index == len(x) - 1:
                self.set_int(int(x[:-1]))
            else:
                if sign == 1:
                    x = x[1:]
                    dot_index -= 1
                # count number of fractional digits
                fdig = len(x) - 1 - dot_index
                # get fraction
                fraction = int(x[:dot_index] + x[dot_index+1:])
                exponent = countBits(fraction) - 1 - fdig
                self.number = (self.construct_posit(sign, exponent, fraction) / Posit(5**fdig, nbits = self.nbits, es = self.es)).number
        else:
            return "Not string"
        
    def is_valid(self):
        # check if a number is a valid posit of nbits
        return 0 <= self.number and self.number < self.npat

    def get_sign_bit(self, x):
        # extract the sign bit, returns 0 or 1
        return x >> (self.nbits - 1)

    def to_signed_int(self, x):
        sign = self.get_sign_bit(x)
        if sign == 1:
            if x != self.inf:
                x = - twosComplement(unsetBit(x, self.nbits-1), self.nbits)
        return x

    def __ge__(self, other):
        if type(other) != Posit:
            other = Posit(other, nbits = self.nbits, es = self.es)
        return self.to_signed_int(self.number) >= self.to_signed_int(other.number)

    def __le__(self, other):
        if type(other) != Posit:
            other = Posit(other, nbits = self.nbits, es = self.es)
        return self.to_signed_int(self.number) <= self.to_signed_int(other.number)

    def __lt__(self, other):
        if type(other) != Posit:
            other = Posit(other, nbits = self.nbits, es = self.es)
        return self.to_signed_int(self.number) < self.to_signed_int(other.number)

    def __gt__(self, other):
        if type(other) != Posit:
            other = Posit(other, nbits = self.nbits, es = self.es)
        return self.to_signed_int(self.number) > self.to_signed_int(other.number)

    def __eq__(self, other):
        if type(other) != Posit:
            other = Posit(other, nbits = self.nbits, es = self.es)
        return self.number == other.number

    def increment_posit(self):
        self.number = (self.number + 1) % (1 << self.nbits)

    # multiply two posits
    def __mul__(self, other):
        if type(other) != Posit:
            other = Posit(other, nbits = self.nbits, es = self.es)
        if self.number == 0 or self.number == self.inf:
            return self
        elif other.number == 0 or other.number == self.inf:
            return other

        sign_a, regime_a, exponent_a, fraction_a = self.decode()
        sign_b, regime_b, exponent_b, fraction_b = other.decode()
        sign_c = sign_a ^ sign_b

        # compute total scale factor
        scale_c = (2**self.es * (regime_a + regime_b) + exponent_a + exponent_b)
        fraction_c = fraction_a * fraction_b

        fa = floorLog2(fraction_a)
        fb = floorLog2(fraction_b)
        fc = floorLog2(fraction_c)

        # adjust based on carry
        scale_c += fc - fa - fb

        # construct posit then return
        return self.construct_posit(sign_c, scale_c, fraction_c)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __radd__(self, other):
        return self.__add__(other)

    def __rsub__(self, other):
        if type(other) != Posit:
            other = Posit(other, nbits = self.nbits, es = self.es)
        return other.__sub__(self)

    def __rtruediv__(self, other):
        if type(other) != Posit:
            other = Posit(other, nbits = self.nbits, es = self.es)
        return other.__truediv__(self)

    def __rpow__(self, other):
        if type(other) != Posit:
            other = Posit(other, nbits = self.nbits, es = self.es)
        return other.__pow__(self)

    def construct_posit(self, sign, scale, fraction):
        if fraction == 0:
            return Posit(nbits = self.nbits, es = self.es)
        n = 0
        # regime = floor(scale / self.es)
        regime = scale >> self.es
        # exponent = scale % 2**es 
        exponent = scale & createMask(self.es, 0)

        # number of bits written for regime
        regime_length = regime + 2 if regime >= 0 else - regime + 1

        # overflow to maxpos underflow to minpos
        if regime_length >= self.nbits + 1:
            p = Posit(nbits = self.nbits, es = self.es)
            p.set_bit_pattern(self.maxpos if regime >= 0 else self.minpos)
            if sign == 1:
                p = -p
            return p

        # encode regime
        if regime >= 0:
            n |= createMask(regime_length - 1, self.nbits - regime_length)
        elif self.nbits - 1 >= regime_length:
            n |= setBit(n, self.nbits - 1 - regime_length)

        # count number of bits available for exponent and fraction
        exponent_bits = min(self.es, self.nbits - 1 - regime_length)
        fraction_bits = self.nbits - 1 - regime_length - exponent_bits
      
        # remove trailing zeroes
        fraction = removeTrailingZeroes(fraction)
        # length of fraction bits, -1 is for hidden bit
        fraction_length = countBits(fraction) - 1
        # remove hidden bit
        fraction &= 2**(countBits(fraction)-1) - 1

        # trailing_bits = number of bits available for exponent + fraction
        trailing_bits = self.nbits - 1 - regime_length
        # exp_frac = concatenate exponent + fraction without trailing zeroes
        exp_frac = removeTrailingZeroes(exponent << (fraction_length) | fraction)
        
        # exp_frac_bits = minimum number of bits needed to represent exp_frac
        # exponent only
        if fraction_length == 0:
            exp_frac_bits = self.es - countTrailingZeroes(exponent)
        # exponent plus fraction
        else:
            exp_frac_bits = self.es + fraction_length
        
        # rounding needs to be done
        if trailing_bits < exp_frac_bits:
            # get overflow bits
            overflown = exp_frac & createMask(exp_frac_bits - trailing_bits, 0)
            # truncate trailing bits, encode to number
            n |= exp_frac >> (exp_frac_bits - trailing_bits)
            # perform round to even rounding by adding last bit to overflown bit
            # tie-breaking
            if overflown == (1 << (exp_frac_bits - trailing_bits - 1)):
                # check last bit
                if checkBit(exp_frac, exp_frac_bits - trailing_bits):
                    n += 1
            # round to next higher value
            elif overflown > (1 << (exp_frac_bits - trailing_bits - 1)):
                n += 1
            # round to next lower value
            else:
                None
        else:
            n |= exp_frac << (trailing_bits - exp_frac_bits)
            
        p = Posit(nbits = self.nbits, es = self.es)
        if sign == 0:
            p.set_bit_pattern(n)
        else:
            p.set_bit_pattern(twosComplement(n, self.nbits))

        return p

    def __sub__(self, other):
        if type(other) != Posit:
            other = Posit(other, nbits = self.nbits, es = self.es)
        return self.__add__(other.__neg__())

    def __float__(self):
        return float(self.get_value())

    def __abs__(self):
        if self.number == 0:
            return self
        elif self.number == self.inf:
            return self
        elif self.get_sign_bit(self.number):
            return self.__neg__()
        else:
            return self

    def __add__(self, other):
        if type(other) != Posit:
            other = Posit(other, nbits = self.nbits, es = self.es)
        if self.number == 0:
            return other
        elif other.number == 0:
            return self
        elif self.number == self.inf or other.number == self.inf:
            return self.inf

        sign_a, regime_a, exponent_a, fraction_a = self.decode()
        sign_b, regime_b, exponent_b, fraction_b = other.decode()
        
        # align fraction bits
        fraction_a, fraction_b = align(fraction_a, fraction_b)

        # compute total scale factor
        scale_a = 2**self.es * regime_a + exponent_a
        scale_b = 2**self.es * regime_b + exponent_b
        scale_c = max(scale_a, scale_b) 
        
        # shift fraction bits 
        if scale_a > scale_b:
            fraction_a <<= scale_a - scale_b
            estimated_length = countBits(fraction_a)
        elif scale_a <= scale_b:
            fraction_b <<= scale_b - scale_a
            estimated_length = countBits(fraction_b)

        # get fraction
        fraction_c = (-1)**sign_a * fraction_a + (-1)**sign_b * fraction_b
        sign_c = int(fraction_c < 0)
        fraction_c = abs(fraction_c)
        
        # check for carry bit
        result_length = countBits(fraction_c)
        scale_c += result_length - estimated_length
        fraction_c = removeTrailingZeroes(fraction_c)

        if fraction_c == 0:
            return Posit(nbits = self.nbits, es = self.es)
        
        # construct posit then return
        return self.construct_posit(sign_c, scale_c, fraction_c)

    def __pow__(self, other):
        if type(other) != Posit:
            other = Posit(other, nbits = self.nbits, es = self.es)
        return Posit(Quire(self)**Quire(other), nbits = self.nbits, es = self.es)

    def get_value(self):
        # 50 digits of precision
        getcontext().prec = 100
        if self.number == 0:
            return Decimal("0")
        elif self.number == self.inf:
            return Decimal("inf")

        sign, regime, exponent, fraction = self.decode() 

        f = Decimal(fraction)
        n = countBits(fraction) - 1

        return ((-1)**sign * Decimal(2)**Decimal(2**self.es * regime + exponent - n) * Decimal(f))

    def __str__(self):
        return self.get_value().__str__()

    def get_reciprocal(self):
        r = Posit(nbits = self.nbits, es = self.es)
        r.number = unsetBit(twosComplement(self.number, self.nbits), self.nbits - 1)
        return r

    def decode(self):
        # TODO: decode without twos complement
        x = self.number

        # exception values
        if x == 0:
            return (0, 0, 0, 0)
        elif x == self.inf:
            return None
        
        # determine sign and decode
        sign = checkBit(x, self.nbits - 1)
        
        if sign == 1:
            x = twosComplement(x, self.nbits)

        # decode regime length and regime sign
        regime_sign = checkBit(x, self.nbits - 2) 
        if regime_sign == 0:
            regime_length = self.nbits - lastSetBit(x) - 1
        else:
            regime_length = self.nbits - lastUnsetBit(x) - 1
        
        # determine lengths
        exponent_length = max(0, min(self.es, self.nbits - 1 - regime_length))
        fraction_length = max(0, self.nbits - 1 - regime_length - exponent_length)
        
        # determine actual values
        regime = - regime_length + 1 if regime_sign == 0 else regime_length - 2
        exponent = extractBits(x, exponent_length, fraction_length) << (self.es - exponent_length)
        
        fraction = removeTrailingZeroes(setBit(extractBits(x, fraction_length, 0), fraction_length))

        return (sign, regime, exponent, fraction)

    def __truediv__(self, other):
        if type(other) != Posit:
            other = Posit(other, nbits = self.nbits, es = self.es)
        fraction = other.decode()[3] 
        # reciprocation is accurate for powers of two
        if fraction & (fraction - 1) ==  0:
            return self * other.get_reciprocal()

        if self.number == 0 or self.number == self.inf:
            return self
        elif other.number == 0 or other.number == self.inf:
            return other

        sign_a, regime_a, exponent_a, fraction_a = self.decode()
        sign_b, regime_b, exponent_b, fraction_b = other.decode()
        sign_c = sign_a ^ sign_b

        # compute total scale factor
        scale_c =  (2**self.es * (regime_a - regime_b) + exponent_a - exponent_b)
        fraction_a, fraction_b = align(fraction_a, fraction_b)
        fraction_a <<= self.nbits * 4
        fraction_c = fraction_a // fraction_b
        fa = floorLog2(fraction_a)
        fb = floorLog2(fraction_b)
        fc = floorLog2(fraction_c)
        
        # adjust exponent
        scale_c -= fa - fb - fc
            
        # construct posit then return
        return self.construct_posit(sign_c, scale_c, fraction_c)

    def __neg__(self):
        # negate a number
        p = Posit(nbits = self.nbits, es = self.es)
        p.set_bit_pattern(twosComplement(self.number, self.nbits))
        return p

    def __trunc__(self):
        if self.number == 0 or self.number == self.inf:
            return self

        sign, regime, exponent, fraction = self.decode()
        scale =  2**self.es * regime + exponent

        if scale >= 0:  
            if scale <= countBits(fraction) - 1:
                fraction &= ~((1 << (countBits(fraction) - 1 - scale)) - 1)
        else:
            fraction = 0
            scale = 0
            
        # construct posit then return
        return self.construct_posit(sign, scale, fraction)


    def __mod__(self, other):
        if type(other) != Posit:
            other = Posit(other, nbits = self.nbits, es = self.es)
        return self - (self / other).__trunc__() * other

    def __repr__(self):
        return self.__str__()

    def __int__(self):
        return int(self.__trunc__().get_value())

    def sigmoid(self):
        other = deepcopy(self)
        other.number = toggleBit(other.number, other.nbits-1)
        other.number = other.number >> 2
        return other

from .Quire import *