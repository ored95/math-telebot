"""
Command with arguments handler
"""
class Request:
    def __init__(self, msg):
        self.cmd = self.extract_cmd(msg)
        self.body = msg
        if self.cmd != None:
            self.body = msg[len(self.cmd):]

    # @staticmethod
    def extract_cmd(self, msg):
        ans = None
        if msg[:3] == '/eq':
            ans = '/eq'
            if 'bst'.find(msg[3]) != -1:
                ans += msg[3]
        elif msg[:6] == '/integ':
            ans = '/integ'
        elif msg[:4] == '/app':
            ans = '/app'
        elif msg[:5] == '/help':
            ans = '/help'
        return ans

    def extract_arguments(self):
        pass