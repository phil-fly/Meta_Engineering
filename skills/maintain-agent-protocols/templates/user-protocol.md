## AGENTS.md instructions for <scope>

## 定位

本文件是用户级 AI Agent 协作协议。

本模板可以保留占位符；复制为生效用户协议前，必须删除或替换所有 `<...>` 占位符，证据不足的入口写为待确认或暂不引用。

它负责说明：

- 任务应如何分类
- 每类任务应遵循什么主流程
- 需要读取哪个工程路由、场景手册或检查入口
- 哪些通用原则必须始终遵守

分层原则：

```text
用户协议说明入口和边界。
工程路由与场景手册说明怎么做。
项目规范说明具体约束。
```

## 优先级

```text
P0 用户当前明确要求
P1 安全限制与系统约束
P2 项目级协议
P3 本协议
P4 ai-agent-protocols/ 下方工程路由、场景手册与检查清单
P5 默认 AI 行为
```

若上层指令与下层入口冲突，以上层为准。

## 使用方式

开始任务前先完成三步：

```text
识别任务类型 → 读取对应入口 → 按入口推进并闭环
```

当一个任务跨越多个类型时：

- 选择一个主类型作为主流程。
- 补充必要的工程路由、场景手册或检查入口。
- 在回复中说明本次采用的主流程和辅助入口。

## 编号规则

以下编号用于管理和引用长期工作流、约束和检查项：

```text
WF-*   → 工作流和执行流程
CON-*  → 约束和边界规则
CHK-*  → 检查项和验收项
```

新增、移动或重命名工作流、约束和检查项时，必须保持编号唯一并同步所有引用。

## 路径变量

本协议内使用以下路径变量减少重复。读取时先按本表展开，不要自行改写目录名。

```text
@protocols  = ai-agent-protocols
@playbooks  = <已选场景手册真值源，默认 @protocols/playbooks>
@routes     = @protocols/routes
@checks     = @protocols/checks
```

若目标仓已有根级 `playbooks/` 并选择继续作为真值源，应把 `@playbooks` 改为 `playbooks` 或项目约定的根级路径，不要同时复制一套 `ai-agent-protocols/playbooks/` 正文。

若使用 `@playbooks`、`@routes` 或 `@checks` 等抽象入口，生成协议时必须保证它们能解析到真实文件；当真实文件落在 `ai-agent-protocols/` 下方时，应在本表写明映射，或生成根级兼容入口指向真值源。

## 任务分类

```text
WF-CODING              开发任务      → 规范 → 变更 → 验证 → 审查
WF-ARCHITECTURE        架构设计      → 需求 → 设计 → 权衡 → 建议
WF-SECURITY-REVIEW     安全审查      → 信息收集 → 分析 → 缓解 → 验证
WF-PERFORMANCE-REVIEW  性能审查      → 目标 → 路径 → 瓶颈 → 优化 → 验证
WF-TROUBLESHOOTING     故障排查      → 证据 → 假设 → 验证 → 根因
WF-RESEARCH            技术调研      → 问题 → 证据 → 对比 → 结论
```

## 场景手册

```text
WF-CODING              → @playbooks/coding.md
WF-ARCHITECTURE        → @playbooks/architecture.md
WF-SECURITY-REVIEW     → @playbooks/security-review.md
WF-PERFORMANCE-REVIEW  → @playbooks/performance-review.md
WF-TROUBLESHOOTING     → @playbooks/troubleshooting.md
WF-RESEARCH            → @playbooks/research.md
```

场景手册只提供执行方法，不替代用户当前要求、系统安全限制或项目级规范。

## 工程路由

用户级协议只保留大类入口。具体语言、框架、API、鉴权、数据访问、日志、部署等细项，应在对应子目录索引中继续路由。

生成生效协议时，本节只能保留本次实际生成、目标仓既有存在或已生成兼容入口的路径；未采用的路由必须从生效协议中移除，并写入生成报告。

```text
前端开发      → @routes/frontend/index.md
后端开发      → @routes/backend/index.md
核心工程      → @routes/core/index.md
安全工程      → @routes/security/index.md
性能工程      → @routes/performance/index.md
平台工程      → @routes/platform/index.md
Agent 治理    → @routes/governance/index.md
```

常见组合入口：

```text
后端 coding    → 后端开发入口 + 核心工程入口；涉及风险时补安全工程或性能工程入口
前端开发       → 前端开发入口；涉及接口、权限或高影响操作时补核心工程或安全工程入口
WF-SECURITY-REVIEW     → 场景手册的安全审查入口 + 安全工程入口；涉及语言实现时补对应工程入口
WF-PERFORMANCE-REVIEW  → 场景手册的性能审查入口 + 性能工程入口；涉及数据访问或可观测性时补核心工程或平台工程入口
WF-ARCHITECTURE        → 场景手册的架构入口 + 相关工程大类入口
```

## 检查入口

```text
CHK-MAINT-*  规则维护       → @checks/maintenance-checklist.md
CHK-SEC-*    安全检查       → @checks/security-checklist.md
CHK-PERF-*   性能检查       → @checks/performance-checklist.md
```

## 通用原则

以下原则只表达长期取舍，不承载具体步骤、命令或检查清单。执行细节下沉到 `@playbooks`，工程约束下沉到 `@routes`，验收项下沉到 `@checks`。

| 原则 | 适用判断 | 维护边界 |
| --- | --- | --- |
| 任务优先 | 先满足用户当前明确要求，再处理长期优化。 | 不把低优先级优化包装成当前任务必需项。 |
| 证据驱动 | 审查、评估、巡检、调研类结论必须说明检查范围、未检查范围和适用范围。 | 不把局部证据包装成全局结论。 |
| CON-SPEC-SYNC | 涉及 API、数据结构、配置、权限模型或系统架构时，先确认项目规范是否需要同步。 | 用户协议不承载项目业务规范正文。 |
| CON-MINIMAL-CHANGE | 默认局部修改，避免无关重构、重命名、目录调整和格式化。 | 修复什么，修改什么。 |
| CON-RISK-LEVEL | 认证、授权、数据迁移、删除和安全控制逻辑等高风险变更，需要先说明影响和验证方式。 | 具体执行步骤放入场景手册或项目协议。 |
| 经验优先 | 优先继承项目规范、历史决策、Wiki、设计文档和既有代码模式。 | 不在缺少背景时推翻既有设计。 |
| CON-REVIEW-CLOSURE | 发现的问题必须归类为已解决、延后处理、明确排除或转入后续任务。 | 禁止问题无故消失。 |
| CON-KNOWLEDGE-CAPTURE | 只沉淀可复用经验、通用设计模式、架构决策和长期有效规则。 | 一次性问题、临时方案、环境异常和偶发故障不沉淀为长期规则。 |
| CON-GIT-SCOPE | 默认不自动提交；仅用户或项目协议明确要求时提交。 | 提交范围仅包含当前任务相关内容。 |
