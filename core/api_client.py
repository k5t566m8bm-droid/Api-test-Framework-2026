import requests
import logging
import allure

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
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def set_token(self, token):
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    def _request(self, method, path, **kwargs):
        url = f"{self.base_url}{path}"
        resp = self.session.request(method.upper(), url, timeout=10, **kwargs)

        cost_time = resp.elapsed.total_seconds()

        allure.attach(
            f"URL: {url}\nMethod: {method}\nParams: {kwargs}\n\n"
            f"Status: {resp.status_code}\nCost: {cost_time}s\nBody: {resp.text}",
            name="请求响应详情", attachment_type=allure.attachment_type.TEXT
        )
        logging.info(f"{method.upper()} {url} - Status: {resp.status_code} - Time: {cost_time}s")

        return resp

    def get(self, path, params=None, **kwargs):
        return self._request("GET", path, params=params, **kwargs)

    def post(self, path, data=None, json=None, **kwargs):
        return self._request("POST", path, data=data, json=json, **kwargs)

    def delete(self, path, **kwargs):
        return self._request("DELETE", path, **kwargs)