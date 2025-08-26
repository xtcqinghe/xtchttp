from ..mapping.error_code import ERROR_CODE_MAPPING


class CodeError(Exception):
    """
    响应码非000001，提供报错及帮助
    """
    def __init__(self, code: str, desc: str = None):
        self._code = code
        self._desc = desc

    def __str__(self):
        if self._desc:
            return self._desc
        else:
            return ERROR_CODE_MAPPING.get(self._code, ERROR_CODE_MAPPING["_"])
