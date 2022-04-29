"""
Equation solution handler
"""
from function import Function
from enum import IntEnum

class Equation:
    def __init__(self, txt):
        # preprocessing 
        txt = txt.lower().replace('=', '-(') + ')'
        txt = txt.replace(' ', '')
        try:
            self.func = Function.extract(txt)
            self.eps = 1e-5
            self.xinit = 1e-3
            self.ranges = []
            self.get_ranges()
            print(self.ranges)
            
            self.roots = []
            # if abs(self.func(0)) <= self.eps:
            #     self.roots.append(0)
                
            self.binary_searching()
            
            # clean same roots
            i = 1
            while i < len(self.roots):
                if abs(self.roots[i-1] - self.roots[i]) < self.eps:
                    self.roots.remove(self.roots[i])
                else:
                    i += 1
            print(self.roots)
        except SyntaxError:
            print("Error: can not recognize that function")

    def same_sign(self, a, b):
        """
        check if 2 numbers have same signs
        """
        return (a >= 0) ^ (b < 0)

    def search_border(self, x, order=1, sign=1, maxTimes=15):
        """
        sign: -1 means negative else 1 - positive
        """
        dx = self.xinit
        time = 1
        while time <= maxTimes and self.same_sign(sign, self.func(x)):
            dx *= 2
            time += 1
            x = x + order * dx
        return x

    # def get_ranges(self, maxRange=1e3):
    #     """_summary_
    #         Extract all monotonic ranges
    #     Args:
    #         maxRange (_type_, optional): _description_. Defaults to 1e3.
    #     """
    #     def get_sign(value):
    #         """
    #         define sign of value, -1 when negative, otherwise +1
    #         """
    #         return -1 if value < 0 else 1
        
    #     # init part
        
    #     sign = get_sign(self.func(-self.xinit))
    #     xl0 = self.search_border(self.xinit, -1, sign)
    #     xr0 = self.search_border(self.xinit, +1, sign)

    #     if xr0 - xl0 < maxRange and not self.same_sign(self.func(xr0), self.func(xl0)):
    #         self.ranges.append([xl0, xr0])

    #     # left part: order=-1
    #     xr = xr0
    #     xl = self.search_border(xr, -1, sign)
    #     while abs(xl) < maxRange and not self.same_sign(self.func(xr), self.func(xl)):
    #         self.ranges.append([xl, xr])
    #         sign = -sign
    #         xr = xl
    #         xl = self.search_border(xr, -1, sign)
        
    #     # right part: order=+1
    #     sign = get_sign(self.func(xl0))
    #     xl = xl0
    #     xr = self.search_border(xl, +1, sign)
    #     while abs(xr) < maxRange and not self.same_sign(self.func(xr), self.func(xl)):
    #         self.ranges.append([xl, xr])
    #         sign = -sign
    #         xl = xr
    #         xr = self.search_border(xl, +1, sign)
    def get_ranges(self, xmin=-1e3, xmax=1e3):
        def get_sign(value):
            """
            define sign of value, -1 when negative, otherwise +1
            """
            return -1 if value < 0 else 1
        
        x, sgx = xmin, get_sign(self.func(xmin))
        dx = 0.1/3      # magic number
        while x <= xmax:
            if not self.same_sign(self.func(x), self.func(x+dx)):
                self.ranges.append([x, x+dx])
            x += dx
        
    def newton(self):
        pass
    
    def binary_searching(self, feps=1e-3):
        for xb, xe in self.ranges:
            xm = (xb + xe) / 2.
            fb, fm, fe = self.func(xb), self.func(xm), self.func(xe)
            while xe - xb > self.eps:
                if self.same_sign(fb, fm):
                    xb, fb = xm, fm
                else:
                    xe, fe = xm, fm
                xm = (xb + xe) / 2.
                fm = self.func(xm)
            if abs(fm) < feps:
                self.roots.append(xm)

# e = Equation("2^x/x^3=x+1")
# e = Equation("x^3-3x^2=-3x+1")
# e = Equation("x^2=1")
# e = Equation("x^2=3x-2")
# e = Equation("t-sin(t)=1")
# e = Equation("exp(t)=t+1")
e = Equation("7x^2-x+3 = 4x^4+1")