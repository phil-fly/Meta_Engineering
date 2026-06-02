# Python 后端总览

适用 Python 后端服务、脚本型服务、API 服务、任务队列和数据处理入口。具体框架约束以项目证据为准，例如 FastAPI、Django、Flask、Celery、Airflow 或项目自定义框架。

## 核心规则

- 默认继承 `../core/api-design.md`、`../core/auth-and-permission.md`、`../core/data-access.md`、`../core/common-quality.md`、`../core/error-and-logging.md`、`../security/index.md` 和 `../performance/common-performance.md`。
- 入口层只处理协议适配、基础校验、认证上下文读取和响应封装；业务规则应下沉到 service、domain 或 use case 层。
- 数据模型、DTO、schema 和 ORM 模型职责应保持清晰；禁止把请求解析、业务决策和持久化细节混在同一对象里。
- 输入反序列化后必须校验字段约束、枚举值、长度、范围、安全整数和资源归属。
- async 代码不得执行长时间同步阻塞；阻塞 I/O 应隔离到合适线程池、进程池或同步执行边界，并设置超时。
- 文件、连接、游标、事务、锁和临时资源必须有关闭、提交、回滚或清理路径，优先使用 context manager 或等价生命周期管理。
- 业务错误应映射为稳定错误码和可操作消息；详细排障信息进入日志，不向客户端泄露堆栈、SQL、内部路径或敏感配置。
- 依赖、虚拟环境和锁文件策略应可追踪；高危依赖漏洞应及时升级或记录例外。
- 高风险 Python 后端改动必须提供至少一种可重复执行的验证命令，并说明验证了什么行为或范围。

## 输出要求

- 说明本次任务涉及入口层、业务层、数据访问、异步/阻塞、资源生命周期或依赖验证中的哪些子域。
- 说明安全、性能、错误表达和可重复验证是否覆盖。
