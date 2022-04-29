"""
Function extraction handler
"""
from math import sin, cos, tan, exp, pi
class Function:
    @staticmethod
    def extract(txt):
        """
        Eval handler without exception
        TODO: log
        """
        # special function
        spec_funcs = ["sin", "cos", "tan", "exp", "pi"]
        # first search for variable
        def is_alpha(c):
            return c >= 'a' and c <= 'z'
        
        i = 0
        while True:
            while not is_alpha(txt[i]):
                i += 1
            j = i+1
            while is_alpha(txt[j]):
                j += 1
            if txt[i:j] not in spec_funcs:
                break
            else:
                i = j
        
        txt = txt.replace(txt[i:j], "x")
        tmp = txt[0]
        for i in range(1, len(txt)):
            if not is_alpha(txt[i-1]) and txt[i] == 'x':
                tmp += '*'
            tmp += txt[i]
        
        tmp = tmp.replace('^', '**')    # x^...
        tmp = tmp.replace('/*', '/')    # 1/x
        tmp = tmp.replace('+*', '+')    # +x
        tmp = tmp.replace('-*', '-')    # -x
        tmp = tmp.replace('(*', '(')    # (x ...)
        tmp = tmp.replace('***', '**')  # ...^x
        tmp = tmp.replace(')(', ')*(')  # ...)(...
        return lambda x: eval(tmp)
