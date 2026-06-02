# 目标仓协议包蓝图

本文件说明使用本技能在目标仓落盘 `ai-agent-protocols/` 时，应创建哪些文件、文件内容从哪里来，以及哪些行为不会自动发生。

## 触发边界

技能被读取或命中触发词时，不自动创建目录或文件。

仅当用户明确提出以下意图时，才在目标仓落盘或修改协议包：

- 创建协议包。
- 补齐协议目录。
- 生成模板目录。
- 生成或维护 `playbooks/`、`routes/`、`checks/`、`templates/`。
- 把当前协议入口引用的文件补齐。

如果用户只是在询问规则、设计或差异，应先解释，不落盘。

## 生成方案预览

落盘前必须先给用户一份生成方案预览，并等待确认。预览只说明计划，不创建文件。

预览必须包含：

- 生效入口：项目协议、用户协议、场景手册、工程路由、检查清单和模板分别选择哪个真值源。
- 生成模式：最小版、项目版或完整版；默认选择项目版。
- 拟生成文件：列出将创建或修改的路径，标明新建、最小修改、别名或跳过。
- 项目事实证据表：每条项目事实、技术栈、命令、目录职责或规范入口都要标注来源文件；没有证据时标为待确认。
- 模板内容边界：说明哪些内容来自通用模板，哪些内容来自目标仓证据。
- 风险与确认点：列出会影响长期协议、入口迁移、双写、无关路由或占位符处理的事项。

项目事实证据表建议格式：

```text
事实/约束 | 状态 | 来源 | 写入位置 | 规范词
语言/框架 | 已验证/待确认 | go.mod / package.json / README / 待确认 | project/AGENTS.md / routes/... | 必须/应/建议/如项目采用...
```

状态规则：

- 已验证：来自本轮已读取的目标仓文件或工具输出。
- 待确认：证据不足但用户表达或目录形态提供合理候选。
- 通用模板：来自本技能模板，不作为项目事实。

规范词规则：

- 已验证且长期适用的项目事实可写成 `必须`、`禁止`、`默认` 或 `仅当`。
- 待确认、跨项目通用或架构未启用的内容只能写成 `应`、`建议` 或 `如项目采用...`。
- 如果无法找到证据，不得把候选技术栈、命令、目录职责或路由写成项目级硬约束。

## 内容来源

目标仓文件应从技能内 `references/` 派生，不要凭空编写，也不要复制外部仓库路径。

技能内 `templates/` 目录提供可直接复制到目标仓 `ai-agent-protocols/templates/` 的模板资产；`references/protocol/user-protocol-template.md`、`references/protocol/project-protocol-template.md` 和 `references/protocol/route-card-template.md` 是模板正文的解释性来源，维护时应保持两者同步。

落盘前先确定目标仓真值源：

```text
项目协议正文    → 根级 AGENTS.md 或 ai-agent-protocols/project/AGENTS.md（二选一）
用户协议正文    → 根级 CODEX.md / CLAUDE.md / ai-agent-protocols/user/AGENTS.md（三选一或按项目约定）
场景手册正文    → 根级 playbooks/ 或 ai-agent-protocols/playbooks/（二选一）
工程路由正文    → ai-agent-protocols/routes/
检查清单正文    → ai-agent-protocols/checks/
模板资产正文    → ai-agent-protocols/templates/
生成过程证据    → 生成报告 / 任务日志 / Issue / PR 描述
```

若目标仓已有根级 `playbooks/` 且内容应继续生效，默认不要再生成同内容的 `ai-agent-protocols/playbooks/*.md`；需要协议包内入口时，只写索引或别名说明，指向根级真值源。若用户明确要求迁移到 `ai-agent-protocols/playbooks/`，应先说明迁移影响，并避免保留两套可编辑正文。

```text
ai-agent-protocols/README.md
  → references/protocol/guide.md 的目录职责、入口策略和维护边界

ai-agent-protocols/user/AGENTS.md
  → 仅当用户协议正文真值源选在协议包内时，来自 references/protocol/user-protocol-template.md；否则只写根级用户协议入口说明

ai-agent-protocols/project/AGENTS.md
  → 仅当项目协议正文真值源选在协议包内时，来自 references/protocol/project-protocol-template.md；否则只写根级项目协议入口说明

ai-agent-protocols/routes/**
  → 项目版只选择目标仓证据支持的 references/engineering/** 对应目录和文件；完整版才复制完整路由覆盖

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

- 目标仓已有同名文件时，先读取并做最小修改，不覆盖用户内容。
- 目标仓没有同名文件时，按蓝图创建骨架并填充可执行内容。
- 默认生成模式是项目版；除非用户明确要求完整版，不生成目标仓未采用的语言、框架或平台路由。
- 若 `ai-agent-protocols/playbooks/` 被选为场景手册真值源，`playbooks/*.md` 应拆分为独立文件，每个文件只包含一个任务流程。
- 若根级 `playbooks/` 被选为场景手册真值源，协议包内不要复制同名正文；可创建 `ai-agent-protocols/playbooks/README.md` 或单文件别名说明，指向根级手册。
- `templates/*.md` 只放可复用格式骨架，不承载决策规则或长期原则。
- 从目标仓扫描得到的读取文件清单、事实来源、置信度标注和生成过程记录只在生成报告中说明，不写入落盘协议正文、协议包 `README.md` 或入口说明。
- 生效协议、协议包 `README.md` 和入口说明不得保留 `<project>`、`<install-command>`、`<path>` 等模板占位符；证据不足时删除该项或写为待确认，不把占位符交给后续 Agent 猜测。
- 修改技能内模板正文时，应同步更新 `templates/` 与 `references/protocol/` 下对应模板参考文件。
- `routes/**` 应保留领域分层，避免把所有工程规则压成单个大文件。
- `checks/*.md` 只放检查项，不放长流程或教程。
- 如果目标仓已经采用不同目录名，应先说明差异并征求确认；默认目录名是 `ai-agent-protocols`。
- 每个生成文件的路径引用必须统一口径。协议包内文件引用根级文件时，使用 `../`、`../../` 等当前文件相对路径，或明确写 `仓库根：<path>`；不要写基准不明的裸路径。

## 三档生成模式

```text
最小版  → 根协议或协议包入口 + 必要 playbooks/checks/templates；不主动生成工程 routes，除非入口已引用。
项目版  → 默认模式；基于目标仓证据裁剪 routes，只生成当前技术栈、目录和任务类型需要的入口。
完整版  → 用户明确要求时使用；包含 UI、Go、Java、Rust、核心工程、安全、性能、平台和治理等完整路由。
```

项目版裁剪规则：

- 发现 `package.json`、前端构建配置或前端源码时，可生成 `routes/frontend/`。
- 发现 `go.mod` 时，可生成 Go 后端路由；发现 Maven/Gradle 文件时，可生成 Java 路由；发现 `Cargo.toml` 时，可生成 Rust 路由。
- 发现 API、数据库、鉴权、日志、配置或服务目录证据时，可生成对应 `routes/core/` 入口。
- 通用安全、性能和质量入口可作为条件路由生成，但正文必须写明适用触发条件，避免把未启用架构写成项目事实。
- 未发现证据的语言和框架路由默认不生成；如果用户需要保留，应在生成报告中标为用户确认的扩展范围。

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

当用户要求“补齐可用协议包”但未要求完整工程路由时，至少创建：

```text
ai-agent-protocols/
├── README.md
├── playbooks/
│   ├── coding.md
│   ├── architecture.md
│   ├── security-review.md
│   ├── performance-review.md
│   ├── troubleshooting.md
│   └── research.md
├── checks/
│   ├── maintenance-checklist.md
│   ├── security-checklist.md
│   └── performance-checklist.md
└── templates/
    ├── user-protocol.md
    ├── project-protocol.md
    └── route-card.md
```

如用户协议已经引用 `routes/`，还应同步创建对应路由入口文件，避免入口悬空。

如果目标仓已有根级 `playbooks/` 并选择继续作为真值源，最小协议包中的 `ai-agent-protocols/playbooks/` 可改为只包含 `README.md` 或别名文件，不复制根级手册正文。

## 闭环检查

落盘后必须检查：

- 用户协议中的每个入口路径是否存在。
- 生成模式是否符合用户确认；默认项目版是否没有无证据语言/框架路由。
- 工作区状态是否清楚；如存在未跟踪文件或无关修改，应在生成报告中说明但不擅自处理。
- `playbooks/` 中是否覆盖用户协议声明的任务分类。
- `templates/` 中是否有用户级、项目级和路由卡片模板。
- `checks/` 中是否有维护、安全和性能检查清单。
- 是否误把项目专属命令、业务规则或一次性约定写入通用模板。
- 是否误把生成过程证据、读取文件清单或“已验证项目事实来源”写入协议正文。
- 是否误把生成依据写入 `ai-agent-protocols/README.md`、`project/AGENTS.md` 或其他入口说明。
- 生效协议、协议包 README 和入口说明是否仍残留 `<...>` 模板占位符。
- 项目级 `必须`、`禁止`、`默认` 或 `仅当` 是否都有目标仓证据支撑。
- 是否存在根级 `playbooks/` 与 `ai-agent-protocols/playbooks/` 的同内容全文双写；若存在，应明确一个为真值源，另一个改为索引或别名。
- 嵌套入口文件中的 `AGENTS.md`、`CODEX.md`、`playbooks/`、`routes/`、`checks/` 路径是否按当前文件位置可解析。

生成报告应与生效协议分离，至少包含：

- 本次生成模式和确认依据。
- 创建、修改、跳过的文件清单。
- 项目事实证据表和待确认项。
- 占位符处理结果。
- 无关技术栈路由检查结果。
- 使用者下一步，例如确认入口文件名、审阅待确认事实、删除未采用路由或在 `git add` 前复查生成报告。
