    
def binary_searching(f, lhs, rhs, frhs, eps):
    try:
        mid = (lhs + rhs) / 2.
        fmid = f(mid)
        if abs(fmid) < eps:
            return mid
        elif fmid * frhs < 0:
            return binary_searching(f, mid, rhs, frhs, eps)
        else:
            return binary_searching(f, lhs, mid, fmid, eps)
    except:
        return None
    
def section(f, lhs, rhs, frhs, eps):
    pass