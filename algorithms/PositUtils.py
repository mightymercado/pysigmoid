import sys
sys.path.append('../lib')
from Posit import *
from random import randint

def create_random_vector(n, nbits = 32, es = 3):
    z = []
    for i in range(n):
        a = Posit(nbits, es, randint(1,100000000))
        b = Posit(nbits, es, randint(1,100000))
        z.append(a / b)
    return z

def create_random_matrix(n, m, nbits =  32, es = 3):
    z = []
    for i in range(n):
        z.append(create_random_vector(m, nbits, es))
    return z