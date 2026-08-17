# 工程路由索引

本文件只负责路由选择，不承载具体执行细节。需要规则正文时，按任务类型加载对应参考文件。

## 路由选择

```text
UI 页面、组件、交互、表单、Design Token、紧凑布局、UI 稳定性、国际化、文案治理、JS/TS、权限渲染、前端请求、项目结构、状态缓存、测试、可访问性、工具链、前端性能 → frontend/index.md
企业级 SaaS 产品设计、管理后台、控制台、运维平台、安全平台、云管平台、AI 平台、数据平台、设备管理系统、线框图、视觉稿 Prompt → frontend/enterprise-saas-design.md
JavaScript、TypeScript、JSX、TSX、Electron 渲染进程 → frontend/javascript-typescript.md
前端目录、feature 边界、共享层、导入方向、文件命名 → frontend/project-structure.md
共享组件、页面局部组件、第三方组件包装、Storybook → frontend/component-system.md
组件状态、应用状态、服务端缓存、URL 状态、缓存失效 → frontend/state-and-cache.md
列表、表格、选择器、枚举、远程搜索        → frontend/list-query.md
提交型表单、字段校验、表单错误展示          → frontend/form-validation.md
用户可见文案、翻译 Key、语言资源、硬编码文案 → frontend/i18n-governance.md
目标仓前端设计规范盘点、Token 真值源、组件与页面模式维护、视觉漂移审查 → frontend/design-system-maintenance.md
颜色 token、品牌色、状态色、中性色、间距、字号、圆角、阴影、motion、组件 token → frontend/styling-and-tokens.md
首屏核心任务、紧凑布局、图表高度            → frontend/compact-ui.md
UI 稳定性、分辨率、浏览器缩放、长文本、表格列宽、Dialog/Drawer 溢出、极限数据 → frontend/ui-stability.md
键盘、焦点、ARIA、语义、复杂组件可访问性、a11y → frontend/accessibility.md
前端单元测试、集成测试、E2E、MSW、用户行为测试 → frontend/testing.md
ESLint、Prettier、TypeScript、typecheck、lint、test、build、CI、前端依赖 → frontend/tooling-and-verification.md
前端首屏、code splitting、bundle、图片字体、Web Vitals → frontend/frontend-performance.md
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
安全检查、前端国际化检查、前端可访问性检查、前端测试检查、前端 UI 稳定性检查、前端组件检查、前端结构检查、性能检查 → ../checks/checklists.md
```

## 多路由任务

- UI 列表查询任务：先读 `frontend/list-query.md`，再按查询类型补 `core/api-design.md`、`core/common-quality.md`、`security/index.md` 或 `performance/index.md`。
- 企业级 SaaS 产品设计、管理后台、控制台、运维/安全/云管/AI/数据平台页面设计：先读 `../scenarios/playbooks.md` 的 `WF-ENTERPRISE-SAAS-DESIGN`，再读 `frontend/enterprise-saas-design.md`，并按页面类型补 `frontend/compact-ui.md`、`frontend/ui-stability.md`、`frontend/component-system.md`、`frontend/list-query.md`、`frontend/form-validation.md`、`frontend/styling-and-tokens.md` 或 `frontend/accessibility.md`。
- UI 页面、弹窗、表单、表格、菜单或提示反馈任务：先读 `frontend/i18n-governance.md`；涉及新页面、共享组件、主题、布局、响应式或视觉参数时补读 `frontend/design-system-maintenance.md`，再按任务类型补 `frontend/form-validation.md`、`frontend/interaction-and-permission.md`、`core/error-and-logging.md` 或其他相关路由。
- 前端结构、组件、状态、测试、UI 稳定性、可访问性、工具链或性能任务：先读 `frontend/index.md`，再按任务类型补 `frontend/project-structure.md`、`frontend/component-system.md`、`frontend/state-and-cache.md`、`frontend/testing.md`、`frontend/ui-stability.md`、`frontend/accessibility.md`、`frontend/tooling-and-verification.md` 或 `frontend/frontend-performance.md`。
- 删除接口任务：先读 `core/api-design.md`、`core/auth-and-permission.md`、`core/data-access.md`，再读 `security/index.md`。
- Go/Java/Rust/Python 后端任务：先读 `backend/index.md` 和对应语言文件，再按需要补充 `core/`、`security/`、`performance/`。
- 安全审查任务：先读 `../scenarios/playbooks.md` 的安全审查流程，再读 `security/index.md` 与相关语言路由。
- 性能审查任务：先读 `../scenarios/playbooks.md` 的性能审查流程，再读 `performance/index.md` 与相关语言路由。
- Agent 能力维护：先读 `governance/agent-governance.md`，再按需要补读 `governance/capability-boundary.md`、`governance/evidence-and-scope.md`、`governance/asset-alignment.md` 或 `governance/review-antipatterns.md`。
