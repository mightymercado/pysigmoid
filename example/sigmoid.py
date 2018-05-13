
from PySigmoid import Posit, set_posit_env
from math import log
from decimal import Decimal as D, getcontext
import numpy as np
import matplotlib.pyplot as plt
from math import exp
from copy import deepcopy as dc

# 500 digits of precision
getcontext().prec = 500
def decacc(x, y):
    if x == y:
        return D('inf')
    else:
        try:
            return -abs((x / y).log10()).log10()
        except:
            return 0

set_posit_env(8, 0)

start = -10
end = 10
xx = []
yy = []
yy2 = []

def sigmoid(x):
  return 1 / (1 + exp(-x))

while start <= end:
    q = Posit(start)
    q.sigmoid()
    xx.append(start)
    yy.append(float(q))
    yy2.append(sigmoid(start))
    start += 0.01

# Plot
plt.plot(xx, yy, xx, yy2, alpha = 0.5)
plt.show()