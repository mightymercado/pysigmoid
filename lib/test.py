from Posit import *
from Quire import *
nbits = 16
es = 0
a = Posit(nbits = nbits, es = es)
b = Posit(nbits = nbits, es = es)
a.set_int(5)
b.set_int(10)
print(a)
print(b)
c = Quire(nbits, es)
c.add_posit_product(a, b)
print(c.to_posit())