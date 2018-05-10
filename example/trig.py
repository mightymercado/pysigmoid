from PySigmoid import *
import PySigmoid.Math as Math
set_posit_env(32, 2)
a = Posit(number = 8)
b = Math.sin(a)
print(b)

#print(Math.pi(32, 2))