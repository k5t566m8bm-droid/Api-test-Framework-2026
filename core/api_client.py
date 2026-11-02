import requests
import logging
import allure
from utils.sign_util import SignUtil  # 引入签名工具

# 配置日志落盘
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("api_test.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)


class ApiClient:
    def __init__(self, base_url, secret_key="my_secret_key_123"):
        self.base_url = base_url
        self.secret_key = secret_key  # <--- 加上这一行，初始化秘钥
        self.session = requests.Session()

    def set_token(self, token):
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    def _request(self, method, path, **kwargs):
        url = f"{self.base_url}{path}"

        # ================= 核心改造：自动生成签名 =================
        # 获取当前的参数 (json 或 params)
        payload = kwargs.get("json") or kwargs.get("params") or {}

        if payload:
            # 1. 加上时间戳
            payload["timestamp"] = SignUtil.get_timestamp()
            # 2. 生成签名
            payload["sign"] = SignUtil.generate_sign(payload, self.secret_key)

            # 3. 更新回 kwargs 中
            if "json" in kwargs:
                kwargs["json"] = payload
            if "params" in kwargs:
                kwargs["params"] = payload

        logging.info(f"发送请求: {method.upper()} {url} | 实际参数: {payload}")
        # ==========================================================

        # 真正发送请求
        resp = self.session.request(method.upper(), url, timeout=10, **kwargs)

        # 记录耗时
        cost_time = resp.elapsed.total_seconds()

        # 记录到 Allure 报告
        allure.attach(
            f"URL: {url}\nMethod: {method}\nParams: {kwargs}\n\n"
            f"Status: {resp.status_code}\nCost: {cost_time}s\nBody: {resp.text}",
            name="请求响应详情", attachment_type=allure.attachment_type.TEXT
        )
        logging.info(f"{method.upper()} {url} - Status: {resp.status_code} - Time: {cost_time}s")

        # 最后才返回响应
        return resp

    def get(self, path, params=None, **kwargs):
        return self._request("GET", path, params=params, **kwargs)

    def post(self, path, data=None, json=None, **kwargs):
        return self._request("POST", path, data=data, json=json, **kwargs)

    def delete(self, path, **kwargs):
        return self._request("DELETE", path, **kwargs)