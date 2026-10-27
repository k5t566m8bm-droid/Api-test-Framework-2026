import pytest
import yaml
import allure
import os  # <--- 新增

from core.assert_handler import AssertHandler

# 获取当前文件所在目录的上一级（项目根目录）
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_yaml(file_path):
    # 用 os.path.join 拼接完整的绝对路径
    full_path = os.path.join(BASE_DIR, file_path)
    with open(full_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

# 这里传入相对于根目录的路径即可
GET_CASES = load_yaml("data/api_cases.yaml")["get_user_cases"]