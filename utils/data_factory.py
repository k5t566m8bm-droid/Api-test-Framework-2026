import time
import random

class DataFactory:
    @staticmethod
    def get_unique_name(prefix="测试用户"):
        """生成带时间戳和随机数的唯一名称，防止并发冲突"""
        timestamp = int(time.time() * 1000)
        rand_num = random.randint(100, 999)
        return f"{prefix}_{timestamp}_{rand_num}"

    @staticmethod
    def get_mock_phone():
        """生成随机的手机号"""
        return f"138{random.randint(10000000, 99999999)}"