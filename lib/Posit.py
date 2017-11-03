from math import ceil, log

class Posit:
    def __init__(self, nbits, es):
        self.number = 0
        # number of bits
        self.nbits = nbits
        # max number of exponent bits
        self.es = es
        # number of patterns
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

    def get_sign_bit():
        # extract the sign bit, returns 0 or 1
        return self.number >> (self.nbits - 1)

    def check_bit(self, x):
        # check if the xth bit is 0
        return int((self.number & 2**x) > 0)

    def get_regime_value(self):
        # the first bit in regime bit
        first = self.check_bit(self.nbits-2)
        # the run length of the regime bits
        
        length = 1
        for i in range(self.nbits-3, -1, -1):
            if first == self.check_bit(i): 
                length += 1
        
        if first == 0:  
            return -length
        else:
            return length - 1
        
    def get_exponent_value(self):
        # get regime length
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
        while start < self.nbits:
            exponent += power * self.check_bit(self.nbits - 1 - start)
            power //= 2
            start += 1
        
        return exponent

    def get_fraction():
        # to be implemented
        return None

    def twos_complement(self):
        # to be implemented
        return None

n = Posit(5,3)
n.set_bit_pattern("0111")