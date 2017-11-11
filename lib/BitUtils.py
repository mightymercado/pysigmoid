def twosComplement(n, bits): 
    n = (1 << bits) - n
    return n

def onesComplement(n, bits):
    return (1 << bits) - n - 1

def lastSetBit(n):
    return n.bit_length() - 1

def lastUnsetBit(n):
    return lastSetBit(onesComplement(n, n.bit_length()))

def ceilLog2(n):
    x = lastSetBit(n)
    return x+int(n!=1<<x)

def floorLog2(n):
    return (countBits(n) - 1)

def nextPowerOfTwo(n):
    return 1 << ceilLog2(n)

def setBit(n, i):
    return n | (1<<i)

def unsetBit(n, i):
    return (n | (1 << i)) ^ (1 << i)

def checkBit(n, i):
    return (n >> i) & 1 

def toggleBit(n, i):
    return n ^ (1 << i)

# creates mask of n consecutive bits, and k trailing zeroes
def createMask(n, k):
    return ((1 << n) - 1) << k

# k = end position
# n = number of bits
# x = integer
def extractBits(x, n, k):
    return (x & createMask(n, k)) >> k

def printBits(n, bits):
    b = bin(n)[2:]
    l = len(b)
    print((bits - l) * "0" + b)

def countBits(n):
    return n.bit_length()

def countTrailingZeroes(n):
    if n == 0:
        return 0
    return (n & -n).bit_length() - 1

def removeTrailingZeroes(n):
    if n == 0:
        return n
    return n >> countTrailingZeroes(n)

def align(a, b):
    a_length = countBits(a)
    b_length = countBits(b)
    if a_length > b_length:
        b <<= (a_length - b_length)
    elif a_length < b_length:
        a <<= (b_length - a_length)
    trailing_a = countTrailingZeroes(a)
    trailing_b = countTrailingZeroes(b)
    a >>= min(trailing_a, trailing_b)
    b >>= min(trailing_a, trailing_b)
    return (a, b)

def floorLog2FivePow(x):
    # works for 1 <= x <= 100
    # https://stackoverflow.com/questions/47229444/how-to-compute-floorlog25x-without-floating-point-arithmetic-or-long-integ/47229742#47229742
    log2_5 = 23219281
    scale = 10000000
    result = x * log2_5
    output = result // scale