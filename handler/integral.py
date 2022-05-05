"""
Integral calculation handler
"""
from function import Function

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
            raise Exception('Parse arguments failed')

    @staticmethod
    def trapezoid(f, a, b, N=1000):
        dx = (b - a) / N
        s = (f(a) + f(b)) / 2.
        a += dx
        for i in range(1, N):
            s += f(a)
            a += dx
        return s * dx
    
    @staticmethod
    def simpson(f, a, b, N=1000):
        dx = (b - a) / N / 2
        fx = [f(a + i*dx) for i in range(2*N + 1)]
        s = (dx / 3) * (fx[0] + 2 * sum(fx[:-2:2]) + 4 * sum(fx[1:-1:2]) + fx[-1])
        return s
    
    @staticmethod
    def rectange(f, a, b, flag='l', N=1000):
        dx = (b - a) / N
        ranges = range(1, N+1) if flag == 'r' else range(N) 
        s = 0
        a += ranges[0] * dx
        for i in ranges:
            s += f(a)
            a += dx
        return s * dx
    
    
try:
    tmp = Integral('x^2-1, -1, 1')
    print(Integral.trapezoid(tmp.func, tmp.a, tmp.b))
    print(Integral.simpson(tmp.func, tmp.a, tmp.b))
    print(Integral.rectange(tmp.func, tmp.a, tmp.b, flag='r'))
    print(Integral.rectange(tmp.func, tmp.a, tmp.b, flag='l'))
except Exception as e:
    print(e)