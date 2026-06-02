---
name: maintain-agent-protocols
description: "创建、审查、重构和维护 AI Agent 协作协议与规则路由。Use for Protocol Engineer reviews, rule ingestion, principle/constraint/workflow ingestion, Spec-first workflow routing, trigger-entry decisions, maintenance-location decisions, AGENTS.md/CODEX.md/CLAUDE.md, ai-agent-protocols directory design, user/project protocol templates, route-based engineering rules, execution-rate analysis, token-cost analysis, conflict reduction, UI/Go/Java/Rust/API/auth/data/security/performance/platform/observability route design, and AI coding workflow agreements. Do not use for ordinary feature implementation, normal code review, general architecture discussion, external specification repository governance, service onboarding to external specs, or project debugging unless the user is creating, reviewing, restructuring, or maintaining agent collaboration protocols or rule routing."
---

# Maintain Agent Protocols

## 概览

使用本技能创建和维护 AI Agent 协作协议，使规则清晰分层、入口稳定、执行细节可按需加载。

技能维护本身按技能创建流程处理，不需要项目规格变更流程。`SKILL.md` 只保留触发、流程和引用导航；执行细节必须下沉到 `references/` 分层文件。

## 技能内部分层

按任务场景读取以下目录，不要默认全量加载。需要总览时先读 `references/index.md`。

- `references/protocol/`：协议生成与维护场景，包含层级、目标仓目录结构、入口模板和冲突处理。
- `references/engineering/`：工程规则路由场景；前端、后端、安全、性能、平台、治理必须用目录隔离。
- `references/scenarios/`：任务流程场景，覆盖开发、架构、安全审查、性能审查、排障和调研。
- `references/checks/`：审查检查场景，覆盖维护、安全与性能检查清单。
- `templates/`：可复制到目标仓 `ai-agent-protocols/templates/` 的模板资产；维护模板正文时必须同步 `user-protocol-template.md`、`project-protocol-template.md` 和 `route-card-template.md`。
- `scripts/`：技能维护验证脚本；当前用于检查模板资产与协议模板参考是否同步。

## 工作流

1. 识别请求类型。
   - `创建`：起草新的用户级协议、项目级协议或完整 `ai-agent-protocols/` 协议包。
   - `维护`：更新、合并、拆分或重构已有规则。
   - `审查`：检查规则是否存在遗漏、歧义、冲突、范围缺失或过期约束。
   - `转换`：把零散说明、口头约定或草稿转成结构化协议和路由文件。
   - `协议工程`：从执行率、复杂度、冲突、Token 成本和长期维护性审查协议体系。
   - `规则摄入`：判断原则、约束、执行流程、模板、检查项和知识应维护在哪里，是否作为触发入口。
   - 仅当用户明确要求创建、落盘、补齐或维护目标仓协议包时，才创建目录和文件；读取或触发技能本身不会自动生成任何文件。

2. 判断目标层级。
   - `用户级`：长期有效的个人协作偏好、默认任务路由、全局安全边界、回复风格、跨项目原则。
   - `项目级`：仓库专属架构、命令、测试要求、编码约定、发布流程、业务领域约束。
   - `工程路由`：UI、Go、Java、Rust、API、安全、性能等功能类型的执行细节入口。
   - `场景手册`：开发、架构、安全审查、性能审查、排障、调研等任务方法。
   - `临时规则`：短期本地约定，除非变成可复用规则，否则不要沉淀为长期协议。

3. 编辑前先收集上下文。
   - 优先检查 `AGENTS.md`、`CODEX.md`、`CLAUDE.md`、`.cursor/rules`、`.github/copilot-instructions.md`、`ai-agent-protocols/**/*.md`、历史 `playbooks/*.md`、项目文档和用户当前指令。
   - 保留历史决策和项目术语，除非它们已经明确过期或冲突。
   - 审查类任务必须说明检查范围、未检查范围和结论适用范围。

4. 应用协议设计规则。
   - 读取 `references/protocol/index.md`，再按场景读取 `references/protocol/guide.md`。
   - 涉及协议工程审查、执行率、Token 成本、协议膨胀或冲突分析时，读取 `references/protocol/protocol-engineer.md`。
   - 涉及原则摄入、约束摄入、执行流程摄入或触发入口判断时，读取 `references/protocol/rule-ingestion.md`。
   - 涉及 OpenSpec、Spec-first、规范驱动开发、审查修复闭环或 Epic/Subtask 拆分时，读取 `references/protocol/openspec-workflow.md`。
   - 涉及完整协议包落盘、模板目录、playbooks 内容来源或目标仓文件生成时，读取 `references/protocol/package-blueprint.md`。
   - 涉及本技能自身目录结构、`templates/` 目录或结构校验 warning 处理时，读取 `references/protocol/skill-structure.md`。
   - 需要工程规则细节时先读取 `references/engineering/index.md`，再进入对应领域目录读取路由文件。
   - 区分“入口”和“执行细节”：用户协议定义路由，工程路由和场景手册定义执行细节。
   - 在用户仓库落盘时，必须创建或维护 `ai-agent-protocols/`，并按功能类型做好入口分层。
   - 用户协议中禁止写执行细节；用户协议只保留执行细节入口。
   - 默认采用完整路由覆盖，至少包含 UI、Go、Java、Rust、通用安全、通用性能和通用质量入口。
   - 默认采用最小修改，避免大范围重写。

5. 闭环。
   - 创建类任务：给出生成的文件或补丁，并说明建议保存位置。
   - 维护类任务：把每个发现归类为已解决、延后处理、明确排除或转入后续任务。
   - 高风险治理变更：编辑前说明影响和验证方式。
   - 除非用户或项目协议明确要求，不自动提交。

## 行为准则

以下规则在整个会话期间有效，不因对话长度而放松：

1. ❗ 用户协议只保留入口和长期原则，执行细节必须下沉到 `references/` 或目标仓 `ai-agent-protocols/`；每次修改前自检。
2. ❗ 新增规则必须先按原则、约束、执行流程、模板、检查项、知识或临时约定分类，再决定维护位置；每次输出前自检。
3. ❗ 审查和优化结论必须说明范围、证据和剩余风险；每次输出前自检。

## 工具优先级

| 操作 | 首选工具 | 降级条件 | 降级工具 |
| --- | --- | --- | --- |
| 查找文件 | `rg --files` / `find` | 首选命令不可用 | `ls` |
| 搜索规则 | `rg` | `rg` 不可用 | `grep` |
| 修改文件 | `apply_patch` | patch 无法唯一匹配 | 缩小上下文后重试 |
| 验证技能 | `skill-craft` 验证脚本 + `scripts/check-template-sync.py` | 脚本缺失、不可运行或连续 2 次失败 | 手动引用检查 |

- 单次失败不等于工具不可用；先重试或缩小范围，连续 2 次同类失败后才降级。
- 降级时说明原因。

## 依赖链

- Step 2 的目标层级判断必须继承 Step 1 的请求类型，不能重新猜测任务。
- Step 4 的参考文件选择必须继承 Step 2 的目标层级和 Step 3 的上下文证据。
- Step 5 的闭环分类必须覆盖本轮所有发现；已解决、延后处理、明确排除、转入后续任务的数量之和应等于发现总数。
- 写入或修改协议前，先核对规则类型、维护位置、触发入口和反证检查是否一致。
- 修改模板正文后，必须验证 `templates/` 与 `references/protocol/` 下对应模板参考文件同步；自动脚本不可用时执行手动 `cmp` 检查。

## 输出约束

禁止输出：

- 未标明来源的强结论。
- 把普通工程建议包装成协议规则。
- 把低频细则写进用户级入口。
- 大段复述模板全文，除非用户明确要求。

维护协议时，最终回复应包含变更范围、验证结果和剩余风险。

## 幻觉防护

所有审查、迁移、冲突和触发判断必须引用具体文件、章节或工具结果；无来源的结论只能标注为待确认。

| 场景 | 正确输出 | 禁止输出 |
| --- | --- | --- |
| 未找到项目协议 | 说明未发现并限制结论范围 | 编造项目约束 |
| 未读取工程路由 | 标注未检查对应工程细节 | 断言规则完整 |
| 规则归属不确定 | 标注候选位置并说明需要确认 | 直接移动为长期规则 |

标注分级：

- 已验证：来自已读文件或工具输出。
- 待确认：证据不足但有合理候选。
- 通用建议：不作为项目事实或强约束。

## 输出要求

写协议时：

- 默认使用中文；仅在技能名、文件名、工具名、命令、英文触发词或既有项目语言需要时保留英文。
- 使用简短稳定的章节名和术语。
- 规范词保持一致：`必须`、`应`、`默认`、`避免`、`禁止`、`仅当`。
- 用户协议只写定位、优先级、任务分类、入口路由和通用原则；不要写具体执行步骤、命令、清单或长模板。
- 执行细节必须写入 `ai-agent-protocols/` 下方功能子目录，例如 `routes/`、`playbooks/`、`checks/`、`templates/`。
- 不要保留外部仓库路径、来源痕迹或外部规格依赖；规则应成为技能内自包含内容。
- 不要把重要约束藏在示例里。

维护规则时：

- 保留无关内容和原有格式。
- 用最小修改消除歧义或冲突。
- 移动规则时说明它为什么属于用户级、项目级、工程路由、场景手册或临时规则。
- 更新长期知识库或 Wiki 前先征求用户确认。
