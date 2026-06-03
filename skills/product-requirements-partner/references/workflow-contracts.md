# Workflow Contracts

## 协作强度

| 模式 | 触发 | 行为 |
| --- | --- | --- |
| 轻量讨论 | brainstorm、快速判断、局部问题、暂不落盘 | 直接讨论，不初始化 `docs/` |
| 产物沉淀 | 用户要求写文件、生成 PRD、立项、设计说明、mockup、调研报告 | 先确认目标文件或建议目录 |
| 项目记忆模式 | 长期项目、多轮协作、用户要求记住决策，或已存在 `ai-agent-workspace/product/memory/` / `docs/00_MEMORY/` | 读取项目记忆并按阈值写入 |

## Scene Contract

| Scene | 最小输入 | 标准输出 | 可写文件 | 不可写条件 |
| --- | --- | --- | --- | --- |
| 价值发现 | 想法、痛点或目标用户线索 | 价值锚点、目标用户、痛点、替代方案、待确认项 | `ai-agent-workspace/product/memory/`、`ai-agent-workspace/product/strategy/`，兼容 `docs/00_MEMORY/`、`docs/01_STRATEGY/` | 用户仍在自由讲述且未确认方向 |
| 流程与范围 | 已确认价值锚点或核心痛点 | 关键用户旅程、MVP 支持/延后范围 | `ai-agent-workspace/product/prd/framework-prd.md`、`ai-agent-workspace/product/memory/TODO.md`，兼容 `docs/02_PRD/`、`docs/TODO.md` | 痛点未闭环或范围仍明显发散 |
| 交互结构 | 核心旅程和 MVP 边界 | Screen Tree、信息层级、主操作 | Framework PRD 或 `ai-agent-workspace/product/design/ui_ux/`，兼容 `docs/03_DESIGN/ui_ux/` | 旅程还未稳定 |
| 实体定义 | 页面结构和关键操作 | 实体清单、状态机、操作矩阵、字段行为 | Framework PRD 或 Feature PRD | 页面结构尚未成形 |
| 设计与交付 | 交互结构、实体状态、设计方向 | 设计指导、mockup、handoff note | `ai-agent-workspace/product/design/`，兼容 `docs/03_DESIGN/` | 待定项影响页面结构或实体逻辑 |
| PRD 评审 | PRD 文本或文件路径 | blocker、clarification、suggestion、可执行性判断 | 原 PRD 或新版本 PRD | 未读目标文档或用户只要求口头反馈 |
| 竞品调研 | 目标问题、市场/用户范围 | 替代方案矩阵、证据、启发与不采纳项 | `ai-agent-workspace/product/resources/`，兼容 `docs/04_RESOURCES/` | 无联网能力且用户未提供资料 |

## Scene Steps

### Scene 1 · 价值发现

做法：

1. 先让用户自由讲述，不用长清单过早框住思路。
2. 追问真实故事、目标用户、约束、替代方案和不可忍受的摩擦。
3. 提炼一个可观察的价值锚点，例如时间、成本、步骤、风险、心理负担或业务指标变化。
4. 有具体故事或硬约束时，追加到产品记忆目录的 `CONTEXT_SNAPSHOT.md`。
5. 价值、范围、目标用户逐步清楚后，维护产品策略目录里的立项类文档。

退出条件：至少一个价值锚点被用户确认。

### Scene 2 · 流程与范围

做法：

1. 从痛点出发写 3-5 条关键用户旅程。
2. 先画理想端到端流程，再切 MVP。
3. MVP 用“支持哪些旅程”定义，不用孤立功能清单定义。
4. 每个核心旅程都记录 `{入口场景} -> {可见信息} -> {用户动作} -> {结果}`。
5. 写入或更新产品 PRD 目录的 `framework-prd.md` 或项目约定的 Framework PRD。

退出条件：痛点覆盖关系和 MVP 延后项都被明确记录。

### Scene 3 · 交互结构

做法：

1. 定义 Screen Tree、信息层级、主操作和关键入口。
2. 把 Scene 2 的旅程映射到页面结构。
3. 以目标用户视角走查：是否看得懂、知道下一步、能回到上下文。
4. 发现冲突时调整页面结构并记录重要设计转向。

退出条件：核心旅程在页面结构中都有明确落点。

### Scene 4 · 实体定义

做法：

1. 从业务流和页面结构抽象实体，不先写数据库 schema。
2. 对关键实体按状态机处理：状态含义、可见性、可编辑性、正向/反向/跳跃转移、每状态操作、字段行为。
3. 用实体模型回查页面结构，发现缺字段、假关系、无 UI 状态或无实体承载的动作时及时调整。

退出条件：用户流、前端页面、后端逻辑三层都能对齐。

### Scene 5 · 设计与交付

做法：

1. 设计产物默认放在产品设计目录，生产代码只在设计确认后再改。
2. 高保真前先写设计指导文档，标记并解释 `[待定项-XXX]`。
3. mockup 使用自包含 HTML；确认后补充 handoff note。
4. 视觉与交付细节按 `references/design-artifacts.md` 和 `references/design-handoff.md` 执行。

退出条件：设计稿、待定项、交付说明和后续开发入口清楚。

## `[Meta]` 层级示例

| 用户输入 | 默认层级 | 目标 |
| --- | --- | --- |
| `[Meta] 以后价值发现先让我自由讲 5 分钟` | Layer 0 | 本技能的 Scene 1 提问方式 |
| `[Meta] 我个人喜欢先看反例再看方案` | Layer 1 | 用户个人偏好，需确认维护位置 |
| `[Meta] 这个项目所有 PRD 都用中文标题` | Layer 2 | 当前项目 `docs/` 或项目协议 |
| `[Meta0] 把竞品调研变成默认步骤` | Layer 0 候选 | 需评估是否所有产品讨论都适用 |
| `[Meta1] 我不想自动写 DECISIONS` | Layer 1 候选 | 需确认是个人偏好还是本技能规则 |
| `[Meta] 这次先不要写文件` | 当前任务约束 | 只影响本轮协作，不沉淀 |

## 闭环状态

审查、调研或需求整理产生的问题必须归入以下状态之一：

- 已解决
- 延后处理
- 明确排除
- 转入后续任务

不要让发现项在后续编辑或总结中消失。
