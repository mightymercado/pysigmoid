from copy import deepcopy

# wrapped using FixedPoint arithmetic via Quire
# tan, sqrt, sin, log, intpower, exp, cos, atan, asin, acos

def sqrt(x):
    if type(x) != Posit:
        raise Exception("Argument must be posit")
    q = Quire(x)
    q.q = q.q.sqrt()
    return Posit(q)

def sin(x):
    if type(x) != Posit:
        raise Exception("Argument must be posit")
    q = Quire(x)
    q.q = q.q.sin()
    return Posit(q)

def cos(x):
    if type(x) != Posit:
        raise Exception("Argument must be posit")
    q = Quire(x)
    q.q = q.q.cos()
    return Posit(q)

def tan(x):
    if type(x) != Posit:
        raise Exception("Argument must be posit")
    q = Quire(x)
    q.q = q.q.tan()
    return Posit(q)

def asin(x):
    if type(x) != Posit:
        raise Exception("Argument must be posit")
    q = Quire(x)
    q.q = q.q.asin()
    return Posit(q)

def acos(x):
    if type(x) != Posit:
        raise Exception("Argument must be posit")
    q = Quire(x)
    q.q = q.q.acos()
    return Posit(q)

def atan(x):
    if type(x) != Posit:
        raise Exception("Argument must be posit")
    q = Quire(x)
    q.q = q.q.atan()
    return Posit(q)

def log(x):
    if type(x) != Posit:
        raise Exception("Argument must be posit")
    q = Quire(x)
    q.q = q.q.log()
    return Posit(q)

def exp(x):
    if type(x) != Posit:
        raise Exception("Argument must be posit")
    q = Quire(x)
    q.q = q.q.exp()
    return Posit(q)

def pi(nbits, es):
    # uses Bailey–Borwein–Plouffe formula
    q = Quire(0, nbits = nbits, es = es)
    q.q = q.family.pi
    return Posit(q)

def intpower(x):
    if type(x) != Posit:
        raise Exception("Argument must be posit")
    q = Quire(x)
    q.q = q.q.intpower()
    return Posit(q)

from PySigmoid import Quire, Posit
from FixedPoint import *
from copy import deepcopy