import json
import logging

from xtchttp import *
import xtchttp


def main():
    # 第一步：创建XTCWatch类
    watch = XTCWatch(
        # 填写手表信息
        bindNumber="",
        chipId="",
        model="",
        # 以下为非必填项
        selfKey='',  # 加密密钥
        encVer=1,  # 加密版本
        log=True,  # 开启日志
        logLevel=logging.INFO,  # 设置日志等级
        proxies={
            "http": None,
            "https": None
        }  # 设置代理
    )
    # 第二步：请求
    try:
        response = watch.post(
            "https://watch.okii.com/watchfriend/watchinfi/int4Boolean",
            {"watchId": watch.watchId}
        )
        response_json = json.loads(response)
        watch.logger.info("返回码: " + response_json.get("code"))
    except Exception as e:
        watch.logger.error(e)


if __name__ == "__main__":
    main()
