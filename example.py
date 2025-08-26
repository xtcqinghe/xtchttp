import json
import logging
from xtchttp import XTCWatch, CodeError

BIND_NUMBER = "BIND_NUMBER"
CHIP_ID = "CHIP_ID"
MODEL = "MODEL"
SELF_KEY = "SELF_KEY"

def v1():
    watch = XTCWatch(
        BIND_NUMBER,
        CHIP_ID,
        MODEL,
        encVer=1,
        log=True,
        logLevel=logging.INFO
    )
    response: str = watch.get("https://watch.okii.com/rsa")
    response_json: dict = json.loads(response)
    print(response_json)

    response: str = watch.post(
        "https://watch.okii.com/watchfriend/watchinfo/int4Boolean",
        {"watchId": watch.watchId}
    )
    response_json: dict = json.loads(response)
    print(response_json)


def v2():
    watch = XTCWatch(
        BIND_NUMBER,
        CHIP_ID,
        MODEL,
        encVer=2,
        selfKey=SELF_KEY,
        log=True,
        logLevel=logging.INFO
    )
    response: str = watch.get("https://watch.okii.com/rsa")
    response_json: dict = json.loads(response)
    print(response_json)

    response: str = watch.post(
        "https://watch.okii.com/watchfriend/watchinfo/int4Boolean",
        {"watchId": watch.watchId}
    )
    response_json: dict = json.loads(response)
    print(response_json)


def v3():
    watch = XTCWatch(
        BIND_NUMBER,
        CHIP_ID,
        MODEL,
        encVer=3,
        selfKey=SELF_KEY,
        log=True,
        logLevel=logging.INFO
    )
    response: str = watch.get("https://watch.okii.com/rsa")
    response_json: dict = json.loads(response)
    print(response_json)

    response: str = watch.post(
        "https://watch.okii.com/watchfriend/watchinfo/int4Boolean",
        {"watchId": watch.watchId}
    )
    response_json: dict = json.loads(response)
    print(response_json)


def err(code: str, desc: str = None):
    raise CodeError(code, desc)


if __name__ == '__main__':
    v1()
    # v2()
    # v3()
    # err("000016")
    # err("000007", "自定义错误文本")

