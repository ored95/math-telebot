"""
Function extraction handler
"""
class Function:
    @staticmethod
    def extract(txt):
        """
        Eval handler without exception
        """
        # first search for variable
        def is_alpha(c):
            return c >= 'a' and c <= 'z'
        
        i = 0
        while not is_alpha(txt[i]):
            i += 1
        j = i+1
        while is_alpha(txt[j]):
            j += 1
        txt = txt.replace(txt[i:j], "x")
        tmp = txt[0]
        for i in range(1, len(txt)):
            if not is_alpha(txt[i-1]) and txt[i] == 'x':
                tmp += '*'
            tmp += txt[i]
        tmp = tmp.replace('^', '**')    # x^...
        tmp = tmp.replace('/*', '/')    # 1/x
        tmp = tmp.replace('(*', '(')    # (x ...)
        tmp = tmp.replace('***', '**')  # ...^x
        tmp = tmp.replace(')(', ')*(')  # ...)(...
        return lambda x: eval(tmp)
