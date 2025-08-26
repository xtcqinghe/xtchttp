"""
加密版本错误
"""

class EncryptVersionError(Exception):
    def __int__(self, code: str):
        self._code = code

    def __str__(self):
        if self._code == "000016":
            return "您的账号需要v2密钥"
        elif self._code == "000018":
            return "您的账号需要v3密钥"
        else:
            return f"错误码：{self._code}"