import pytest
import yaml
import allure
from core.assert_handler import AssertHandler


def load_yaml(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


GET_CASES = load_yaml("../data/api_cases.yaml")["get_user_cases"]


@allure.feature("接口业务闭环测试")
class TestApiFlow:

    @pytest.mark.regression
    @pytest.mark.parametrize("case_data", GET_CASES)
    def test_api_data_driven(self, api_client, case_data):
        """数据驱动验证、Schema深度断言与耗时断言"""
        allure.story(case_data["case_name"])

        method = case_data["method"]
        path = case_data["path"]

        func = getattr(api_client, method.lower())
        resp = func(path)

        # 断言 1：状态码
        assert resp.status_code == case_data["expect_status"], f"{case_data['case_name']} 状态码不符"

        # 断言 2：字段存在
        if "expect_field" in case_data and resp.status_code == 200:
            assert case_data["expect_field"] in resp.json()

        # 断言 3：Schema 深度结构校验
        if "expect_schema" in case_data:
            AssertHandler.assert_schema(resp.json(), case_data["expect_schema"])

        # 断言 4：响应时间断言（小于2秒）
        cost_time = resp.elapsed.total_seconds()
        assert cost_time < 2.0, f"接口性能不达标，耗时 {cost_time}s"

    # ================= 核心业务链：DB数据自动清理 + 接口依赖 =================
    @pytest.fixture
    def create_and_clean_customer(self, db):
        """前置造数据，后置强制清理"""
        customer_name = "赵婷婷测试客户"
        job = "高级测试工程师"

        with allure.step(f"前置准备：创建一条测试数据 -> {customer_name}"):
            db.insert("INSERT INTO users (name, job) VALUES (?, ?)", (customer_name, job))

        yield customer_name, job

        with allure.step(f"后置清理：自动删除测试数据 -> {customer_name}"):
            db.delete("DELETE FROM users WHERE name = ?", (customer_name,))

    @pytest.mark.regression
    def test_db_transaction_flow(self, api_client, db, create_and_clean_customer):
        allure.story("用户增删接口依赖与底层数据一致性校验")
        customer_name, job = create_and_clean_customer

        with allure.step("步骤1：查库确认前置数据存在"):
            db_result = db.query_one("SELECT name, job FROM users WHERE name = ?", (customer_name,))
            assert db_result is not None

        with allure.step("步骤2：发送 POST 请求新增用户，提取动态ID"):
            resp = api_client.post("/users", json={"name": customer_name, "job": job})
            assert resp.status_code == 201
            new_user_id = resp.json().get("id")
            assert new_user_id is not None, "接口未返回有效的用户ID"

        with allure.step(f"步骤3：使用动态ID [{new_user_id}] 发送 GET 请求获取详情"):
            get_resp = api_client.get(f"/users/{new_user_id}")
            assert get_resp.status_code == 200

        with allure.step(f"步骤4：使用动态ID [{new_user_id}] 发送 DELETE 请求"):
            del_resp = api_client.delete(f"/users/{new_user_id}")
            assert del_resp.status_code == 200