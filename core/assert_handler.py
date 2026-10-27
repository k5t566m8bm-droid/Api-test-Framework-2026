import jsonschema
import allure

class AssertHandler:
    @staticmethod
    def assert_schema(data, schema):
        try:
            jsonschema.validate(instance=data, schema=schema)
        except jsonschema.exceptions.ValidationError as e:
            allure.attach(str(e), name="Schema校验失败详情", attachment_type=allure.attachment_type.TEXT)
            raise AssertionError(f"数据结构校验失败: {e.message}")