from PySigmoid import *
import PySigmoid.Math as Math
from math import *
set_posit_env(32, 2)

a = Posit(number = 25555)
b = Math.sqrt(a)
print(trunc(Posit(1.5)))
print(trunc(Posit(0.1)))
print(trunc(Posit(0.1111)))
print(trunc(Posit(0.12222)))
print(trunc(Posit(132222.2)))
print(trunc(Posit(13222.0)))
print(Posit(1230812398129831293.0222))