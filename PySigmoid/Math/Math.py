from copy import deepcopy

def sqrt(x, algo = "newton"):
    if type(x) != Posit:
        raise Exception("Argument must be posit")
    if algo == "newton":
        t = deepcopy(x)
        two = Posit(nbits = x.nbits, es = x.es, number = 2)
        while True:
            nt = (x / t + t) / two
            if t == nt:
                break
            t = nt
        return t
    elif algo == "bisection":
        low = 0
        high = x.maxpos
        # convergence at log(number_of_bit_patterns) = nbits
        for i in range(x.nbits):
            m = (low + high) // 2
            p = Posit(nbits = x.nbits, es = x.es)
            p.set_bit_pattern(m)
            r = p * p
            if r == x:
                return p
            elif r < x:
                low = m
            else:
                high = m
        return p
    else:
        raise Exception("Invalid algo parameter")
    return None

def sin(x, algo = "taylor"):
    if type(x) != Posit:
        raise Exception("Argument must be posit")
    total = Quire(0, x.nbits, x.es)
    mul = Quire(x)
    y = Quire(x)
    sign = -1
    i = 1
    iters = 0
    eps = Posit(str(x.minpos)).get_value()
    while mul.q > eps:
        iters += 1
        if iters > 1000:
            break
        sign *= -1
        total += mul * Quire(sign, x.nbits, x.es)
        print(mul)
        mul = mul * (y * y / Quire(2 * i, x.nbits, x.es) / Quire(2 * i + 1, x.nbits, x.es))
        i += 1
    return Posit(total) # round

def cos(x, algo = "taylor"):
    return None

def tan(x, algo = "taylor"):
    return None

def csc(x, algo = "taylor"):
    return None

from PySigmoid import Posit, Quire