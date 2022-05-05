"""
Equation solution handler
"""
from function import Function
from methods import *
from math import pi, inf
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
    
    @staticmethod
    def fType(txt, spec_funcs = ["sin", "cos", "tan"]):
        txt = txt.lower()
        for _type in spec_funcs:
            if txt.find(_type) != -1:
                return True     # periodic functions
        return False            # normal functions
                
def is_interval(f, x1, x2, eps=1e-10):
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
            if x != res[0]:
                x += dx
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
                if abs(f(root)) < 1e-5 and (len(roots) == 0 or (len(roots) != 0 and abs(root - roots[-1]) > eps)):
                    if root > 1e12: root = inf
                    if root < -1e12: root = -inf
                    roots.append(root)
    return roots



equations = open('test').readlines()

for eqn in equations:
    f = Equation.func(eqn)
    if f is not None:
        eps = 1e-18
        lhs, rhs = -1e3, 1e3
        if Equation.fType(eqn):
            lhs, rhs = -pi, pi
        
        start = time.time()
        intervals = search_intervals(f, lhs, rhs)
        print(f'\nEQN: {eqn} (intervals [{len(intervals)}]: {time.time() - start:.5f} sec.)')
        
        start = time.time()
        roots = root(f, binary_searching, intervals, eps)
        print(f'Binary searching({time.time() - start:.5f} sec.): {roots}')
        
        start = time.time()
        roots = root(f, secant, intervals, eps)
        print(f'Secant({time.time() - start:.5f} sec.): {roots}')

        start = time.time()
        roots = root(f, brentq, intervals, eps)
        print(f'Brent({time.time() - start:.5f} sec.): {roots}')
    else:
        print("Error: can not recognize that function")
