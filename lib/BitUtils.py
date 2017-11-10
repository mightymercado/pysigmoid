def twosComplement(n, bits):
    if (n & (1 << (bits - 1))) != 0: 
        n = n - (1 << bits)
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

def nextPowerOfTwo(n):
    return 1 << ceilLog2(n)

def setBit(n, i):
    return n | (1<<i)

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
    return (a, b)