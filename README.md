# xtchttp - 小天才API请求工具

> 面向小天才手表的 HTTP 通信封装，支持全版本加密，自动完成密钥协商与数据加解密。

---

## 1. 安装

>复制库到项目目录

依赖  
```
pip install requests cryptography
```

---

## 2. 快速开始

```python
from xtchttp import XTCWatch

watch = XTCWatch(
    bindNumber="",
    chipId="",
    model="",
    encVer=1
)

# 发送 GET
print(watch.get("http://watch.okii.com/get"))

# 发送 POST
resp = watch.post("http://watch.okii.com/post", {"watchId": watch.watchId})
print(resp)
```

---

## 3. 参数说明

| 参数 | 类型 | 默认值 | 说明                                                                   |
|---|---|---|----------------------------------------------------------------------|
| **bindNumber** | str | - | 手表绑定号（必填）                                                            |
| **chipId** | str | - | 手表主板 ID（必填）                                                          |
| **model** | str | - | 机型代号，如 `I18`、`I32`（必填）                                               |
| **encVer** | int | 1 | 加密版本：<br>`0` 不加密<br>`1` 内置 RSA 公钥<br>`2` 自定义 RSA 公钥<br>`3` 自定义 AES+密钥 |
| **selfKey** | str | None | `encVer=2/3` 时必须提供，格式见下                                              |
| **log** | bool | False | 是否打印日志                                                               |
| **logLevel** | int | logging.WARNING | 日志等级                                                                 |
| **proxies** | dict | None | `requests` 代理字典                                                      |

### 3.1 selfKey 格式

| encVer | 格式                               |
|---|----------------------------------|
| 2 | `keyId:rsaPublicKey`             |
| 3 | `keyId:aesKey:encryptedEebbkKey` |

---

## 4. 公开方法

### 4.1 request(method, url, data=None) → str
通用请求方法，自动根据加密版本加解密并构建头信息。

```python
watch.request("POST", "http://watch.okii.com/post", {"msg": "test"})
```

### 4.2 get(url) → str
简化 GET 请求。

```python
watch.get("http://watch.okii.com/get")
```

### 4.3 post(url, data) → str
简化 POST 请求。

```python
watch.post("http://watch.okii.com/post", {"watchId": watch.watchId})
```

### 4.4 put(url, data) → str
简化 PUT 请求。
```python
watch.put("http://watch.okii.com/put", {"watchId": watch.watchId})
```

---

## 5. 加密版本差异

| 版本 | 加密方式    | 说明                        |
|---|---------|---------------------------|
| 0 | 无       | 不加密                       |
| 1 | RSA+AES | 使用内置 RSA 公钥               |
| 2 | RSA+AES | 使用自定义 RSA 公钥（需 `selfKey`） |
| 3 | RSA+AES | 使用自定义 AES 密钥（需 `selfKey`） |

---

## 6. 日志

开启日志示例：

```python
import logging
watch = XTCWatch("", "", "", log=True, logLevel=logging.INFO)
```

输出示例：
```
2024-06-01 12:00:00 - xtcwatch - INFO - 成功绑定账号:user(1234567)
```

---

## 7. 代理

走本地代理：

```python
watch = XTCWatch(
    "", "", "",
    proxies={"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
)
```

---

## 8. 异常

| 异常 | 触发场景 |
|---|---|
| `Exception("encVer错误")` | 传入非法 `encVer` |
| 初始化失败 | 绑定号错误或网络问题，提示 `获取watchId失败` |
| 网络异常 | 由 `requests` 抛出 |

---

## 9. 完整示例

```python
from xtchttp import XTCWatch

# 使用 encVer=3，需提供自定义密钥
self_key = "key_id:aes_key:encrypted_eebbk_key"
watch = XTCWatch(
    bindNumber="",
    chipId="",
    model="",
    encVer=3,
    selfKey=self_key,
    log=True
)

# get
resp = watch.get("http://watch.okii.com/")
print("返回体:", resp)

# post
resp = watch.post("http://watch.okii.com/", {})
print("返回体:", resp)
```

---

## 10. 注意事项

1. **bindNumber**、**chipId**、**model** 必须与实际手表一致，否则初始化会失败。  
2. `encVer=1` 使用内置 RSA 公钥，无需额外密钥。  

3. 若使用代理，请确保代理支持 CONNECT 隧道，且不会篡改 HTTPS 证书链。

4. 本项目仅供学习参考，使用本项目造成的一切后果由本人承担。

