"""
账号信息错误
"""

class AccountWrongError(Exception):
    def __init__(self, code: str):
        self._code = code

    def __str__(self):
        return '账号信息错误，请检查后重试。返回码：{}'.format(
                self._code
        )