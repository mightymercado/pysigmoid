from PySigmoid import Posit, set_posit_env
from math import log
from decimal import Decimal as D, getcontext
import numpy as np
import matplotlib.pyplot as plt
from math import exp
from copy import deepcopy as dc

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

set_posit_env(8, 0)

start = -100
end = 100
xx = []
yy = []
yy2 = []

def sigmoid(x):
  return 1 / (1 + exp(-x))

while start <= end:
    q = Posit(start)
    q = q.sigmoid()
    xx.append(start)
    yy.append(float(q))
    yy2.append(sigmoid(start))
    start += 0.01

# Plot

a = plt.plot(xx, yy, color = 'red', label = "Posit Flip Sign, Shift Right Two Times")
b = plt.plot(xx, yy2, color = 'blue', label = "Floating Point 1/(1 + e^-x)")
plt.legend()

plt.show()