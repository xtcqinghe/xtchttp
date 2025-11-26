from .cryptoutils import CryptoUtils
import json
from datetime import datetime


class HttpHelper:
    V1_RSA_PUBLIC_KEY = "MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAL9n5AXhw1raL2B6O52LRKOcqjHydrFD4m+lFJW3xv/viRutOim4twKFlamB/edfz1KqydsMTVqsDCRiz8UuKU0CAwEAAQ=="

    @staticmethod
    def buildBaseRequestParam(bind, watchId, chipid):
        param_json = {"accountId": watchId,
                      "appId": "2",
                      "deviceId": bind,
                      "imFlag": "1",
                      "mac": "unkown",
                      "program": "watch",
                      "registId": 0,
                      "requestId": CryptoUtils.getUuid(0),
                      "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                      "token": chipid
                      }
        return json.dumps(param_json).replace(' "', '"')

    @staticmethod
    def sign(url, param, data, aesKey):
        if data == 'null' or not data:
            data = ''
        return CryptoUtils.md5Encrypt(HttpHelper.dealUrl(url) + param + data + aesKey).upper()

    @staticmethod
    def getEebbkKeyV1(aesKey):
        return CryptoUtils.rsaEncrypt(aesKey,HttpHelper.V1_RSA_PUBLIC_KEY)

    @staticmethod
    def getEebbkKeyV2(aesKey, rsaKey):
        return CryptoUtils.rsaEncrypt(aesKey, rsaKey)

    @staticmethod
    def buildRequestHeaderWithoutEncrypt(bind, watchId, chipid, model, version="2.0.0"):
        return {
            "uuid": CryptoUtils.getUuid(1),
            "model": model,
            "imSdkVersion": "102",
            "packageVersion": "52710",
            "packageName": "com.xtc.moment",
            "Eebbk-Sign": "0",
            "Base-Request-Param": HttpHelper.buildBaseRequestParam(bind, watchId, chipid),
            "dataCenterCode": "CN_BJ",
            "Version": F"W_{version}",
            "Grey": "0",
            "Accept-Language": "zh-CN",
            "Watch-Time-Zone": "GMT+08:00",
            "Content-Type": "application/json; charset=UTF-8",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.12.0"
        }

    @staticmethod
    def buildRequestHeaderV1(bind, watchId, chipid, model, url, data, aesKey, version="2.0.0"):
        param = HttpHelper.buildBaseRequestParam(bind, watchId, chipid)
        eebbkSign = HttpHelper.sign(url, param, data, aesKey)
        eebbkKey = HttpHelper.getEebbkKeyV1(aesKey)
        baseRequestParam = HttpHelper.aesEncrypt(param, aesKey)
        headers = {
            "uuid": CryptoUtils.getUuid(1),
            "model": model,
            "imSdkVersion": "102",
            "packageVersion": "52700",
            "packageName": "com.xtc.moment",
            "Eebbk-Sign": eebbkSign,
            "Base-Request-Param": baseRequestParam,
            "Eebbk-Key": eebbkKey,
            "encrypted": "encrypted",
            "dataCenterCode": "CN_BJ",
            "Version": f"W_{version}",
            "Grey": "0",
            "Accept-Language": "zh-CN",
            "Watch-Time-Zone": "GMT+08:00",
            "Content-Type": "application/json; charset=UTF-8",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.12.0"
        }
        return headers

    @staticmethod
    def buildRequestHeaderV2(bind, watchId, chipid, model, selfKey, url, data, aesKey, version="2.0.0"):
        a = selfKey.split(':')
        rsaKey = a[1]
        keyId = a[0]
        param = HttpHelper.buildBaseRequestParam(bind, watchId, chipid)
        eebbkSign = HttpHelper.sign(url, param, data, aesKey)
        eebbkKey = HttpHelper.getEebbkKeyV2(aesKey, rsaKey)
        baseRequestParam = HttpHelper.aesEncrypt(param, aesKey)
        headers = {
            "uuid": CryptoUtils.getUuid(1),
            "model": model,
            "imSdkVersion": "102",
            "packageVersion": "52700",
            "packageName": "com.xtc.moment",
            "Eebbk-Sign": eebbkSign,
            "Base-Request-Param": baseRequestParam,
            "Eebbk-Key": eebbkKey,
            "Eebbk-Key-Id": keyId,
            "encrypted": "encrypted",
            "dataCenterCode": "CN_BJ",
            "Version": f"W_{version}",
            "Grey": "0",
            "Accept-Language": "zh-CN",
            "Watch-Time-Zone": "GMT+08:00",
            "Content-Type": "application/json; charset=UTF-8",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.12.0"
        }
        return headers

    @staticmethod
    def buildRequestHeaderV3(bind, watchId, chipid, model, url, data, aesKey, eebbkKey, keyId, version="2.0.0"):
        param = HttpHelper.buildBaseRequestParam(bind, watchId, chipid)
        eebbkSign = HttpHelper.sign(url, param, data, aesKey)
        baseRequestParam = HttpHelper.aesEncrypt(param, aesKey)
        headers = {
            "uuid": CryptoUtils.getUuid(1),
            "model": model,
            "imSdkVersion": "102",
            "packageVersion": "52700",
            "packageName": "com.xtc.moment",
            "Eebbk-Sign": eebbkSign,
            "Base-Request-Param": baseRequestParam,
            "Eebbk-Key": eebbkKey,
            "Eebbk-Key-Id": keyId,
            "encrypted": "encrypted",
            "dataCenterCode": "CN_BJ",
            "Version": f"W_{version}",
            "Grey": "0",
            "Accept-Language": "zh-CN",
            "Watch-Time-Zone": "GMT+08:00",
            "Content-Type": "application/json; charset=UTF-8",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.12.0"
        }
        return headers

    @staticmethod
    def aesEncrypt(data, key):
        return CryptoUtils.aesEncrypt(data, key)

    @staticmethod
    def aesDecrypt(data, key):
        return CryptoUtils.unGzip(CryptoUtils.aesDecrypt(data, key))

    @staticmethod
    def dealUrl(url):
        query_start = url.find('?')
        fragment_start = url.find('#')
        if query_start == -1:
            return url
        if fragment_start != -1:
            return url[:query_start] + url[fragment_start:]
        else:
            return url[:query_start]
