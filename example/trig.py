from Posit import *
from Quire import *

set_posit_env(64, 3)
a = Posit(number = 25)
b = a.sqrt_newton()
print(b.sin())