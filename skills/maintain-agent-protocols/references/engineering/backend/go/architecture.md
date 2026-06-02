# Go 架构与分层

## 核心规则

- 默认继承 `api-design.md`、`auth-and-permission.md`、`data-access.md`、`common-quality.md`、`common-security.md`、`common-performance.md`、`error-and-logging.md`。
- Handler 只处理协议层职责：绑定、基础校验、鉴权上下文读取和响应封装；业务逻辑下沉到 Service。
- Service 负责业务规则、权限语义和事务编排；Repository 只负责数据访问和查询组装。
- 所有受保护接口必须先通过统一认证入口，再做授权和资源归属判断。

## 输出要求

- 说明入口层、业务层、数据访问层边界。
