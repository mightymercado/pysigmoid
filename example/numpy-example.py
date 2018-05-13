from PySigmoid import Posit as P, set_posit_env
import numpy as np
set_posit_env(64, 3)

# input matrix
reg = [
    [0, 2, 3, 4],
    [3, 4, 5, 6],
    [1, 3, 2, 11],
    [3, 5, 3, 4]
]

# functiont to cast a regular matrix to a posit matrix
posify = lambda x: [list(map(P, e)) for e in x]
pos = posify(reg) # convert to posit

b = np.matrix(pos)
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
# dot product
print(a.dot(b))