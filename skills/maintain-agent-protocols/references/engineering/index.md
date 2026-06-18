# 工程路由索引

本文件只负责路由选择，不承载具体执行细节。需要规则正文时，按任务类型加载对应参考文件。

## 路由选择

```text
UI 页面、组件、交互、表单、Design Token、紧凑布局、JS/TS、权限渲染、前端请求 → frontend/index.md
JavaScript、TypeScript、JSX、TSX、Electron 渲染进程 → frontend/javascript-typescript.md
列表、表格、选择器、枚举、远程搜索        → frontend/list-query.md
提交型表单、字段校验、表单错误展示          → frontend/form-validation.md
颜色 token、品牌色、状态色、中性色          → frontend/design-tokens.md
首屏核心任务、紧凑布局、图表高度            → frontend/compact-ui.md
Go 服务、接口、数据访问、并发、测试       → backend/go.md
Java/Spring 服务、事务、校验、线程池      → backend/java.md
Rust 服务、Result、async、serde、unsafe   → backend/rust.md
Python 服务、schema、async、依赖、验证    → backend/python.md
接口契约、分页、筛选、排序、响应体        → core/api-design.md
登录、授权、资源归属、默认拒绝            → core/auth-and-permission.md
Repository、事务、缓存、存储层查询        → core/data-access.md
输入校验、密钥、审计、OWASP、敏感操作     → security/index.md
运行配置、功能开关、外部集成、配置可发现性  → security/dependency-and-config.md
N+1、资源泄漏、复杂度、阻塞、对象创建     → performance/common-performance.md
命名、注释规范、状态语义、悬空引用、根因修复 → core/common-quality.md
错误码、用户错误、结构化日志、脱敏        → core/error-and-logging.md
路由、限流、认证前置、边界保护            → platform/gateway.md
部署目录、runtime、生命周期、清理策略     → platform/deployment.md
追踪、日志、指标、审计、关联标识          → platform/observability.md
Agent 边界、证据、不确定性、按需加载      → governance/agent-governance.md
技能提示语、模板、元数据一致性             → governance/asset-alignment.md
开发、架构、安全审查、性能审查流程        → ../scenarios/playbooks.md
安全检查、性能检查                         → ../checks/checklists.md
```

## 多路由任务

- UI 列表查询任务：先读 `frontend/list-query.md`，再按查询类型补 `core/api-design.md`、`core/common-quality.md`、`security/index.md` 或 `performance/index.md`。
- 删除接口任务：先读 `core/api-design.md`、`core/auth-and-permission.md`、`core/data-access.md`，再读 `security/index.md`。
- Go/Java/Rust/Python 后端任务：先读 `backend/index.md` 和对应语言文件，再按需要补充 `core/`、`security/`、`performance/`。
- 安全审查任务：先读 `../scenarios/playbooks.md` 的安全审查流程，再读 `security/index.md` 与相关语言路由。
- 性能审查任务：先读 `../scenarios/playbooks.md` 的性能审查流程，再读 `performance/index.md` 与相关语言路由。
- Agent 能力维护：先读 `governance/agent-governance.md`，再按需要补读 `governance/capability-boundary.md`、`governance/evidence-and-scope.md`、`governance/asset-alignment.md` 或 `governance/review-antipatterns.md`。
