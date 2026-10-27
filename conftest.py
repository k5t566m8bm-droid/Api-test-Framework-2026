import pytest
import yaml
import shutil
import os
from core.db_client import DBClient
from core.api_client import ApiClient


def pytest_sessionstart(session):
    """启动前清理历史数据，并写入 Allure 环境信息"""
    allure_dir = "./allure-results"
    if os.path.exists(allure_dir):
        shutil.rmtree(allure_dir)
    os.makedirs(allure_dir)

    with open(os.path.join(allure_dir, "environment.properties"), "w", encoding="utf-8") as f:
        f.write("Tester=ZhaoTingTing\n")
        f.write("Environment=Test_Env\n")
        f.write("Python_Version=3.10\n")


def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="test", help="选择运行环境: test 或 pro")


@pytest.fixture(scope="session")
def env_config(request):
    env_name = request.config.getoption("--env")
    with open("config/env.yaml", "r", encoding="utf-8") as f:
        all_envs = yaml.safe_load(f)["env"]
    return all_envs[env_name]


@pytest.fixture(scope="session")
def db(env_config):
    db_client = DBClient(env_config["db_path"])
    yield db_client
    db_client.close()


@pytest.fixture(scope="session")
def api_client(env_config):
    client = ApiClient(env_config["base_url"])
    # 模拟全局鉴权，真实项目此处应为调登录接口获取 token
    client.set_token("fake_token_for_demo")
    return client