# 目标仓协议包蓝图

本文件说明使用本技能在目标仓落盘 `ai-agent-protocols/` 时，应创建哪些文件、文件内容从哪里来，以及哪些行为不会自动发生。

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

预览必须包含：

- 生效入口：项目协议、用户协议、场景手册、工程路由、检查清单和模板分别选择哪个真值源。
- 模型入口判断：说明用户是否明确指定入口；未指定时说明当前模型或工具环境如何推断，以及为什么选择 `AGENTS.md`、`CLAUDE.md` 或既有兼容入口。
- 生成模式：最小版、项目版或完整版；默认选择项目版。
- 拟生成文件：列出将创建或修改的路径，标明新建、最小修改、别名或跳过。
- 路径变量映射：若用户协议使用 `@playbooks`、`@routes` 或 `@checks`，必须说明它们映射到目标仓哪些真实目录。
- 编号方案：说明本次工作流 `WF-*`、约束 `CON-*`、检查项 `CHK-*` 的编号范围、继承来源和冲突处理。
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

技能内 `templates/` 目录提供可直接复制到目标仓 `ai-agent-protocols/templates/` 的模板资产；`references/protocol/user-protocol-template.md`、`references/protocol/project-protocol-template.md` 和 `references/protocol/route-card-template.md` 是模板正文的解释性来源，维护时应保持两者同步。

落盘前先确定目标仓真值源：

```text
项目协议正文    → 根级 AGENTS.md / CLAUDE.md / ai-agent-protocols/project/AGENTS.md（三选一；按模型入口规则）
用户协议正文    → 根级 AGENTS.md / CLAUDE.md / ai-agent-protocols/user/AGENTS.md（三选一；按模型入口规则）
场景手册正文    → 根级 playbooks/ 或 ai-agent-protocols/playbooks/（二选一）
工程路由正文    → ai-agent-protocols/routes/
检查清单正文    → ai-agent-protocols/checks/
模板资产正文    → ai-agent-protocols/templates/
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

`CON-PACKAGE-PLAYBOOK-SINGLE-SOURCE`：若目标仓已有根级 `playbooks/` 且内容应继续生效，默认不要再生成同内容的 `ai-agent-protocols/playbooks/*.md`；需要协议包内入口时，只写索引或别名说明，指向根级真值源。若用户明确要求迁移到 `ai-agent-protocols/playbooks/`，应先说明迁移影响，并避免保留两套可编辑正文。

## 入口兼容与别名

当生效用户协议使用 `@playbooks`、`@routes`、`@checks` 等抽象入口时，目标仓必须满足以下任一条件，避免首次读取失败：

- 在用户协议的“路径变量”中声明真实映射，例如 `@playbooks = ai-agent-protocols/playbooks`。
- 在协议包 README 或入口说明中声明同一映射，并确保用户协议引用该说明。
- 生成兼容入口，例如根级 `playbooks/README.md` 指向 `ai-agent-protocols/playbooks/`，或根级 `playbooks/<task>.md` 作为别名文件指向协议包内真值源。

兼容入口规则：

- `CON-PACKAGE-ALIAS-LIGHTWEIGHT`：兼容入口只写跳转、映射和真值源说明，不复制完整正文。
- `CON-PACKAGE-ALIAS-RESOLVABLE`：如果用户协议引用 `@playbooks/coding.md`，生成后必须能解析到真实文件或别名文件。
- `CON-PACKAGE-ALIAS-NO-COMPAT`：如果选择不生成兼容入口，必须在生成报告中说明原因，并把用户协议中的路径变量改成真实目录。
- `CON-PACKAGE-ALIAS-REPORT`：生成报告应列出抽象入口、真实路径、兼容入口和验证结果。

```text
ai-agent-protocols/README.md
  → references/protocol/guide.md 的目录职责、入口策略和维护边界

ai-agent-protocols/user/AGENTS.md
  → 仅当用户协议正文真值源选在协议包内时，来自 references/protocol/user-protocol-template.md；否则只写根级用户协议入口说明

ai-agent-protocols/project/AGENTS.md
  → 仅当项目协议正文真值源选在协议包内时，来自 references/protocol/project-protocol-template.md；否则只写根级项目协议入口说明

ai-agent-protocols/routes/**
  → 项目版按粒度选择目标仓证据支持的 references/engineering/** 对应目录和文件；完整版才复制完整路由覆盖

ai-agent-protocols/playbooks/*.md
  → 仅当场景手册正文真值源选在协议包内时，来自 references/scenarios/playbooks.md 中同名场景章节；否则只写根级手册别名或索引

ai-agent-protocols/checks/*.md
  → references/checks/checklists.md 中同名检查清单章节

ai-agent-protocols/templates/user-protocol.md
  → templates/user-protocol.md

ai-agent-protocols/templates/project-protocol.md
  → templates/project-protocol.md

ai-agent-protocols/templates/route-card.md
  → templates/route-card.md
```

## 生成规则

- `CON-PACKAGE-GENERATE-MINIMAL-EDIT`：目标仓已有同名文件时，先读取并做最小修改，不覆盖用户内容。
- `CON-PACKAGE-GENERATE-SKELETON`：目标仓没有同名文件时，按蓝图创建骨架并填充可执行内容。
- `CON-PACKAGE-GENERATE-PROJECT-MODE`：默认生成模式是项目版；除非用户明确要求完整版，不生成目标仓未采用的语言、框架或平台路由。
- `CON-PACKAGE-GENERATE-ENTRY-PRUNING`：生成用户协议时，工程路由和检查入口只列本次实际生成、目标仓既有存在或已生成兼容入口的路径；未采用路由只写入生成报告。
- `CON-PACKAGE-GENERATE-FILE-LEVEL`：项目版必须支持文件级路由粒度；不要因为发现一个后端证据就生成全部后端语言路由。
- `CON-PACKAGE-GENERATE-PLAYBOOK-SPLIT`：若 `ai-agent-protocols/playbooks/` 被选为场景手册真值源，`playbooks/*.md` 应拆分为独立文件，每个文件只包含一个任务流程。
- `CON-PACKAGE-GENERATE-ROOT-PLAYBOOK`：若根级 `playbooks/` 被选为场景手册真值源，协议包内不要复制同名正文；可创建 `ai-agent-protocols/playbooks/README.md` 或单文件别名说明，指向根级手册。
- `CON-PACKAGE-GENERATE-TEMPLATE-SCOPE`：`templates/*.md` 只放可复用格式骨架、填写规则和可实例化的通用协议条款，不承载目标仓专属决策或一次性任务约定。
- `CON-PACKAGE-GENERATE-EVIDENCE-REPORT-ONLY`：从目标仓扫描得到的读取文件清单、事实来源、置信度标注和生成过程记录只在生成报告中说明，不写入落盘协议正文、协议包 `README.md` 或入口说明。
- `CON-PACKAGE-GENERATE-NO-PLACEHOLDER`：生效协议、协议包 `README.md` 和入口说明不得保留 `<project>`、`<install-command>`、`<path>` 等模板占位符；证据不足时删除该项或写为待确认，不把占位符交给后续 Agent 猜测。
- `CON-PACKAGE-GENERATE-TEMPLATE-SYNC`：修改技能内模板正文时，应同步更新 `templates/` 与 `references/protocol/` 下对应模板参考文件。
- `CON-PACKAGE-GENERATE-ROUTE-LAYERING`：`routes/**` 应保留领域分层，避免把所有工程规则压成单个大文件。
- `CON-PACKAGE-GENERATE-CHECKS-SCOPE`：`checks/*.md` 只放检查项，不放长流程或教程。
- `CON-PACKAGE-GENERATE-DIR-DIFFERENCE`：如果目标仓已经采用不同目录名，应先说明差异并征求确认；默认目录名是 `ai-agent-protocols`。
- `CON-PACKAGE-GENERATE-PATH-BASE`：每个生成文件的路径引用必须统一口径。协议包内文件引用根级文件时，使用 `../`、`../../` 等当前文件相对路径，或明确写 `仓库根：<path>`；不要写基准不明的裸路径。

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
ai-agent-protocols/
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

如果目标仓已有根级 `playbooks/` 并选择继续作为真值源，最小协议包中的 `ai-agent-protocols/playbooks/` 可改为只包含 `README.md` 或别名文件，不复制根级手册正文。

## 闭环检查

落盘后必须检查：

- CHK-MAINT-001 用户协议中的每个入口路径是否存在。
- CHK-MAINT-002 `@playbooks`、`@routes`、`@checks` 等抽象入口是否有真实路径映射或兼容入口。
- CHK-MAINT-003 用户协议是否只列实际生成、既有存在或已兼容的工程路由和检查入口。
- CHK-MAINT-004 生成模式是否符合用户确认；默认项目版是否没有无证据语言/框架路由。
- CHK-MAINT-005 工作流、约束和检查项是否分别使用 `WF-*`、`CON-*`、`CHK-*` 编号，且同一真值源内唯一。
- CHK-MAINT-006 路由索引是否按 `项目证据支持`、`条件适用`、`通用治理` 标注。
- CHK-MAINT-007 工作区状态是否清楚；如存在未跟踪文件或无关修改，应在生成报告中说明但不擅自处理。
- CHK-MAINT-008 `playbooks/` 中是否覆盖用户协议声明的任务分类。
- CHK-MAINT-009 `templates/` 中是否有用户级、项目级和路由卡片模板。
- CHK-MAINT-010 `checks/` 中是否有维护、安全和性能检查清单。
- CHK-MAINT-011 是否误把项目专属命令、业务规则或一次性约定写入通用模板。
- CHK-MAINT-012 是否误把生成过程证据、读取文件清单或“已验证项目事实来源”写入协议正文。
- CHK-MAINT-013 是否误把生成依据写入 `ai-agent-protocols/README.md`、`project/AGENTS.md` 或其他入口说明。
- CHK-MAINT-014 生效协议、协议包 README 和入口说明是否仍残留 `<...>` 模板占位符。
- CHK-MAINT-015 Codex 场景是否默认选择 `AGENTS.md`，且未新建 `codex.md` 或 `CODEX.md`。
- CHK-MAINT-016 Claude 场景是否默认选择 `CLAUDE.md`，且与 `AGENTS.md` 或既有入口的真值源关系清楚。
- CHK-MAINT-017 项目级 `必须`、`禁止`、`默认` 或 `仅当` 是否都有目标仓证据支撑。
- CHK-MAINT-018 OpenSpec、风险控制等高频规则是否只保留入口锚点，避免结构化约束和详情章节重复展开。
- CHK-MAINT-019 是否存在根级 `playbooks/` 与 `ai-agent-protocols/playbooks/` 的同内容全文双写；若存在，应明确一个为真值源，另一个改为索引或别名。
- CHK-MAINT-020 嵌套入口文件中的 `AGENTS.md`、`CODEX.md`、`playbooks/`、`routes/`、`checks/` 路径是否按当前文件位置可解析。

生成报告应与生效协议分离，至少包含：

- 本次生成模式和确认依据。
- 模型入口判断依据，以及最终生效入口文件。
- 编号清单：新增、继承、弃用或迁移的 `WF-*`、`CON-*`、`CHK-*`。
- 创建、修改、跳过的文件清单。
- 项目事实证据表和待确认项。
- 抽象入口映射和兼容入口验证结果。
- 占位符处理结果。
- 无关技术栈路由检查结果。
- 路由索引三类标注结果。
- 重复展开压缩结果。
- 使用者下一步，例如确认入口文件名、审阅待确认事实、删除未采用路由或在 `git add` 前复查生成报告。
