"""
Equation solution handler
"""
from function import Function
from methods import *
import time

class Equation:
    @staticmethod
    def func(txt):
        # preprocessing 
        txt = txt.lower().replace('=', '-(') + ')'
        txt = txt.replace(' ', '')
        try:
            return Function.extract(txt)
        except SyntaxError:
            return None

def is_interval(f, x1, x2, eps):
    try:
        f1, f2 = f(x1), f(x2)
        if abs(f2) < eps:
            return [x2, x2]
        if abs(f1) < eps:
            return [x1, x1]
        if f1 * f2 < 0:
            return [x1, x2]
        if abs(f1 * f2) < 1e-3:
            # binary searching
            xm = (x1 + x2) / 2.
            fm = f(xm)
            while abs(x1-x2) > eps:
                if abs(abs(f1) - max(abs(fm), abs(f1), abs(f2))) < eps:
                    x1, f1 = xm, fm
                else:
                    x2, f2 = xm, fm
                xm = (x1 + x2) / 2.
                fm = f(xm)
            if abs(fm) < eps:
                return [xm, xm]
        return None
    except:
        return None

def search_intervals(f, lhs, rhs, dx=0.083, eps=1e-10):
    intervals = []
    x = lhs
    while x < rhs:
        res = is_interval(f, x, x+dx, eps)
        if res is not None:
            intervals.append(res)
            x = res[0]
        x += dx
    return intervals
        
def root(f, method, intervals, eps=1e-10):
    roots = []
    for lhs, rhs in intervals:
        if lhs == rhs:
            roots.append(lhs)
        else:
            root = method(f, lhs, rhs, f(rhs), eps)
            if root is not None:
                roots.append(root)
    return roots

# TODO
# e = Equation("t-sin(t)=1")    # periodic function
# e = Equation("exp(t)=t+1")    # OverflowError: math range error
equations = ["exp(t)=t+1"] #"7x^2-x+3 = 4x^4+1", "x^2=3x-2", "x^2=1", "x^3-3x^2=-3x+1", "2^x/x^3=x+1", "1/x=3"]
for eqn in equations:
    f = Equation.func(eqn)
    if f is not None:
        start = time.time()
        intervals = search_intervals(f, -1e3, 1e3)
        roots = root(f, binary_searching, intervals)
        print(f'\nEQN: {eqn} ({time.time() - start:.5f} sec.)')
        print(roots)
    else:
        print("Error: can not recognize that function")
