from core.api_client import ApiClient


class OrderService:
    def __init__(self, api_client: ApiClient):
        self.api = api_client

    def create_and_pay_order(self, product_id, user_token):
        """封装：创建订单 -> 提取ID -> 支付订单"""
        self.api.set_token(user_token)

        # 1. 创建订单
        create_resp = self.api.post("/api/order/create", json={"product_id": product_id})
        assert create_resp.status_code == 200
        order_id = create_resp.json()["data"]["order_id"]

        # 2. 支付订单（依赖上一步的 order_id）
        pay_resp = self.api.post("/api/order/pay", json={"order_id": order_id})
        return pay_resp, order_id