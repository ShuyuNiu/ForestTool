__author__ = 'zxlee'
__github__ = 'https://github.com/SmileZXLee/forestTool'


class User:
    user_name = ''
    user_id = ''
    remember_token = ''

    def __init__(self, user_name, user_id, remember_token):
        self.user_name = user_name
        self.user_id = user_id
        self.remember_token = remember_token
