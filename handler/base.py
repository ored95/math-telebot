# import re
"""
User information handler
"""
class User:
    def __init__(self, msg):
        self.uid = msg.chat.id
        self.uname = self.get_username(msg)
    
    @classmethod
    def get_uid(cls, msg):
        return cls(msg).uid

    def get_username(self, msg):
        user = msg.from_user
        uname = user.first_name + ' ' + user.last_name
        return uname
      