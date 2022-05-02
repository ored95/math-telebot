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

def search_intervals(f, lhs=-1e3, rhs=1e3, dx=0.083, eps=1e-10):
    intervals = []
    x1, x2 = lhs, lhs+dx
    f1, f2 = f(x1), f(x2)
    while x2 <= rhs:
        if abs(f2) < eps:
            intervals.append([x2, x2])
            x1 = x2+dx
            f1 = f(x1)
        else:
            if abs(f1) < eps:
                intervals.append([x1, x1])    
            elif f1 * f2 < 0:
                intervals.append([x1, x2])
            x1, f1 = x2, f2
        x2 = x1+dx
        f2 = f(x2)
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
equations = ["7x^2-x+3 = 4x^4+1", "x^2=3x-2", "x^2=1", "x^3-3x^2=-3x+1", "2^x/x^3=x+1", "1/x=3"]
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
