from re import X
from scipy import optimize

def binary_searching(f, lhs, rhs, frhs, eps):
    mid = (lhs + rhs) / 2.
    fmid = f(mid)
    iter = 1
    while abs(lhs - rhs) > eps and iter < 1000:
        if fmid * frhs < 0:
            lhs = mid
        else:
            rhs, frhs = mid, fmid
        iter += 1
        mid  = (lhs + rhs) / 2.
        fmid = f(mid)
    if abs(fmid) < 1e-8: 
        return mid
    return None
    
def secant(f, lhs, rhs, frhs, eps):
    flhs = f(lhs)
    iter = 1
    while abs(lhs - rhs) > eps and abs(frhs - flhs) > eps and iter < 1000:
        iter += 1
        k = (rhs - lhs) / (frhs - flhs)
        lhs = rhs - k * frhs
        rhs = lhs - k * flhs
        flhs, frhs = f(lhs), f(rhs)
    mid = (lhs + rhs) / 2.
    if abs(f(mid)) < 1e-8: 
        return (lhs + rhs) / 2.
    return None

def brentq(f, lhs, rhs, frhs, eps):
    x = optimize.brentq(f, lhs, rhs, xtol=eps)
    # if abs(f(x)) < eps:
    #     return x
    # return None
    return x