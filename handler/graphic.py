"""
Graphic handler
"""
from approximation_help import *
import numpy as np
import matplotlib.pyplot as plt
class Graphic:
    @staticmethod
    def plot(x, y, legends=['Newton', 'CubicSpline', 'LSM'], npt=1000):
        gpc = list()
        if 'Newton' in legends:
            newton = Newton(x, y)
            px, py = newton.get_plot_points(npt)
            item = {
                'legend': 'Newton',
                'X': px,
                'Y': py
            }
            gpc.append(item)
        if 'CubicSpline' in legends:
            cspline = CubicSpline(x, y)
            px, py = cspline.get_plot_points(npt)
            item = {
                'legend': 'Cubic Spline',
                'X': px,
                'Y': py
            }
            gpc.append(item)
        if 'LSM' in legends:
            # err = []
            for n in range(7, 0, -1):
                lsm = LSM(x, y, n)
                # err.append(lsm.mse())
                px, py = lsm.get_plot_points(npt)
                item = {
                    'legend': f'LSM (n={n})',
                    'X': px,
                    'Y': py
                }
                gpc.append(item)
        
        # plt.figure(figsize=(20,16))
        plt.title('2D-Approximation')
        plt.grid()
        plt.plot(x, y, 'go', markersize=12)
        for item in gpc[:3]:
            plt.plot(item['X'], item['Y'], label=item['legend'])
        plt.legend(loc="upper left")
        return plt#, err    


# Example
# x = [1, 2, 3, 5, 6, 8]
# y = [0.1, 0.4, 0.93, 2.7, 1.8, 1.1]

# plt = Graphic.plot(x, y, npt=100)
# plt.show()