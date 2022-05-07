"""
Command with arguments handler
"""
class Request:
    def __init__(self, msg):
        self.cmd = self.extract_cmd(msg)
        self.body = msg
        if self.cmd != None:
            self.body = msg[len(self.cmd):]

    def extract_cmd(self, msg):
        ans = None
        if msg[:3] == '/eq':
            ans = '/eq'
            if 'bst'.find(msg[3]) != -1:
                ans += msg[3]
        elif msg[:6] == '/integ':
            ans = '/integ'
            if 'stlr'.find(msg[6]) != -1:
                ans += msg[6]
        elif msg[:4] == '/app':
            ans = '/app'
            if 'xyv'.find(msg[4]) != -1:
                ans += msg[4]
        elif msg[:5] == '/help':
            ans = '/help'
        return ans
        