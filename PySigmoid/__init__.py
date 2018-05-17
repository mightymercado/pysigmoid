from .Posit import *
from .Quire import *

def set_posit_env(nbits, es):
    Posit.NBITS = nbits
    Posit.ES = es
    Quire.NBITS = nbits
    Quire.ES = es
    