import requests
import json
import logging
from ..utils.cryptoutils import CryptoUtils
from ..utils.httphelper import HttpHelper
from ..exception.account_wrong_error import AccountWrongError
from ..exception.enc_ver_wrong_error import EncVerWrongError

class XTCWatch:
    """
    XTCWatch类
    可进行小天才手表的http请求
    """
    bindNumber = ''
    chipId = ''
    model = ''
    watchId = ''
    encVer: int = 0
    aesKey = ''
    rsaKey = ''
    keyId = ''
    eebbkKey = ''
    logger = None

    def __init__(self, bindNumber: str, chipId: str, model: str, encVer: int = 1, selfKey: str = None,
                 log: bool = False, logLevel = logging.WARNING, proxies = None):
        """
        初始化XTCWatch类

        Args:
            bindNumber: 绑定号
            chipId: 主板id
            model: 机型代号
            encVer: 加密版本可选0(不加密) 1 2 3
            selfKey: 提取的手表密钥，以:分割
            log: 日志开海关
            logLevel: 日志等级
            proxies: 代理设置
        """
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logLevel)
        self.bindNumber = bindNumber
        self.chipId = chipId
        self.model = model
        self.proxies = proxies
        if log:
            logging.basicConfig(
                level=logLevel,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                handlers=[logging.StreamHandler()]
            )
        else:
            self.logger.addHandler(logging.NullHandler())
        self.encVer = encVer
        if encVer == 0:
            self.rsaKey = ''
            self.keyId = ''
        elif encVer == 1:
            self.rsaKey = ''
            self.keyId = ''
        elif encVer == 2:
            splitSelfKey = selfKey.split(':')
            self.rsaKey = splitSelfKey[1]
            self.keyId = splitSelfKey[0]
        elif encVer == 3:
            splitSelfKey = selfKey.split(':')
            self.aesKey = splitSelfKey[1]
            self.eebbkKey = splitSelfKey[2]
            self.keyId = splitSelfKey[0]
        else:
            raise EncVerWrongError()

        self.loadWatchId()

    def loadWatchId(self):
        response = self.request('POST', 'http://watch.okii.com/watchaccount/bindnumber',
                                {'bindNumber': self.bindNumber})
        # print(response)
        resp_data = json.loads(response)
        if resp_data.get('code') == '000001' and resp_data.get('data') != None:
            self.watchId = resp_data.get('data').get('id')
            name = resp_data.get('data').get('name')
            self.logger.info('成功绑定账号:{}({})'.format(name, self.watchId))
        else:
            raise AccountWrongError(resp_data.get('code'))

    def request(self, method: str, url: str, data: dict | str | None) -> str:
        if isinstance(data, dict):
            data = json.dumps(data)
        if self.encVer == 0:
            headers = HttpHelper.buildRequestHeaderWithoutEncrypt(self.bindNumber, self.watchId, self.chipId, self.model)
            return requests.request(method, url, headers=headers, data=data, proxies=self.proxies).text
        elif self.encVer == 1:
            aesKey = CryptoUtils.getAesKey()
            headers = HttpHelper.buildRequestHeaderV1(self.bindNumber, self.watchId, self.chipId, self.model, url,
                                                      data, aesKey)
            if data is not None:
                data = HttpHelper.aesEncrypt(data, aesKey)
            resp = requests.request(method, url, headers=headers, data=data, proxies=self.proxies)
            return HttpHelper.aesDecrypt(resp.text, aesKey) if resp.headers.get(
                'encrypted') == 'encrypted' else resp.text

        elif self.encVer == 2:
            aesKey = CryptoUtils.getAesKey()
            headers = HttpHelper.buildRequestHeaderV2(self.bindNumber, self.watchId, self.chipId, self.model,
                                                      self.keyId + ':' + self.rsaKey, url, data, aesKey)
            if data is not None:
                data = HttpHelper.aesEncrypt(data, aesKey)
            resp = requests.request(method, url, headers=headers, data=data, proxies=self.proxies)
            return HttpHelper.aesDecrypt(resp.text, aesKey) if resp.headers.get(
                'encrypted') == 'encrypted' else resp.text

        elif self.encVer == 3:
            headers = HttpHelper.buildRequestHeaderV3(self.bindNumber, self.watchId, self.chipId, self.model, url,
                                                      data, self.aesKey, self.eebbkKey, self.keyId)
            if data is not None:
                data = HttpHelper.aesEncrypt(data, self.aesKey)
            resp = requests.request(method, url, headers=headers, data=data, proxies=self.proxies)
            return HttpHelper.aesDecrypt(resp.text, self.aesKey) if resp.headers.get(
                'encrypted') == 'encrypted' else resp.text
        else:
            raise EncVerWrongError

    def get(self, url: str) -> str:
        return self.request("GET", url, None)

    def post(self, url: str, data: dict | str) -> str:
        return self.request("POST", url, data)

    def put(self, url: str, data: dict | str) -> str:
        return self.request("PUT", url, data)


