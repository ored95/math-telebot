"""
2D Approximation handler
"""
from sympy import EX
from .approximation_help import *
class Approximation:
    def __init__(self, txt=None):    # cmd: /app x:.. y:..
        # preprocessing 
        self.X = []
        self.Y = []
        if txt is not None:
            txt = txt.lower().replace(' ', '')
            if txt.find('x:') == -1 or txt.find('y:') == -1:
                raise Exception('app: not enough parameter')
            try:
                i = 0
                while txt[i:i+2] != 'x:':
                    i += 1
                i += 2
                j = i
                while txt[j:j+2] != 'y:':
                    j += 1
                self.X = list(map(float, txt[i:j].split(sep=',')))
                self.Y = list(map(float, txt[j+2:].split(sep=',')))
                if len(self.X) != len(self.Y):
                    raise Exception('app: arguments have different size')    
            except:
                raise Exception('Bad request (app): invalid command instruction')
            
    def setX(self, txt):    # cmd: /appx ..
        try:
            self.X = list(map(float, txt.split(sep=',')))
        except:
            raise Exception('appx: parse arguments failed')
    
    def setY(self, txt):    # cmd: /appy
        try:
            self.Y = list(map(float, txt.split(sep=',')))
        except:
            raise Exception('appy: parse arguments failed')

    def interp_help(self, x_value, algo='ne'):  # cmd: /appv
        y_value = None
        if algo == 'ne':
            newton = Newton(self.X, self.Y)
            y_value = [{
                'algo': newton.__str__(),
                'value': newton.interp(x_value)
            }]
        if algo == 'cs':
            cspline = CubicSpline(self.X, self.Y)
            y_value = [{
                'algo': cspline.__str__(),
                'value': cspline.interp(x_value)
            }]
        if algo == 'lsm':
            y_value = []
            for n in range(1, 7):
                lsm = LSM(self.X, self.Y, n)
                item = {
                    'algo': lsm.__str__(),
                    'value': lsm.interp(x_value)
                }
                y_value.append(item)
        return y_value
        
    def interp(self, txt, algos=['ne', 'cs', 'lsm']):   # cmd: /appv
        try:
            if len(self.X) != len(self.Y):
                raise Exception('app: arguments have different size')
            x_value = float(txt)
            res = []
            for algo in algos:
                res.extend(self.interp_help(x_value, algo))
            return res
        except:
            raise Exception('app: unable to convert to float type')    

# Example        
# app = Approximation('x:1, 2,3, 4 y:0.1, 0.4, 0.9, 1.6')
# for item in app.interp('2.5', algos=['ne', 'lsm']):
#     print(f'{item["algo"]}: {item["value"]}')