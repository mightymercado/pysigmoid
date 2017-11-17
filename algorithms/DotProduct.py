import sys
sys.path.append('../lib')
from Posit import *
from PositUtils import *

def dot_product(x, y, accumulator):
    if len(x) != len(y): return False
    for i in range(len(x)):
        accumulator += x[i] * y[i]
    return accumulator

from random import random as rand
xx = [rand()*rand()*100 for i in range(10000)]
yy = [rand()*rand()*1234 for i in range(10000)] 
x = list(map(lambda x: Posit(64, 3, x), xx))
y = list(map(lambda x: Posit(64, 3, x), yy))
#x = create_random_vector(10, 32, 2)
#y = create_random_vector(10, 32, 2)
z = Posit(64, 3, "0")
print(dot_product(x, y, z))
print(sum(float(xx[i]) * float(yy[i]) for i in range(len(x))))