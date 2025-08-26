"""
加密版本不存在
"""


class EncVerWrongError(Exception):
    def __int__(self):
        pass

    def __str__(self):
        return "加密版本不存在，请选择：0/1/2/3"
