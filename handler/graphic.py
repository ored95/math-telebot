"""
Graphic handler
"""
from .approximation_help import *
from .equation import *
from .integral import *
import numpy as np
import matplotlib.pyplot as plt

class Graphic:
    @staticmethod
    def plotApp(plt, x, y, legends=['ne', 'cs', 'lsm'], minN=1, maxN=7, npt=1000):
        gpc = list()
        if 'ne' in legends:
            newton = Newton(x, y)
            px, py = newton.get_plot_points(npt)
            item = {
                'legend': newton.__str__(),
                'X': px,
                'Y': py
            }
            gpc.append(item)
        if 'cs' in legends:
            cspline = CubicSpline(x, y)
            px, py = cspline.get_plot_points(npt)
            item = {
                'legend': cspline.__str__(),
                'X': px,
                'Y': py
            }
            gpc.append(item)
        if 'lsm' in legends:
            # err = []
            for n in range(maxN, minN-1, -1):
                lsm = LSM(x, y, n)
                # err.append(lsm.mse())
                px, py = lsm.get_plot_points(npt)
                item = {
                    'legend': lsm.__str__(),
                    'X': px,
                    'Y': py
                }
                gpc.append(item)
        
        # plt.figure(figsize=(20,16))
        plt.clf()   # clear current figure of plot
        plt.title('2D-Approximation')
        plt.grid()
        plt.plot(x, y, 'go', markersize=12)
        for item in gpc:
            plt.plot(item['X'], item['Y'], label=item['legend'])
        plt.legend(loc="upper left")
        return plt#, err    

    @staticmethod
    def plotFunc(plt, f, a=1e-3, b=1e-3, npt=1000, title='Function'):
        px = np.linspace(a, b, npt)
        py = [f(x) for x in px]
        plt.clf()   # clear current figure of plot
        plt.title(title)
        plt.grid()
        plt.plot(px, py)
        return plt

# Example
# x = [1, 2, 3, 5, 6, 8]
# y = [0.1, 0.4, 0.93, 2.7, 1.8, 1.1]

# plt = Graphic.plotApp(x, y, npt=100, legends=['ne', 'cs'])
# plt.show()

# plt = Graphic.plotFunc(Equation.func('x^2-3x=2'), a=-100, b=100, title='Equation')
# plt.show()

# tmp = Integral('x^2-x+2, -1, 1')
# plt1 = Graphic.plotFunc(tmp.func, a=tmp.a, b=tmp.b, title='Integral')
# plt1.show()