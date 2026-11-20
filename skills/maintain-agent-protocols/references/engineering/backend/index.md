# 后端工程入口

Go、Java、Rust、Python 后端服务任务先读本文件，再按语言读取对应文件。

## 文件

- `go.md`：Go 后端、并发、context、错误和测试规则。
- `java.md`：Java/Spring 后端、事务、校验、异常、线程池和依赖规则。
- `rust.md`：Rust 后端、Result、async、serde、unsafe 和并发规则。
- `python.md`：Python 后端、schema、async、资源生命周期、依赖和验证规则。

## 关联

- API 契约：读取 `../core/api-design.md`。
- 鉴权授权：读取 `../core/auth-and-permission.md`。
- 数据访问：读取 `../core/data-access.md`。
- 用户错误与日志职责分离：读取 `../core/error-and-logging.md`。
- 高风险后端变更验证：Go、Java、Rust 结合语言级 `verification.md`，Python 结合 `python.md` 中的验证要求，并读取 `../core/error-and-logging.md` 说明可重复验证命令。
- 安全控制：读取 `../security/index.md`。
- 性能约束：读取 `../performance/common-performance.md`。
