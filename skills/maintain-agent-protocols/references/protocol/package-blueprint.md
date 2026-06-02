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

## 内容来源

目标仓文件应从技能内 `references/` 派生，不要凭空编写，也不要复制外部仓库路径。

技能内 `templates/` 目录提供可直接复制到目标仓 `ai-agent-protocols/templates/` 的模板资产；`references/protocol/user-protocol-template.md`、`references/protocol/project-protocol-template.md` 和 `references/protocol/route-card-template.md` 是模板正文的解释性来源，维护时应保持两者同步。

```text
ai-agent-protocols/README.md
  → references/protocol/guide.md 的目录职责、入口策略和维护边界

ai-agent-protocols/user/AGENTS.md
  → references/protocol/user-protocol-template.md

ai-agent-protocols/project/AGENTS.md
  → references/protocol/project-protocol-template.md

ai-agent-protocols/routes/**
  → references/engineering/** 对应目录和文件

ai-agent-protocols/playbooks/*.md
  → references/scenarios/playbooks.md 中同名场景章节

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
- `playbooks/*.md` 应拆分为独立文件，每个文件只包含一个任务流程。
- `templates/*.md` 只放可复用格式骨架，不承载决策规则或长期原则。
- 修改技能内模板正文时，应同步更新 `templates/` 与 `references/protocol/` 下对应模板参考文件。
- `routes/**` 应保留领域分层，避免把所有工程规则压成单个大文件。
- `checks/*.md` 只放检查项，不放长流程或教程。
- 如果目标仓已经采用不同目录名，应先说明差异并征求确认；默认目录名是 `ai-agent-protocols`。

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

## 闭环检查

落盘后必须检查：

- 用户协议中的每个入口路径是否存在。
- `playbooks/` 中是否覆盖用户协议声明的任务分类。
- `templates/` 中是否有用户级、项目级和路由卡片模板。
- `checks/` 中是否有维护、安全和性能检查清单。
- 是否误把项目专属命令、业务规则或一次性约定写入通用模板。
