"""
2D Approximation handler
"""
from approximation_help import *
class Approximation:
    def __init__(self, txt):    # cmd: /app x:.. y:..
        # preprocessing 
        txt = txt.lower().replace(' ', '')
        self.X = []
        self.Y = []
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
        except:
            raise Exception('Parse arguments failed')
        
    def setX(self, txt):    # cmd: /appx ..
        try:
            self.X = list(map(float, txt.split(sep=',')))
        except:
            raise Exception('Parse arguments failed')
    
    def setY(self, txt):    # cmd: /appy
        try:
            self.Y = list(map(float, txt.split(sep=',')))
        except:
            raise Exception('Parse arguments failed')

    def interp_help(self, x_value, method=Newton):
        return method.interp(x_value, self.X, self.Y)
        
    def interp(self, txt, methods=[Newton]):
        try:
            x_value = float(txt)
            res = []
            for method in methods:
                res.append(self.interp_help(x_value, method))
            return res
        except:
            raise Exception('unable to convert to float type')    
        
app = Approximation('x:1, 2,3, 4 y:0.1, 0.4, 0.9, 1.6')
print(app.interp('2.5'))