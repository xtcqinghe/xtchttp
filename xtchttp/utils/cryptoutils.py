import base64
import os
import hashlib
import gzip
import io
import uuid
import random
import string
from datetime import datetime
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.asymmetric import padding as rsa_padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend    

class CryptoUtils:
    @staticmethod
    def aesEncrypt(data: str, key: str) -> str:
        """AES 加密（ECB 模式），返回 Base64 编码的密文"""
        key_bytes = key.encode()
        data_bytes = data.encode('utf-8')
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(data_bytes) + padder.finalize()
        cipher = Cipher(algorithms.AES(key_bytes), modes.ECB(), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        return base64.b64encode(ciphertext).decode('utf-8')

    @staticmethod
    def aesDecrypt(data: str, key: str) -> str:
        """AES 解密（ECB 模式），返回解密后的字符串"""
        key_bytes = key.encode()
        ciphertext = base64.b64decode(data)
        cipher = Cipher(algorithms.AES(key_bytes), modes.ECB(), backend=default_backend())
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(ciphertext) + decryptor.finalize()
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        plaintext = unpadder.update(padded_data) + unpadder.finalize()
        return plaintext

    @staticmethod
    def rsaEncrypt(data: str, key: str) -> str:
        """RSA 加密（PKCS1v1.5 填充），返回 Base64 编码的密文"""
        der_key = base64.b64decode(key)
        public_key = serialization.load_der_public_key(der_key, backend=default_backend())
        data_bytes = data.encode('utf-8')
        ciphertext = public_key.encrypt(
            data_bytes,
            rsa_padding.PKCS1v15()
        )
        return base64.b64encode(ciphertext).decode('utf-8')

    @staticmethod
    def md5Encrypt(data: str) -> str:
        """计算 MD5 哈希值，返回十六进制字符串"""
        md5_hash = hashlib.md5()
        md5_hash.update(data.encode('utf-8'))
        return md5_hash.hexdigest()

    @staticmethod
    def sha256Encrypt(data: str) -> str:
        """计算 SHA-256 哈希值，返回十六进制字符串"""
        sha256_hash = hashlib.sha256()
        sha256_hash.update(data.encode('utf-8'))
        return sha256_hash.hexdigest()
        
    @staticmethod
    def unGzip(compressed_data):
        try:
            buffer = io.BytesIO(compressed_data)
            with gzip.GzipFile(fileobj=buffer, mode='rb') as f:
                decompressed_data = f.read()
            return decompressed_data.decode()
        except Exception as e:
            print(f"解压缩失败：{e}")
            return None
    
    @staticmethod
    def gzip(input_string):
        out = io.BytesIO()
        with gzip.GzipFile(fileobj=out, mode="w") as f:
            f.write(input_string.encode("utf-8"))
        return str(out.getvalue())
    def getUuid(withLine:int=0):
        if withLine==0:
            return str(uuid.uuid4().hex)
        else:
            return str(uuid.uuid4())
    
    @staticmethod
    def getAesKey():
        characters = string.ascii_letters + string.digits
        return ''.join(random.choices(characters, k=16))