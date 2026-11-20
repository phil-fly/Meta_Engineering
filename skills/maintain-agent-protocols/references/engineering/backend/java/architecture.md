# Java 架构与分层

## 核心规则

- 默认继承 `api-design.md`、`auth-and-permission.md`、`data-access.md`、`common-quality.md`、`common-security.md`、`common-performance.md`、`error-and-logging.md`。
- Controller 只处理协议层职责；业务规则放在 Service；数据访问放在 Repository 或 Mapper。
- 请求对象必须使用明确 validation 规则，禁止依赖业务深处才发现基础字段错误。
- 事务边界必须放在业务一致性层；多表写入、删除和状态迁移必须保证一致性。

## 输出要求

- 说明入口层、业务层、数据访问层边界。
