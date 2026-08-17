# 场景化引用入口

本目录按使用场景分层。先根据任务选择场景目录，再按需读取具体文件，不要默认全量加载。

## 协议生成与维护

- `protocol/index.md`：协议场景入口与读取顺序。
- `protocol/guide.md`：协议层级、目标仓目录结构、入口模板、维护检查和冲突处理。
- `protocol/index.md` 同时覆盖协议包升级同步场景，用于已落盘项目协议对照最新技能规则做差异审查和最小修改同步。
- `protocol/collaboration-boundaries.md`：用户协作边界、讨论/执行/维护模式、确认门槛、证据范围和完成定义。
- `protocol/protocol-engineer.md`：协议工程审查，覆盖角色定位、协议膨胀、执行率、冲突、结构和 Token 成本。
- `protocol/trigger-stability-guide.md`：触发稳定性审查，覆盖任务入口、场景手册、工程路由、项目约束、约束门禁和检查项之间的触发链路。
- `protocol/rule-ingestion.md`：原则、约束、约束触发项、执行流程、模板、检查项和知识的摄入与触发判断。
- `protocol/openspec-workflow.md`：Spec-first 工作流，覆盖规范前置、变更闭环、审查闭环和 Epic 拆分。
- `protocol/package-blueprint.md`：目标仓协议包落盘蓝图，说明生成方案预览、入口兼容、三档生成模式、路由状态标注、目录、内容来源和不会自动生成的边界。
- `protocol/skill-structure.md`：技能自身目录结构说明，覆盖多层 `references/`、`templates/` 和结构校验 warning 处理。
- `protocol/user-protocol-template.md`：用户级协议模板，可直接复用后按项目裁剪。
- `protocol/project-protocol-template.md`：项目级协议模板，可直接复用后按仓库约束裁剪。
- `protocol/route-card-template.md`：工程路由卡片模板，可落盘到 `ai-agent-protocols/templates/route-card.md`。
- `../templates/user-protocol.md`、`project-protocol.md`、`route-card.md`：复制到目标仓 `ai-agent-workspace/protocols/templates/`，旧项目可兼容 `ai-agent-protocols/templates/`。
- `../templates/frontend-design-system-review-prompt.md`：复制到目标仓协议模板目录，作为前端设计系统基线调查与变更审查的独立只读提示语；它不在 `references/protocol/` 维护镜像正文。
- `../templates/design-tokens.md`：仅在目标仓存在或将首次引入真实前端实现时，实例化为 `ai-agent-workspace/product/design/design-tokens.md` 或继承兼容 `docs/03_DESIGN/design-tokens.md`；不得复制到协议模板或路由目录。

## 工程规则路由

- `engineering/index.md`：工程路由总索引，先读它决定后续加载目录。
- `engineering/frontend/`：前端和 UI 开发，包含目标仓设计系统维护、企业级 SaaS 设计、项目结构、组件系统、状态缓存、请求数据、表单、国际化、样式 token、紧凑 UI、UI 稳定性、可访问性、测试、工具链和前端性能。
- `engineering/backend/`：Go、Java、Rust、Python 后端开发。
- `engineering/core/`：API、鉴权授权、数据访问、通用质量、错误与日志。
- `engineering/security/`：通用安全、OWASP 和敏感操作。
- `engineering/performance/`：通用性能和性能审查。
- `engineering/platform/`：网关、部署和可观测性。
- `engineering/governance/`：Agent 能力边界、证据范围、资产一致性和审查反模式。

## 场景流程

- `scenarios/index.md`：场景流程入口与读取顺序。
- `scenarios/playbooks.md`：开发、架构、企业级 SaaS 产品设计、安全审查、性能审查、排障和调研流程，包含预检门、变更门、验证门和报告门等约束触达节点。

## 审查检查

- `checks/index.md`：检查场景入口与读取顺序。
- `checks/checklists.md`：维护、安全、前端设计系统、前端国际化、前端可访问性、前端测试、前端性能、前端 UI 稳定性、企业级 SaaS 设计、前端组件、前端结构与通用性能检查清单。

## 安装态共享规则

- `shared/interactive-decision-protocol.md`：关键决策的原生问询、选项设计和降级规则；仅保留本 Skill 所需内容的安装态投影。
- `shared/target-workspace-layout.md`：目标仓统一产物目录、兼容路径和真值源规则。
- 这两个文件是随 Skill 安装的运行时资产；源码仓根级 `references/` 是跨技能编辑真值源，使用 `scripts/check-template-sync.py` 检查精确副本或当前 Skill 专用投影同步。
