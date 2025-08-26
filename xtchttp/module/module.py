import json as j
import requests
from ..utils.httphelper import HttpHelper
from ..utils.cryptoutils import CryptoUtils

def reqToV1(method:str,url:str,headers:dict=None,data:str=None,json:dict=None) -> str:
    if headers==None or (data==None and json==None) or (data!=None and json!=None):
        raise Exception('参数错误')
    if json:
        data=j.dumps(json)
    aesKey=CryptoUtils.getAesKey()
    model = headers.get('model')
    brp = j.loads(headers.get('Base-Request-Param'))
    bindNumber = brp.get('deviceId')
    chipId = brp.get('token')
    watchId = brp.get('accountId')
    headers=HttpHelper.buildRequestHeaderV1(bindNumber,watchId,chipId,model,url,data,aesKey)
    if data != None:
        data=HttpHelper.aesEncrypt(data,aesKey)
    resp = requests.request(method,url,headers=headers,data=data)
    return HttpHelper.aesDecrypt(resp.text,aesKey) if resp.headers.get('encrypted')=='encrypted' else resp.text