# 目标仓协议包蓝图

本文件说明使用本技能在目标仓落盘协议包时，应创建哪些文件、文件内容从哪里来，以及哪些行为不会自动发生。新项目默认协议包路径为 `ai-agent-workspace/protocols/`；目标仓已存在 `ai-agent-protocols/` 时可兼容继承。跨技能统一布局见 `../shared/target-workspace-layout.md`。

## 触发边界

`CON-PACKAGE-TRIGGER-NO-AUTO-CREATE`：技能被读取或命中触发词时，不自动创建目录或文件。

仅当用户明确提出以下意图时，才在目标仓落盘或修改协议包：

- 创建协议包。
- 补齐协议目录。
- 生成模板目录。
- 生成或维护 `playbooks/`、`routes/`、`checks/`、`templates/`。
- 把当前协议入口引用的文件补齐。

`CON-PACKAGE-TRIGGER-EXPLAIN-ONLY`：如果用户只是在询问规则、设计或差异，应先解释，不落盘。

## 生成方案预览

`WF-PACKAGE-PREVIEW`：落盘前必须先给用户一份生成方案预览，并等待确认。预览只说明计划，不创建文件。

可执行工具链：

- `scripts/protocol-package.py detect <target-repo>`：把目标仓入口、协议目录和技术栈证据输出为 JSON。
- `scripts/protocol-package.py plan <target-repo> --mode minimal|project|full`：按 `scripts/protocol-package-manifest.json` 生成拟落盘文件、路由裁剪和检查清单计划。
- `scripts/protocol-package.py scaffold <target-repo> --mode minimal|project|full`：按计划写入协议包；默认跳过既有文件，只有显式 `--overwrite` 才覆盖。
- `scripts/protocol-package.py validate <target-repo>`：检查根级生效入口及其本地 Markdown 引用、协议包目录、模板资产、`WF-*`/`CHK-*` 核心内容、路由索引状态标注和占位符泄漏。

脚本输出用于生成方案预览和生成报告，不替代用户确认。`scaffold` 不自动维护根级生效入口，因此执行者完成入口维护前，`validate` 应返回失败；这表示协议包尚未生效，不是可忽略 warning。

预览必须包含：

- 生效入口：项目协议、用户协议、场景手册、工程路由、检查清单和模板分别选择哪个真值源。
- 问询方式：说明本轮是否使用当前 Agent App 的原生确认/问询机制；若未使用，说明是环境不可用还是无需确认。
- 模型入口判断：说明用户是否明确指定入口；未指定时说明当前模型或工具环境如何推断，以及为什么选择 `AGENTS.md`、`CLAUDE.md` 或既有兼容入口。
- 生成模式：最小版、项目版或完整版；默认选择项目版。
- 拟生成文件：列出将创建或修改的路径，标明新建、最小修改、别名或跳过。
- 路径变量映射：若用户协议使用 `@playbooks`、`@routes` 或 `@checks`，必须说明它们映射到目标仓哪些真实目录。
- 编号方案：说明本次工作流 `WF-*`、约束 `CON-*`、检查项 `CHK-*` 的编号范围、继承来源和冲突处理。
- 触发稳定性检查：说明工作流、条件适用路由、项目级约束和检查项映射是否存在明显断链；若未检查，说明原因。
- 约束门禁检查：说明高频或高风险 `CON-*` 是否绑定到相关 `WF-*` 的预检门、变更门、验证门或报告门；若未绑定，说明是延后处理、低频项目事实还是待确认候选。
- 项目事实证据表：每条项目事实、技术栈、命令、目录职责或规范入口都要标注来源文件；没有证据时标为待确认。
- 模板内容边界：说明哪些内容来自通用模板，哪些内容来自目标仓证据。
- 风险与确认点：列出会影响长期协议、入口迁移、双写、无关路由或占位符处理的事项。

项目事实证据表建议格式：

```text
事实/约束 | 状态 | 来源 | 写入位置 | 规范词
语言/框架 | 已验证/待确认 | go.mod / package.json / README / 待确认 | project/AGENTS.md / routes/... | 必须/应/建议/如项目采用...
```

状态规则：

- `CON-PACKAGE-FACT-VERIFIED`：已验证状态必须来自本轮已读取的目标仓文件或工具输出。
- `CON-PACKAGE-FACT-PENDING`：待确认状态表示证据不足但用户表达或目录形态提供合理候选。
- `CON-PACKAGE-FACT-TEMPLATE`：通用模板来自本技能模板，不作为项目事实。

规范词规则：

- `CON-PACKAGE-NORM-VERIFIED`：已验证且长期适用的项目事实可写成 `必须`、`禁止`、`默认` 或 `仅当`。
- `CON-PACKAGE-NORM-PENDING`：待确认、跨项目通用或架构未启用的内容只能写成 `应`、`建议` 或 `如项目采用...`。
- `CON-PACKAGE-NORM-NO-EVIDENCE`：如果无法找到证据，不得把候选技术栈、命令、目录职责或路由写成项目级硬约束。

## 内容来源

`CON-PACKAGE-CONTENT-SOURCE`：目标仓文件应从技能内 `references/` 派生，不要凭空编写，也不要复制外部仓库路径。

技能内 `templates/` 目录提供可直接复制到目标仓协议模板目录的模板资产；新项目默认 `ai-agent-workspace/protocols/templates/`，旧项目兼容 `ai-agent-protocols/templates/`。`references/protocol/user-protocol-template.md`、`references/protocol/project-protocol-template.md` 和 `references/protocol/route-card-template.md` 是模板正文的解释性来源，维护时应保持两者同步。

落盘前先确定目标仓真值源：

```text
项目协议正文    → 根级 AGENTS.md / CLAUDE.md / ai-agent-workspace/protocols/project/AGENTS.md / 兼容 ai-agent-protocols/project/AGENTS.md（四选一；按模型入口规则）
用户协议正文    → 根级 AGENTS.md / CLAUDE.md / ai-agent-workspace/protocols/user/AGENTS.md / 兼容 ai-agent-protocols/user/AGENTS.md（四选一；按模型入口规则）
场景手册正文    → 根级 playbooks/ / ai-agent-workspace/protocols/playbooks/ / 兼容 ai-agent-protocols/playbooks/（三选一）
工程路由正文    → ai-agent-workspace/protocols/routes/，兼容 ai-agent-protocols/routes/
检查清单正文    → ai-agent-workspace/protocols/checks/，兼容 ai-agent-protocols/checks/
模板资产正文    → ai-agent-workspace/protocols/templates/，兼容 ai-agent-protocols/templates/
生成过程证据    → 生成报告 / 任务日志 / Issue / PR 描述
```

模型入口规则：

- `CON-PACKAGE-ENTRY-USER-SPECIFIED`：用户明确指定入口文件时，按用户当前要求执行。
- `CON-PACKAGE-ENTRY-MODEL-AWARE`：用户未指定时，必须主动判断当前模型或工具环境；Codex/OpenAI 场景默认生成或维护 `AGENTS.md`，Claude/Anthropic 场景默认生成或维护 `CLAUDE.md`。
- `CON-PACKAGE-ENTRY-FALLBACK`：无法识别模型或工具环境时，默认使用 `AGENTS.md`。
- `CON-PACKAGE-ENTRY-CODEX-LEGACY`：`CODEX.md` 或 `codex.md` 只作为既有历史文件的兼容、迁移或显式用户要求对象；不得在 Codex 场景默认新建。
- `CON-PACKAGE-ENTRY-MIGRATION`：若既有入口与模型默认入口不同，预览中必须说明保留、迁移或别名策略，并确保只有一个可编辑真值源。

编号规则：

- `CON-PACKAGE-ID-WORKFLOW`：工作流和执行流程使用 `WF-*`。
- `CON-PACKAGE-ID-CONSTRAINT`：约束和边界规则使用 `CON-*`。
- `CON-PACKAGE-ID-CHECK`：检查项和验收项使用 `CHK-*`。
- `CON-PACKAGE-ID-INHERIT`：目标仓已有编号时继承既有编号，不为同一规则创建新编号。
- `CON-PACKAGE-ID-UNIQUE`：新增编号前必须扫描同一真值源，避免同类型编号冲突。
- `CON-PACKAGE-ID-REPORT`：生成报告必须列出新增、继承、弃用或迁移的编号。

`CON-PACKAGE-PLAYBOOK-SINGLE-SOURCE`：若目标仓已有根级 `playbooks/` 且内容应继续生效，默认不要再生成同内容的协议包 `playbooks/*.md`；需要协议包内入口时，只写索引或别名说明，指向根级真值源。若用户明确要求迁移到统一协议目录，应先说明迁移影响，并避免保留两套可编辑正文。

## 入口兼容与别名

当生效用户协议使用 `@playbooks`、`@routes`、`@checks` 等抽象入口时，目标仓必须满足以下任一条件，避免首次读取失败：

- 在用户协议的“路径变量”中声明真实映射，例如 `@playbooks = ai-agent-workspace/protocols/playbooks`。
- 在协议包 README 或入口说明中声明同一映射，并确保用户协议引用该说明。
- 生成兼容入口，例如根级 `playbooks/README.md` 指向 `ai-agent-workspace/protocols/playbooks/` 或兼容协议目录，或根级 `playbooks/<task>.md` 作为别名文件指向协议包内真值源。

兼容入口规则：

- `CON-PACKAGE-ALIAS-LIGHTWEIGHT`：兼容入口只写跳转、映射和真值源说明，不复制完整正文。
- `CON-PACKAGE-ALIAS-RESOLVABLE`：如果用户协议引用 `@playbooks/coding.md`，生成后必须能解析到真实文件或别名文件。
- `CON-PACKAGE-ALIAS-CANONICAL-ENTRY`：生成生效用户协议时，任务分类、场景手册、工程路由和检查入口必须写展开后的真实路径；`@playbooks`、`@routes` 和 `@checks` 只保留在路径变量表或入口说明中。
- `CON-PACKAGE-ALIAS-NO-GUESS`：不得要求后续模型把 `@playbooks/coding.md` 自行解释为某个目录；若真实真值源是根级 `playbooks/`，必须在路径变量表中显式写 `@playbooks = playbooks`。
- `CON-PACKAGE-ALIAS-NO-COMPAT`：如果选择不生成兼容入口，必须在生成报告中说明原因，并把用户协议中的路径变量改成真实目录。
- `CON-PACKAGE-ALIAS-REPORT`：生成报告应列出抽象入口、真实路径、兼容入口和验证结果。

```text
ai-agent-workspace/protocols/README.md
  → references/protocol/guide.md 的目录职责、入口策略和维护边界

ai-agent-workspace/protocols/user/AGENTS.md
  → 仅当用户协议正文真值源选在协议包内时，来自 references/protocol/user-protocol-template.md；否则只写根级用户协议入口说明

ai-agent-workspace/protocols/project/AGENTS.md
  → 仅当项目协议正文真值源选在协议包内时，来自 references/protocol/project-protocol-template.md；否则只写根级项目协议入口说明

ai-agent-workspace/protocols/routes/**
  → 项目版按粒度选择目标仓证据支持的 references/engineering/** 对应目录和文件；完整版才复制完整路由覆盖

ai-agent-workspace/protocols/playbooks/*.md
  → 仅当场景手册正文真值源选在协议包内时，来自 references/scenarios/playbooks.md 中同名场景章节；否则只写根级手册别名或索引

ai-agent-workspace/protocols/checks/*.md
  → references/checks/checklists.md 中同名检查清单章节

ai-agent-workspace/protocols/templates/user-protocol.md
  → templates/user-protocol.md

ai-agent-workspace/protocols/templates/project-protocol.md
  → templates/project-protocol.md

ai-agent-workspace/protocols/templates/route-card.md
  → templates/route-card.md
```

目标仓已采用 `ai-agent-protocols/` 时，可把上述路径整体映射到兼容目录；映射必须写入入口说明或生成报告，且不得同时保留两套可编辑正文。

## 生成规则

- `CON-PACKAGE-GENERATE-MINIMAL-EDIT`：目标仓已有同名文件时，先读取并做最小修改，不覆盖用户内容。
- `CON-PACKAGE-GENERATE-NATIVE-ASK`：生成或调整协议需要用户确认时，若当前 Agent App 支持原生确认、结构化问询或弹出式问题，应优先使用原生机制；不可用时退化为普通文本问询。
- `CON-PACKAGE-GENERATE-SKELETON`：目标仓没有同名文件时，按蓝图创建骨架并填充可执行内容。
- `CON-PACKAGE-GENERATE-PROJECT-MODE`：默认生成模式是项目版；除非用户明确要求完整版，不生成目标仓未采用的语言、框架或平台路由。
- `CON-PACKAGE-GENERATE-ENTRY-PRUNING`：生成用户协议时，场景手册、工程路由和检查入口只列本次实际生成、目标仓既有存在或已生成兼容入口的真实路径；未采用路由只写入生成报告。
- `CON-PACKAGE-GENERATE-FILE-LEVEL`：项目版必须支持文件级路由粒度；不要因为发现一个后端证据就生成全部后端语言路由。
- `CON-PACKAGE-GENERATE-PLAYBOOK-SPLIT`：若协议包 `playbooks/` 被选为场景手册真值源，`playbooks/*.md` 应拆分为独立文件，每个文件只包含一个任务流程。
- `CON-PACKAGE-GENERATE-ROOT-PLAYBOOK`：若根级 `playbooks/` 被选为场景手册真值源，协议包内不要复制同名正文；可创建协议包内 `playbooks/README.md` 或单文件别名说明，指向根级手册。
- `CON-PACKAGE-GENERATE-TEMPLATE-SCOPE`：`templates/*.md` 只放可复用格式骨架、填写规则和可实例化的通用协议条款，不承载目标仓专属决策或一次性任务约定。
- `CON-PACKAGE-GENERATE-EVIDENCE-REPORT-ONLY`：从目标仓扫描得到的读取文件清单、事实来源、置信度标注和生成过程记录只在生成报告中说明，不写入落盘协议正文、协议包 `README.md` 或入口说明。
- `CON-PACKAGE-GENERATE-NO-PLACEHOLDER`：生效协议、协议包 `README.md` 和入口说明不得保留 `<project>`、`<install-command>`、`<path>` 等模板占位符；证据不足时删除该项或写为待确认，不把占位符交给后续 Agent 猜测。
- `CON-PACKAGE-GENERATE-TEMPLATE-SYNC`：修改技能内模板正文时，应同步更新 `templates/` 与 `references/protocol/` 下对应模板参考文件。
- `CON-PACKAGE-GENERATE-ROUTE-LAYERING`：`routes/**` 应保留领域分层，避免把所有工程规则压成单个大文件。
- `CON-PACKAGE-GENERATE-CHECKS-SCOPE`：`checks/*.md` 只放检查项，不放长流程或教程。
- `CON-PACKAGE-GENERATE-DIR-DIFFERENCE`：如果目标仓已经采用不同目录名，应先说明差异并征求确认；新项目默认目录是 `ai-agent-workspace/protocols`，旧项目可兼容 `ai-agent-protocols`。
- `CON-PACKAGE-GENERATE-PATH-BASE`：每个生成文件的路径引用必须统一口径。协议包内文件引用根级文件时，使用 `../`、`../../` 等当前文件相对路径，或明确写 `仓库根：<path>`；不要写基准不明的裸路径。

## 触发链路规则

生成或升级协议包时，按 `trigger-stability-guide.md` 做轻量触发链路检查。检查结果进入预览或报告，不写入生效协议正文。

- `CON-PACKAGE-TRIGGER-STABILITY-CHECK`：创建、升级同步或协议工程审查时，应检查任务入口、场景手册、工程路由、项目级约束和检查项之间是否存在明显断链。
- `CON-PACKAGE-TRIGGER-WF-GATE`：创建、升级同步或协议工程审查时，应检查高频和高风险约束是否被相关场景手册门禁节点触达；只在项目协议中孤立出现的关键约束应列为断链或延后强化项。
- `CON-PACKAGE-TRIGGER-STABILITY-NO-ENGINE`：除非另有脚本实现，不声称已运行自动验证引擎；结论应标注来自已读文件、`rg` 搜索结果或待确认推断。
- `CON-PACKAGE-TRIGGER-STABILITY-PREVIEW`：升级同步时若建议强化 playbooks、routes 或 checks，必须在升级预览中列出拟修改文件和强化原因，并让用户选择“只同步规则”或“同步规则 + 强化触发链路”。
- `CON-PACKAGE-TRIGGER-STABILITY-GENERATE`：新建协议包时，可以把通用触发条件直接写入新生成的 playbooks 或 routes/index；仍需保持短引用，不复制完整约束正文。
- `CON-PACKAGE-TRIGGER-STABILITY-REPORT`：生成报告应说明高/中/低稳定触发结论、不能稳定触发的约束或路由、已强化项、未强化项和剩余风险。

## 三档生成模式

```text
最小版  → 根协议或协议包入口 + 必要 playbooks/checks/templates；不主动生成工程 routes，除非入口已引用。
项目版  → 默认模式；基于目标仓证据裁剪 routes，只生成当前技术栈、目录和任务类型需要的文件级入口。
完整版  → 用户明确要求时使用；包含 UI、JavaScript/TypeScript、Go、Java、Rust、Python、核心工程、安全、性能、平台和治理等完整路由。
```

项目版裁剪规则：

- 发现 `package.json`、前端构建配置或前端源码时，可生成 `routes/frontend/index.md` 和 `routes/frontend/javascript-typescript.md`；只有发现列表、远程搜索、提交型表单、Design Token、紧凑布局、权限渲染、导航状态等证据时，才生成对应细分路由。
- 发现 `go.mod` 时，可生成 Go 后端路由；发现 Maven/Gradle 文件时，可生成 Java 路由；发现 `Cargo.toml` 时，可生成 Rust 路由；发现 `pyproject.toml`、`requirements.txt`、`setup.py`、`Pipfile` 或 Python 服务源码时，可生成 Python 路由；未发现的语言路由不生成。
- 发现 API、数据库、鉴权、日志、配置或服务目录证据时，可生成对应 `routes/core/` 细分入口；只发现其中一类时，不展开其他无证据细项。
- 通用安全、性能和质量入口可作为条件适用路由生成，但正文必须写明适用触发条件，避免把未启用架构写成项目事实。
- Agent 治理、证据范围、资产一致性等与协议维护相关的内容归为通用治理路由，默认只生成索引或轻量入口。
- 未发现证据的语言和框架路由默认不生成；如果用户需要保留，应在生成报告中标为用户确认的扩展范围。

路由索引标注规则：

- `项目证据支持`：目标仓文件、配置、源码或用户明确说明证明该路由当前适用。
- `条件适用`：当前未证明常驻适用，但任务触发时应读取，例如安全、性能、风险控制。
- `通用治理`：协议维护、证据范围、Agent 边界、生成报告等治理类路由。

项目版 `routes/index.md` 和各子目录索引必须标注以上三类之一；不允许只列路径而不说明适用状态。

条件适用路由还应写明触发条件；高风险或高频条件路由应能从相关 playbook 读到短触发语句。若目标仓已有 playbook 真值源，默认最小修改补充引用；若用户选择只升级规则，不修改 playbook，则在报告中把该项归为延后处理。

锚点式引用规则：

- OpenSpec、风险控制、规范同步、审查闭环等高频规则，只在项目协议保留一个入口锚点。
- 规则正文已经在同一协议章节、场景手册、检查清单或工程路由展开时，不要再作为结构化项目约束重复写一遍。
- 需要强调项目特例时，项目协议只写“项目差异”和“锚点引用”，不复制通用规则全文。

完整版规则：

- 保留完整覆盖能力，但必须在预览中说明会生成与当前仓库无直接证据的通用路由。
- 完整版中的未验证技术栈规则不得写入项目级协议正文；只作为通用路由或模板资产存在。

## 同步验证

维护技能内模板正文后，优先运行：

```bash
python3 scripts/check-template-sync.py
```

该脚本检查以下文件必须完全同步：

```text
templates/user-protocol.md          == references/protocol/user-protocol-template.md
templates/project-protocol.md       == references/protocol/project-protocol-template.md
templates/route-card.md             == references/protocol/route-card-template.md
```

## 最小协议包

当用户要求“补齐可用协议包”但未要求完整工程路由时，至少创建入口、必要场景手册、必要检查项和模板资产；未被入口引用或用户未选择的场景文件不要强行生成：

```text
ai-agent-workspace/
└── protocols/
    ├── README.md
    ├── playbooks/
    │   ├── <必要任务手册>.md
    │   └── README.md
    ├── checks/
    │   ├── <必要检查清单>.md
    │   └── README.md
    └── templates/
        ├── user-protocol.md
        ├── project-protocol.md
        └── route-card.md
```

如用户协议已经引用 `routes/`，还应同步创建对应路由入口文件，避免入口悬空。

如果目标仓已有根级 `playbooks/` 并选择继续作为真值源，最小协议包中的协议 `playbooks/` 目录可改为只包含 `README.md` 或别名文件，不复制根级手册正文。

## 闭环检查

落盘后必须使用 `../checks/checklists.md` 的 `maintenance-checklist` 执行闭环检查。本文件只说明协议包生成场景，不复制检查项正文。

生成报告应与生效协议分离，至少包含：

- 本次生成模式和确认依据。
- 本轮问询方式：原生确认/问询、普通文本问询或无需问询。
- 模型入口判断依据，以及最终生效入口文件。
- 编号清单：新增、继承、弃用或迁移的 `WF-*`、`CON-*`、`CHK-*`。
- 创建、修改、跳过的文件清单。
- 项目事实证据表和待确认项。
- 抽象入口映射和兼容入口验证结果。
- 占位符处理结果。
- 无关技术栈路由检查结果。
- 路由索引三类标注结果。
- 触发稳定性检查结果、强化选择和剩余断链风险。
- 约束门禁绑定结果，以及未绑定约束的处理分类。
- 重复展开压缩结果。
- 使用者下一步，例如确认入口文件名、审阅待确认事实、删除未采用路由或在 `git add` 前复查生成报告。
