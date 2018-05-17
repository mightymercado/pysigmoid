from PySigmoid import *
from math import *
set_posit_env(32, 2)
# float to posit
print(Posit(3.2))
# int to posit
print(Posit(31238912839))
# string to posit
print(Posit("-2.333344"))

# posit to float
print(float(Posit("3.2")))
# posit to int
print(int(Posit(31238912839)))
# posit to string
print(str(Posit("-2.333344")))

a = Posit(1)
b = Posit(2)
# Addition
print(a+b)
# Subtraction
print(a-b)
# Division
print(a/b)
# multiplication
print(a*b)
# square root
print(sqrt(a))
# power
print(a**b)

# operation with other types works too!
print(2.5 + a + 3 + b)