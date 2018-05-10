from PySigmoid import Posit as P, set_posit_env
import numpy as np

set_posit_env(64, 3)

# square matrix of elements
reg = [
    [0, 2, 3, 4],
    [3, 4, 5, 6],
    [1, 3, 2, 11],
    [3, 5, 3, 4]
]

pos = [list(map(P, e)) for e in reg] # convert to posit

b = np.matrix(reg)
a = np.matrix(pos)

# addition
print(b+b)
print(a+a)
# subtraction
print(b-b)
print(a-a)
# multiplication
print(b*b)
print(a*a)
# transpose
print(np.transpose(b))
print(np.transpose(a))
# exponentiate
print(b**2)
print(a**2)