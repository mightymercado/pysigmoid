s
from PySigmoid import Posit, set_posit_env
from math import log
from decimal import Decimal as D, getcontext
import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy 
from mpmath import mpf, mp
mp.prec = 7

# 500 digits of precision
getcontext().prec = 50
def decacc(x, y):
    if x == y:
        return D('inf')
    else:
        try:
            return -abs((x / y).log10()).log10()
        except:
            return 0

import numpy
p = Posit()
p.set_bit_pattern(p.maxpos)
p = -p
p = p.get_value()

q = Posit()
q.set_bit_pattern(q.maxpos)
q = q.get_value()

xx = []
yy = []
while p <= q:
    t = deepcopy(p)
    x = Posit(float(p)).get_value()
    y = p
    d = decacc(x, y)
    xx.append(float(p))
    yy.append(float(d))
    p += D("1")
    print(p)
 
# Plot
plt.plot(xx, yy, alpha=1)
plt.xlabel('x')
plt.ylabel('Decimal Accuracy of x when converting to Posit')
plt.show()

set_posit_env(8, 1)

p = Posit()
p.set_bit_pattern(p.maxpos)
p = -p
p = p.get_value()

q = Posit()
q.set_bit_pattern(q.maxpos),
q = q.get_value()

xx = []
yy = []
while p <= q:
    t = deepcopy(p)
    x = Posit(float(p)).get_value()
    y = p
    d = decacc(x, y)
    xx.append(float(p))
    yy.append(float(d))
    p += D("1")
    print(p)
 
# Plot
plt.plot(xx, yy, alpha=1)
plt.xlabel('x')
plt.ylabel('Decimal Accuracy of x when converting to Posit')
plt.show()