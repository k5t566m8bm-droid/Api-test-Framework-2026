import pytest
import allure
from service.order_service import OrderService


@allure.feature("订单模块")
def test_user_pay_order_success(api_client, db):
    """测试用户下单并支付成功"""

    # 1. 调用业务层，一行代码搞定复杂业务流
    order_service = OrderService(api_client)
    pay_resp, order_id = order_service.create_and_pay_order(product_id=101, user_token="xxx")

    # 2. 断言
    assert pay_resp.status_code == 200
    assert pay_resp.json()["status"] == "SUCCESS"

    # 3. 查数据库验证底层状态流转
    db_status = db.query_one("SELECT status FROM orders WHERE order_id = ?", (order_id,))
    assert db_status[0] == "PAID"