"""
Equation solution handler
"""
from tkinter import RIGHT
from function import Function
from enum import Enum
class order(Enum):
    LEFT=-1
    RIGHT=+1

class Equation:
    def __init__(self, txt):
        # preprocessing 
        txt = txt.lower().replace('=', '-(') + ')'
        self.func = Function.extract(txt)
        self.xinit = 1e-3

    def same_sign(self, a, b):
        return (a >= 0) ^ (b < 0)

    def search_border(self, x, order=order.LEFT, sign=1):
        """
        sign: -1 means negative else 1 - positive
        """
        dx = self.xinit
        while self.same_sign(sign, self.func(x)):
            dx *= 2
            x = x + order * dx
        return x

    # def get_range(self, xstart, xend, maxRange=1e3):
    #     fs, fe = -1, 1  # by default: sign=-1 means < 0, 
    #     xs, xe = self.left_border(xstart), self.right_border(xend)
    #     if xe - xs < maxRange:
    #         self.ranges.push_back([xs, xe])
    #     return xs, xe

    def get_ranges(self, maxRange=1e6):
        self.ranges = []
        # init part
        sign = -1 if (self.func(-self.xinit) < 0) else 1
        sig0 = -sign
        xl0 = -self.xinit
        xr0 = self.search_border(self.xinit, sign)
        if xr0 - xl0 < maxRange:
            self.ranges.push_back([xl0, xr0])

        # left part
        xr = xr0
        xl = self.search_border(xr, order.LEFT, sign)
        while abs(xl) < maxRange:
            self.ranges.push_back([xl, xr])
            sign = -sign
            xr = xl
            xl = self.search_border(xr, order.LEFT, sign)

        # right part
        sign = sig0 
        xl = xl0
        xr = self.search_border(xl, order.RIGHT, sign)
        while abs(xr) < maxRange:
            self.ranges.push_back([xl, xr])
            sign = -sign
            xl = xr
            xr = self.search_border(xl, order.RIGHT, sign)
 
    def binary_search(self, maxIter=1000):
        """
        Return:
            all monotonous part of function
        """    
        for n in range(maxIter):
            pass

    def newton(self, xstart=-100, xend=100):
        pass

e = Equation("(x^2 - 1)(6x-2/x)=7x^3/(3x+2)-2")
e.disp()

func = lambda x: (x ** 2 - 1)*(6*x-2/x)-7*x**3/(3*x+2)+2
print(func(1))