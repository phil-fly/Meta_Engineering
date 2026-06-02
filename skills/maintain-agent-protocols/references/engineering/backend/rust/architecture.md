# Rust 架构与分层

## 核心规则

- 默认继承 `api-design.md`、`auth-and-permission.md`、`data-access.md`、`common-security.md`、`common-performance.md`、`error-and-logging.md`。
- 业务错误使用 `Result` 显式表达，错误类型应能区分用户错误、系统错误和权限错误。
- 业务路径禁止裸 `unwrap`、`expect` 或等价崩溃式处理；只有不可恢复的不变量可明确说明后使用。
- 输入反序列化后必须校验字段约束、长度、枚举值、安全整数范围和资源归属。

## 输出要求

- 说明入口层、业务层、数据访问层边界。
