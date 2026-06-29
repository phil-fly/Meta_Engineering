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
识别任务类型 → 读取对应入口 → 检查约束触发项 → 按入口推进并闭环
```

当一个任务跨越多个类型时：

- 选择一个主类型作为主流程。
- 补充必要的工程路由、场景手册或检查入口。
- 对命中的高频或高风险 `CON-*`，在对应场景手册的预检门、变更门、验证门或报告门中处理。
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
@protocols  = ai-agent-workspace/protocols
@playbooks  = ai-agent-workspace/protocols/playbooks
@routes     = ai-agent-workspace/protocols/routes
@checks     = ai-agent-workspace/protocols/checks
```

若目标仓已有根级 `playbooks/`、`ai-agent-protocols/playbooks/` 或其他目录并选择继续作为真值源，应把 `@playbooks` 改为已确认的真实路径，不要同时复制一套可编辑正文。

`CON-PATH-VARIABLE-RESOLVE`：读取任何 `@playbooks`、`@routes` 或 `@checks` 引用前，必须先按本表递归展开到真实仓库路径；禁止把 `@playbooks/coding.md` 自行猜测为根级 `playbooks/coding.md`。

`CON-PATH-CANONICAL-ENTRIES`：生成生效协议时，下方“场景手册”“工程路由”和“检查入口”必须写展开后的真实路径；`@...` 变量只保留在本节作为映射说明，不作为任务执行时的最终读取路径。

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
WF-CODING              → ai-agent-workspace/protocols/playbooks/coding.md
WF-ARCHITECTURE        → ai-agent-workspace/protocols/playbooks/architecture.md
WF-SECURITY-REVIEW     → ai-agent-workspace/protocols/playbooks/security-review.md
WF-PERFORMANCE-REVIEW  → ai-agent-workspace/protocols/playbooks/performance-review.md
WF-TROUBLESHOOTING     → ai-agent-workspace/protocols/playbooks/troubleshooting.md
WF-RESEARCH            → ai-agent-workspace/protocols/playbooks/research.md
```

场景手册只提供执行方法，不替代用户当前要求、系统安全限制或项目级规范。

场景手册应通过门禁节点触达约束：

```text
预检门  → 判断任务命中的 CON-*、风险等级和需要补读的路由
变更门  → 限制实施行为，例如规范同步、最小修改和高风险确认
验证门  → 要求测试、检查、证据或替代验证说明
报告门  → 汇报命中的关键约束、验证结果、未覆盖范围和剩余风险
```

用户级协议不复制约束执行细节；高频或高风险约束应在对应场景手册或工程路由中保留短引用。

## 工程路由

用户级协议只保留大类入口。具体语言、框架、API、鉴权、数据访问、日志、部署等细项，应在对应子目录索引中继续路由。

生成生效协议时，本节只能保留本次实际生成、目标仓既有存在或已生成兼容入口的路径；未采用的路由必须从生效协议中移除，并写入生成报告。

```text
前端开发      → ai-agent-workspace/protocols/routes/frontend/index.md
后端开发      → ai-agent-workspace/protocols/routes/backend/index.md
核心工程      → ai-agent-workspace/protocols/routes/core/index.md
安全工程      → ai-agent-workspace/protocols/routes/security/index.md
性能工程      → ai-agent-workspace/protocols/routes/performance/index.md
平台工程      → ai-agent-workspace/protocols/routes/platform/index.md
Agent 治理    → ai-agent-workspace/protocols/routes/governance/index.md
```

常见组合入口：

```text
后端 coding    → ai-agent-workspace/protocols/routes/backend/index.md + ai-agent-workspace/protocols/routes/core/index.md；涉及风险时补 ai-agent-workspace/protocols/routes/security/index.md 或 ai-agent-workspace/protocols/routes/performance/index.md
前端开发       → ai-agent-workspace/protocols/routes/frontend/index.md；涉及接口、权限或高影响操作时补 ai-agent-workspace/protocols/routes/core/index.md 或 ai-agent-workspace/protocols/routes/security/index.md
WF-SECURITY-REVIEW     → ai-agent-workspace/protocols/playbooks/security-review.md + ai-agent-workspace/protocols/routes/security/index.md；涉及语言实现时补对应工程真实路径
WF-PERFORMANCE-REVIEW  → ai-agent-workspace/protocols/playbooks/performance-review.md + ai-agent-workspace/protocols/routes/performance/index.md；涉及数据访问或可观测性时补 ai-agent-workspace/protocols/routes/core/index.md 或 ai-agent-workspace/protocols/routes/platform/index.md
WF-ARCHITECTURE        → ai-agent-workspace/protocols/playbooks/architecture.md + 相关工程真实路径
```

## 检查入口

```text
CHK-MAINT-*  规则维护       → ai-agent-workspace/protocols/checks/maintenance-checklist.md
CHK-SEC-*    安全检查       → ai-agent-workspace/protocols/checks/security-checklist.md
CHK-PERF-*   性能检查       → ai-agent-workspace/protocols/checks/performance-checklist.md
```

## 通用原则

以下原则只表达长期取舍，不承载具体步骤、命令或检查清单。执行细节下沉到已确认的场景手册真实路径，工程约束下沉到已确认的工程路由真实路径，验收项下沉到已确认的检查清单真实路径。

| 原则 | 适用判断 | 维护边界 |
| --- | --- | --- |
| 任务优先 | 先满足用户当前明确要求，再处理长期优化。 | 不把低优先级优化包装成当前任务必需项。 |
| 证据驱动 | 审查、评估、巡检、调研类结论必须说明检查范围、未检查范围和适用范围。 | 不把局部证据包装成全局结论。 |
| CON-SPEC-SYNC | 涉及 API、数据结构、配置、权限模型或系统架构时，先确认项目规范是否需要同步。 | 用户协议不承载项目业务规范正文。 |
| CON-MINIMAL-CHANGE | 默认局部修改，避免无关重构、重命名、目录调整和格式化。 | 修复什么，修改什么。 |
| CON-RISK-LEVEL | 认证、授权、数据迁移、删除和安全控制逻辑等高风险变更，需要先说明影响和验证方式。 | 具体执行步骤放入场景手册或项目协议。 |
| CON-NATIVE-ASK | 协议生成、调整、入口迁移、真值源选择或高风险治理变更需要用户确认时，若当前 Agent App 支持原生确认/问询机制，应优先使用。 | 不支持原生机制时退化为普通文本问询；一次默认不超过 3 个关键问题。 |
| 经验优先 | 优先继承项目规范、历史决策、Wiki、设计文档和既有代码模式。 | 不在缺少背景时推翻既有设计。 |
| CON-REVIEW-CLOSURE | 发现的问题必须归类为已解决、延后处理、明确排除或转入后续任务。 | 禁止问题无故消失。 |
| CON-KNOWLEDGE-CAPTURE | 只沉淀可复用经验、通用设计模式、架构决策和长期有效规则。 | 一次性问题、临时方案、环境异常和偶发故障不沉淀为长期规则。 |
| CON-GIT-SCOPE | 默认不自动提交；仅用户或项目协议明确要求时提交。 | 提交范围仅包含当前任务相关内容。 |
