from PySigmoid import *

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