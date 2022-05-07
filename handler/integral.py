"""
Integral calculation handler
"""
from .function import Function
import time
class Integral:
    def __init__(self, txt):
        # preprocessing 
        txt = txt.lower().replace(' ', '')
        try:
            args = txt.split(sep=',')
            self.func = Function.extract(args[0])
            self.a = float(args[1])
            self.b = float(args[2])
        except:
            raise Exception('Bad request (integ): invalid command instruction')

    @staticmethod
    def trapezoid(f, a, b, N=1000):
        dx = (b - a) / N
        s = (f(a) + f(b)) / 2.
        a += dx
        for i in range(1, N):
            s += f(a)
            a += dx
        return s * dx, 'Trapezoid rule'
    
    @staticmethod
    def simpson(f, a, b, N=1000):
        dx = (b - a) / N / 2
        fx = [f(a + i*dx) for i in range(2*N + 1)]
        s = (dx / 3) * (fx[0] + 2 * sum(fx[:-2:2]) + 4 * sum(fx[1:-1:2]) + fx[-1])
        return s, 'Simpson rule'
    
    @staticmethod
    def lrectangle(f, a, b, N=1000):
        dx = (b - a) / N
        s = 0
        a = 0
        for _ in range(N):
            s += f(a)
            a += dx
        return s * dx, 'Left rectangle rule'

    @staticmethod
    def rrectangle(f, a, b, N=1000):
        dx = (b - a) / N
        s = 0
        a += dx
        for _ in range(1, N+1):
            s += f(a)
            a += dx
        return s * dx, 'Right rectangle rule'

def integ(f, a, b, methods=[Integral.simpson, Integral.trapezoid, Integral.lrectangle, Integral.rrectangle]):
    res = list()
    for method in methods:
        start = time.time()
        value, rule = method(f, a, b)
        runtime = time.time() - start
        item = {
            'rule': rule,
            'value': value,
            'runtime': runtime
        }
        res.append(item)
    return res

# Example
# try:
#     tmp = Integral('x^2-1, -1, 1')
#     print(Integral.trapezoid(tmp.func, tmp.a, tmp.b))
#     print(Integral.simpson(tmp.func, tmp.a, tmp.b))
#     print(Integral.lrectangle(tmp.func, tmp.a, tmp.b))
#     print(Integral.rrectangle(tmp.func, tmp.a, tmp.b))
# except Exception as e:
#     print(e)