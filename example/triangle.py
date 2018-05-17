#from decimal import Decimal as D, getcontext
from math import sqrt
#getcontext().prec = 40
from PySigmoid import *
D = Posit
set_posit_env(128, 4)

def area(a, b, c):
    s = (a + b + c) / D(2)
    return sqrt(s) * sqrt(s-a) * sqrt(s-b) * sqrt(s-c)

a = D(7)
b = D(7) / D(2) + D(3) * D(2)**D(-111)
c = b
k = area(a,b,c)

set_posit_env(16, 5)
print(Posit(float(k)))