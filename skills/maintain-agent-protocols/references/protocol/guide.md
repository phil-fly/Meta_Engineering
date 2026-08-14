# AI Agent 协作协议指南

创建或维护用户级、项目级 AI Agent 协作协议时使用本参考。协议文件负责入口和边界，工程路由与场景手册负责执行细节。目标仓统一产物目录和新旧路径兼容规则见 `../shared/target-workspace-layout.md`。

## 协议层级

| 层级 | 目的 | 常见文件 | 适合放置 | 避免放置 |
| --- | --- | --- | --- | --- |
| 用户级 | 跨项目生效的默认协作规则 | `AGENTS.md`、`ai-agent-workspace/protocols/user/AGENTS.md`、兼容 `ai-agent-protocols/user/AGENTS.md` | 协作风格、指令优先级、任务分类、入口路由、长期原则 | 命令、步骤、检查清单、语言细节、项目约束 |
| 项目级 | 仓库专属约束和执行要求 | `AGENTS.md`、`CLAUDE.md`、`ai-agent-workspace/protocols/project/AGENTS.md`、兼容 `ai-agent-protocols/project/AGENTS.md`、既有 `CODEX.md` 兼容入口 | 架构、命令、测试、编码约定、发布、业务边界 | 个人偏好、全局哲学、跨项目长流程、生成过程证据 |
| 工程路由 | 按功能类型承载执行细节 | `ai-agent-workspace/protocols/routes/*.md`，兼容 `ai-agent-protocols/routes/*.md` | UI、JavaScript/TypeScript、Go、Java、Rust、Python、API、安全、性能等规则 | 用户协议入口、项目私有例外 |
| 场景手册 | 某类任务的执行方法 | `ai-agent-workspace/protocols/playbooks/*.md`，兼容 `ai-agent-protocols/playbooks/*.md` | 开发、架构、安全审查、性能审查、排障、调研流程 | 稳定项目事实、全局优先级 |
| 检查清单 | 审查和验收项 | `ai-agent-workspace/protocols/checks/*.md`，兼容 `ai-agent-protocols/checks/*.md` | 维护、安全、性能检查项 | 入口路由、项目实施细节 |
| 本地临时 | 短期任务约定 | 线程备注、任务计划、Issue 评论 | 一次性范围决策、实验说明 | 长期标准，除非审查后正式提升 |

## 指令优先级

除非当前环境提供更严格的层级，否则使用以下默认优先级：

```text
P0 用户当前明确要求
P1 安全限制与系统约束
P2 项目级协议
P3 用户级协议
P4 工程路由与场景手册
P5 默认 AI 行为
```

如果两条规则冲突，保留高优先级规则，并修改、移动或删除低优先级规则。不确定时，先明确标注冲突，不要静默选择。

## 创建流程

`WF-PROTOCOL-CREATE`：创建或维护协议入口、协议包和工程路由时，默认按以下流程推进。

1. 明确目标：用户级协议、项目级协议、工程路由、场景手册，或完整协议包。
2. 收集已有规则：用户请求、仓库文档、现有协议文件、命令、测试要求和反复出现的问题。
3. 盘点已有入口：根级 `AGENTS.md`、`CODEX.md`、`CLAUDE.md`、根级 `playbooks/`、既有 `ai-agent-protocols/`、OpenSpec 或其他项目协议。
4. 若用户未明确指定入口文件，先按模型入口判据识别当前模型或工具环境并选择默认入口：Codex/OpenAI 场景使用 `AGENTS.md`，Claude/Anthropic 场景使用 `CLAUDE.md`，无法识别时使用 `AGENTS.md`。
5. 先输出生成方案预览，声明唯一生效入口、各资产真值源、生成模式、拟生成文件、路径变量映射和项目事实证据表。
6. 在预览中补充触发稳定性检查：工作流、条件适用路由、项目约束、约束门禁和检查项映射是否存在明显断链；需要强化 playbooks 或 routes 时列为确认项。
7. 用户确认后再写入文件；不要同时生成两套可编辑正文。
8. 在用户仓库中创建或维护统一协议目录；新项目默认 `ai-agent-workspace/protocols/`，旧项目已有 `ai-agent-protocols/` 时可继续作为真值源。
9. 默认使用项目版生成模式，按目标仓证据裁剪工程路由；最小版和完整版只在用户选择或明确语义匹配时使用。
10. 用户协议只写入口和原则，不写执行细节。
11. 工程路由写执行细节，并按功能类型互相引用。
12. 检查重复、歧义、冲突、遗漏、占位符、触发链路断点和意外约束。

## 生效入口与真值源

落盘前必须先做入口决策：

- `CON-PROTOCOL-ENTRY-PROJECT-SINGLE-SOURCE`：项目协议只能有一个生效正文。若根级 `AGENTS.md` 生效，`ai-agent-protocols/project/AGENTS.md` 只写定位、读取顺序和维护说明；反之亦然。
- `CON-PROTOCOL-ENTRY-USER-SINGLE-SOURCE`：用户协议只能有一个生效正文。若根级用户协议已存在，应优先保持现有入口，不在协议包内复制全文；若既有入口与当前模型官方入口冲突，应在预览中说明迁移或兼容方案。
- `CON-PROTOCOL-ENTRY-SELECTION-ORDER`：模型入口选择顺序为用户明确要求 > 当前模型或工具环境 > 既有协议入口 > 默认 `AGENTS.md`。
- `CON-PROTOCOL-ENTRY-EVIDENCE`：模型入口判据优先使用当前运行环境或模型标识；其次看用户请求是否点名 Codex/OpenAI 或 Claude/Anthropic；再次看根级既有入口文件；仍无法判断时使用 `AGENTS.md`。预览中必须说明使用了哪条判据。
- `CON-PROTOCOL-ENTRY-CODEX`：Codex/OpenAI 场景默认生成或维护 `AGENTS.md`；禁止在用户未明确要求时为 Codex 新建 `codex.md` 或 `CODEX.md`。
- `CON-PROTOCOL-ENTRY-CLAUDE`：Claude/Anthropic 场景默认生成或维护 `CLAUDE.md`；若同时存在 `AGENTS.md`，必须声明两者的真值源关系。
- `CON-PROTOCOL-ENTRY-CODEX-LEGACY`：`CODEX.md` 或 `codex.md` 只作为既有历史文件的兼容、迁移或显式用户要求对象；新建前必须说明原因。
- `CON-PROTOCOL-PLAYBOOK-SINGLE-SOURCE`：场景手册只能有一个可编辑正文目录。若目标仓已有根级 `playbooks/`，默认继承它作为真值源；除非用户明确要求迁移，否则不要把同一正文复制到 `ai-agent-protocols/playbooks/`。
- `CON-PROTOCOL-ENTRY-ALIAS-ONLY`：若必须同时保留两个入口，其中一个应是别名、索引或跳转说明，不承载完整流程正文。
- `CON-PROTOCOL-ENTRY-REPORT`：生成或维护后，最终回复应说明本次选择的生效入口和真值源，以及哪些旧入口被保留为兼容入口。
- `CON-PROTOCOL-ENTRY-PRUNING`：生效用户协议中的工程路由和检查入口只能列出实际生成、目标仓既有存在或已生成兼容入口的路径；未采用入口留在生成报告，不写入生效协议。

路径规则：

- `CON-PROTOCOL-PATH-BASE`：每个入口文件应明确路径口径，使用仓库根相对路径或当前文件相对路径。
- `CON-PROTOCOL-PATH-NESTED`：嵌套目录中的文件引用根级文件时，应使用可解析路径，例如 `../../AGENTS.md`，或明确标注 `仓库根：AGENTS.md`。
- `CON-PROTOCOL-PATH-NO-BARE-NESTED`：禁止在嵌套文件中写无法判断基准目录的裸路径，例如只写 `AGENTS.md`、`CODEX.md` 或 `playbooks/<task>.md`。
- `CON-PROTOCOL-PATH-ABSTRACT-MAPPING`：用户协议使用 `@playbooks`、`@routes`、`@checks` 等抽象入口时，必须在同一文件或协议包入口说明中声明映射；如果目标仓实际落盘到 `ai-agent-protocols/playbooks` 等目录，应自动写明映射或生成根级兼容入口。
- `CON-PROTOCOL-PATH-CANONICAL-ENTRY`：生效用户协议中的任务分类、场景手册、工程路由和检查入口应写展开后的真实路径；路径变量只作为映射说明，不作为任务执行时的最终读取路径。
- `CON-PROTOCOL-PATH-NO-GUESS`：读取 `@playbooks/coding.md` 等抽象入口前必须先查路径变量表；禁止把它自行猜测为根级 `playbooks/coding.md`，除非路径变量明确声明根级 `playbooks/` 是真值源。
- `CON-PROTOCOL-PATH-ALIAS-CONTENT`：兼容入口只承载跳转和真值源说明，不复制完整正文。

## 落盘触发边界

`CON-PROTOCOL-MATERIALIZATION-EXPLICIT`：使用本技能不会自动创建目录或文件。只有用户明确要求创建、补齐、落盘或维护目标仓协议包时，才写入 `ai-agent-workspace/protocols/`、兼容 `ai-agent-protocols/` 或相关入口文件。

目标仓协议包的文件清单、内容来源和最小生成范围见 `package-blueprint.md`。如果只是解释协议设计、回答目录来源或审查现有规则，应先输出结论，不自动落盘。

`CON-PROTOCOL-MATERIALIZATION-PREVIEW`：即使用户要求生成协议包，也应先进入生成方案预览，不直接落盘完整协议包。预览确认后再执行文件创建或修改。

## 仓库目录分层

`CON-PROTOCOL-DIR-NAME`：使用本技能在新用户仓库中落盘协议时，默认目录为 `ai-agent-workspace/protocols`。如果目标仓已采用 `ai-agent-protocols`，应先说明兼容关系并可继续维护旧目录作为真值源，不要同时生成两套可编辑正文。

`CON-PROTOCOL-DIR-PROJECT-MODE`：默认结构为项目版，基础目录保持稳定，`routes/` 只生成目标仓证据支持的领域。完整版结构用于用户明确要求完整覆盖时。

```text
ai-agent-workspace/
└── protocols/
    ├── README.md
    ├── user/
    │   └── AGENTS.md
    ├── project/
    │   └── AGENTS.md
    ├── routes/
    │   ├── index.md
    │   ├── frontend/
    │   ├── backend/
    │   ├── core/
    │   ├── security/
    │   ├── performance/
    │   ├── platform/
    │   └── governance/
    ├── playbooks/
    ├── checks/
    └── templates/
```

推荐职责：

- `README.md`：说明目录职责、入口策略、与目标仓统一产物目录的映射和维护边界。
- `user/`：用户级入口协议，只放定位、优先级、任务路由、长期原则。
- `project/`：项目级协议或模板，可包含项目命令和项目约束。
- `routes/`：按工程功能承载执行细节，是规则细节的主要落点；前端、后端、安全、性能等应目录级隔离。项目版只生成已验证或条件适用的领域，完整版才生成全路由。
- `playbooks/`：按任务类型承载流程方法。
- `checks/`：承载审查和验收检查项。
- `templates/`：承载可复用协议模板。

生成模式：

- 最小版：只生成根协议或协议包入口、必要 playbooks、checks 和 templates；如果入口没有引用 routes，不主动生成工程路由。
- 项目版：默认模式；基于 `package.json`、前端源码、`go.mod`、Maven/Gradle、`Cargo.toml`、`pyproject.toml`、`requirements.txt`、Makefile、README、OpenSpec 或现有目录证据裁剪到文件级工程路由。
- 完整版：仅用户明确要求时使用；包含 UI、JavaScript/TypeScript、Go、Java、Rust、Python、通用安全、通用性能、平台和治理等完整路由，并在生成报告中标注哪些路由没有目标仓证据。

项目版路由索引必须标注路由状态：

```text
项目证据支持  → 当前仓库证据证明适用
条件适用      → 任务触发时适用，不作为常驻项目事实
通用治理      → 协议维护、证据范围、Agent 边界或生成报告相关
```

路由索引只列项目版实际生成的路由；未生成的完整路由应留在生成报告的“未采用路由”中，不放进生效入口。

## 用户协议入口规则

用户协议禁止包含执行细节。以下内容视为执行细节，必须下沉到目标仓统一协议目录：

- 具体命令、脚本、工具调用方式。
- 多步骤实施流程。
- 详细检查清单。
- 大段模板、示例输出或代码片段。
- 某类任务的完整方法论。
- 语言、框架、仓库或项目专属约束。

用户协议应只保留：

- 协议定位。
- 指令优先级。
- 任务分类。
- 工程路由、场景手册和检查清单入口。
- 通用原则摘要。
- 维护边界和变更原则。

工作流、约束和检查项的长期引用必须编号：

```text
工作流  → WF-*
约束    → CON-*
检查项  → CHK-*
```

编号必须在同一真值源内唯一；生成、移动、拆分、合并或弃用编号时，应同步引用并写入生成报告或维护记录。

## 用户级协议模板

技能内可复用模板见 `user-protocol-template.md`。

- 可复制模板资产：`../../templates/user-protocol.md`。
- 维护模板正文时，必须同步更新 `user-protocol-template.md` 与 `../../templates/user-protocol.md`，避免目标仓落盘内容漂移。
- 目标仓建议落盘位置：`ai-agent-workspace/protocols/templates/user-protocol.md`，旧项目可兼容 `ai-agent-protocols/templates/user-protocol.md`。
- 实际生效时，可按目标仓约定复制到根 `AGENTS.md` 或 `ai-agent-workspace/protocols/user/AGENTS.md`；旧项目可兼容 `ai-agent-protocols/user/AGENTS.md`。

## 项目级协议模板

技能内可复用模板见 `project-protocol-template.md`。

- 可复制模板资产：`../../templates/project-protocol.md`。
- 维护模板正文时，必须同步更新 `project-protocol-template.md` 与 `../../templates/project-protocol.md`，避免目标仓落盘内容漂移。
- 项目级模板中的约束信息应写成结构化记录，至少包含 `约束名称`、`适用范围`、`生效条件`、`流程节点`、`门禁动作`、`规则正文`、`验证方式` 和 `报告要求`，不要只留标签词。
- 项目级协议可以记录长期有效的项目事实和项目约束，但不要保留“已验证项目事实来源”、读取文件清单或生成过程证据；这些内容应进入生成报告、任务日志、Issue 或 PR 描述。
- 项目级协议中的硬性规范词必须有目标仓证据支撑；证据不足的候选约束只能写成待确认、建议或条件规则。
- OpenSpec、风险控制、规范同步、审查闭环等高频规则应优先用锚点式入口引用；如果详情章节已经展开，结构化约束中只保留锚点和项目差异，不重复全文。
- 会影响任务触发稳定性的项目级约束，应写明生效条件、流程节点、门禁动作和验证方式；高风险或高频约束应能通过场景手册门禁节点、工程路由或检查项短路径触达。
- 目标仓建议落盘位置：`ai-agent-workspace/protocols/templates/project-protocol.md`，旧项目可兼容 `ai-agent-protocols/templates/project-protocol.md`。
- 实际生效时，应按模型入口规则复制到根 `AGENTS.md`、`CLAUDE.md` 或 `ai-agent-workspace/protocols/project/AGENTS.md`；`CODEX.md` 仅用于既有历史入口兼容、迁移或用户明确要求，旧项目可兼容 `ai-agent-protocols/project/AGENTS.md`。

## 路由卡片模板

技能内可复用模板见 `route-card-template.md`。

- 可复制模板资产：`../../templates/route-card.md`。
- 维护路由卡片模板时，必须同步更新 `route-card-template.md` 与 `../../templates/route-card.md`，避免目标仓落盘内容漂移。
- 目标仓建议落盘位置：`ai-agent-workspace/protocols/templates/route-card.md`，旧项目可兼容 `ai-agent-protocols/templates/route-card.md`。
- 新增工程路由时，可按该模板创建具体 `routes/**.md` 文件，再补充领域规则正文。

## 维护检查清单

审查或编辑已有协议文件时，使用 `../checks/checklists.md` 的 `maintenance-checklist` 作为唯一检查项正文。本文件只保留维护入口，避免与检查清单真值源重复。

## 冲突处理模式

规则重复时：

- 保留最高层级的长期规则。
- 在用户协议中只保留入口，不重复执行细节。
- 项目特有例外保留在项目级文件。

规则冲突时：

- 指出具体冲突句子。
- 应用指令优先级。
- 将低优先级规则改为例外、更窄范围，或删除。
- 最终回复说明处理方式。

规则归属错误时：

- 个人偏好移动到用户级协议。
- 用户协议中的执行步骤下沉到 `routes/`、`playbooks/`、`checks/` 或 `templates/`。
- 仓库命令或架构细节移动到项目级协议。
- 语言、框架、工程域细节移动到对应工程路由。
- 任务流程移动到场景手册。
- 审查项移动到检查清单。
- 生成或审计来源清单移动到生成报告、Issue、PR 描述或任务日志。
- 一次性任务约束保留在线程或 Issue，不写入长期文件。

## 内容边界

- 技能内规则应自包含，不要求读取外部仓库才能理解。
- 技能维护按技能创建流程处理，不走项目规格变更流程。
- 长期知识库或 Wiki 更新前必须征求用户确认。
