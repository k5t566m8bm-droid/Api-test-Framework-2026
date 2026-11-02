# 🚀 企业级纯接口自动化测试框架 (ApiTest-Framework)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Pytest](https://img.shields.io/badge/Pytest-7.0%2B-green)
![Allure](https://img.shields.io/badge/Allure-Report-orange)
![CI](https://img.shields.io/badge/CI-GitHub%20Actions-brightgreen)

## 📖 项目简介

本框架基于 **Python + Pytest + Requests** 独立从 0 到 1 打造，严格遵循“测试金字塔”模型。针对现代互联网敏捷研发流程，剔除维护成本极高的 UI 自动化，专注于**纯接口级**的业务逻辑校验与底层数据一致性保障。

框架采用**模块化分层架构**，引入 **API Object（业务对象）设计模式**，完美解决复杂业务流中接口依赖传参的痛点。结合数据驱动、JSON Schema 深度校验与底层数据库断言，是一套可直接落地于真实企业生产环境的工程化测试底座。

## ✨ 核心特性 (Features)

- **API Object 业务分层**：独离出 `service` 层封装复杂业务动作，让测试用例层（`tests`）极度精简，实现业务逻辑与脚本彻底解耦。
- **企业级安全机制**：底层自动拦截请求，利用 `SignUtil` 工具类实现时间戳与 MD5 自动加签防篡改，支持无缝扩展复杂的 AES/RSA 加密逻辑。
- **SQLAlchemy 连接池**：摒弃原生 SQL 驱动，引入 SQLAlchemy ORM 与连接池 (`pool_size`, `max_overflow`)，大幅提升高并发下数据库操作的安全性与性能。
- **数据工厂与并发隔离**：封装 `DataFactory` 动态生成唯一测试数据（如带时间戳的手机号/姓名），配合 `pytest-xdist` 实现多进程并发且数据互不干扰。
- **API + DB 双端深度断言**：引入 JSON Schema 校验响应结构；直连数据库实现端到端一致性验证；基于 `pytest.fixture` 的 `yield` 机制，确保前置造数与后置清理强制执行。
- **生产级健壮性与 CI/CD**：支持多环境热切换；集成失败重试；全量报文抓取并落盘日志；已配置 GitHub Actions 自动化流水线，实现云端并发回归。
## 📂 项目结构

```text
ApiTest-Framework/
├── .github/workflows/ci.yml      # GitHub Actions 自动化持续集成流水线
├── config/
│   └── env.yaml                  # 多环境配置隔离 (域名/DB路径/鉴权信息)
├── data/
│   └── api_cases.yaml            # 数据驱动测试数据 (YAML)
├── core/                         # 【核心基础设施层】
│   ├── api_client.py             # 底层请求封装 (日志、耗时、报文抓取)
│   ├── db_client.py              # 数据库 CRUD 封装
│   └── assert_handler.py         # JSON Schema 深度断言封装
├── service/                      # 【API Object 业务层】封装接口依赖与业务动作
│   ├── user_service.py           # 用户模块业务流
│   └── order_service.py          # 订单模块业务流 (如：串联下单与支付)
├── tests/                        # 【测试用例层】只负责调用业务与断言
│   ├── test_api_flow.py          # 基础单接口数据驱动用例
│   └── test_order_flow.py        # 核心业务流闭环用例
├── conftest.py                   # 全局 Fixture 与钩子函数(环境清理、路由)
├── pytest.ini                    # Pytest 核心配置 (并发、重试、标签)
├── requirements.txt              # 项目依赖清单
├── .gitignore                    # Git 忽略配置
└── README.md