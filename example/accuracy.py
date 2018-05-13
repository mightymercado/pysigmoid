
from PySigmoid import Posit, set_posit_env
from math import log
from decimal import Decimal as D, getcontext
import numpy as np
import matplotlib.pyplot as plt

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

        
start = -D(float(np.finfo(np.float16).max))
end = D(float(np.finfo(np.float16).max))
i = 0
xx = []
yy = []
while start <= end:
    x = D(float(np.float16(start)))
    y = start
    print(x, y, decacc(x, y))
    xx.append(start)
    yy.append(decacc(x,y))
    start += D("0.1")
    i+=1
 
# Plot
plt.scatter(xx, yy, alpha=0.5)
plt.xlabel('x')
plt.ylabel('y')
plt.show()

set_posit_env(16, 2)

p = Posit()
p.set_bit_pattern(p.maxpos)
p = -p
q = Posit()
q.set_bit_pattern(p.maxpos)
start = p.get_value()
end = q.get_value()
i = 0
xx = []
yy = []
while start <= end:
    x = Posit(start.__str__())
    x = x.get_value()
    y = start
    print(x, y, decacc(x,y))
    xx.append(start)
    yy.append(decacc(x,y))
    start += D("1000000")
    i+=1
 
# Plot
plt.plot(xx, yy, alpha=0.5)
plt.xlabel('x')
plt.ylabel('y')
plt.show()