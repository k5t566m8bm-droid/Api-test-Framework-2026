# utils/sign_util.py
import hashlib
import time
import json


class SignUtil:
    @staticmethod
    def get_timestamp():
        """获取当前毫秒级时间戳"""
        return str(int(time.time() * 1000))

    @staticmethod
    def generate_sign(params: dict, secret_key: str):
        """
        模拟企业级签名生成逻辑：
        1. 将参数字典按 key 升序排列
        2. 拼接成 key=value 的形式
        3. 末尾加上秘钥 secret_key
        4. 进行 MD5 加密，转成大写
        """
        # 过滤掉空值和 sign 字段本身
        filter_params = {k: v for k, v in params.items() if v is not None and k != "sign"}

        # 按照字典的键排序
        sorted_params = sorted(filter_params.items())

        # 拼接成字符串
        sign_str = "&".join([f"{k}={v}" for k, v in sorted_params])

        # 加上分配给我们的私钥（真实环境里这个秘钥是绝对不能泄露的）
        sign_str += f"&key={secret_key}"

        # 计算 MD5
        md5 = hashlib.md5(sign_str.encode('utf-8'))
        return md5.hexdigest().upper()