# Target Workspace Layout

## 定位

本文件定义各技能在用户目标仓落盘 AI 协作产物时的统一入口目录。它用于避免不同技能各自创建 `ai-agent-protocols/`、`docs/`、`reports/` 等分散入口。

原则：

- 根级 `AGENTS.md`、`CLAUDE.md` 等仍是模型自动发现和运行入口。
- `ai-agent-workspace/` 是 AI 协作产物的统一入口目录。
- 已有项目可以继续使用既有 `docs/` 或 `ai-agent-protocols/` 作为真值源，但必须在统一入口中声明映射，避免双写。
- 新增技能不得自行发明新的目标仓顶层产物目录；必须注册到本布局或明确说明例外。

## 推荐结构

```text
ai-agent-workspace/
├── README.md
├── protocols/
│   ├── user/
│   ├── project/
│   ├── routes/
│   ├── playbooks/
│   ├── checks/
│   └── templates/
├── product/
│   ├── memory/
│   ├── strategy/
│   ├── prd/
│   ├── design/
│   └── resources/
├── reports/
│   ├── generation/
│   ├── reviews/
│   └── research/
└── shared/
    ├── glossary.md
    └── decisions.md
```

## 路径映射

| 能力域 | 推荐路径 | 兼容旧路径 | 说明 |
| --- | --- | --- | --- |
| 协议包 | `ai-agent-workspace/protocols/` | `ai-agent-protocols/` | 新项目默认使用推荐路径；旧项目已有 `ai-agent-protocols/` 时可继续作为真值源。 |
| 用户/项目入口协议 | 根级 `AGENTS.md` 或 `CLAUDE.md`；正文可在 `ai-agent-workspace/protocols/user/` 或 `project/` | 根级历史入口、`ai-agent-protocols/user/`、`ai-agent-protocols/project/` | 根级入口用于模型发现；正文真值源只能有一个。 |
| 工程路由 | `ai-agent-workspace/protocols/routes/` | `ai-agent-protocols/routes/` | 承载工程执行细节。 |
| 场景手册 | `ai-agent-workspace/protocols/playbooks/` | `ai-agent-protocols/playbooks/`、根级 `playbooks/` | 若根级 `playbooks/` 已存在且明确选为真值源，可保留；否则不得把协议入口自动猜到根级 `playbooks/`。 |
| 检查清单 | `ai-agent-workspace/protocols/checks/` | `ai-agent-protocols/checks/` | 承载审查和验收项。 |
| 协议模板 | `ai-agent-workspace/protocols/templates/` | `ai-agent-protocols/templates/` | 只放可复用模板，不放项目事实。 |
| 产品记忆 | `ai-agent-workspace/product/memory/` | `docs/00_MEMORY/` | 记录事实快照、会话记忆和 TODO。 |
| 立项与策略 | `ai-agent-workspace/product/strategy/` | `docs/01_STRATEGY/` | 记录价值、范围和业务决策依据。 |
| PRD | `ai-agent-workspace/product/prd/` | `docs/02_PRD/` | Framework PRD 与 Feature PRD。 |
| 设计与交付 | `ai-agent-workspace/product/design/` | `docs/03_DESIGN/` | 设计指导、mockup、prototype、handoff。 |
| 调研资料 | `ai-agent-workspace/product/resources/` | `docs/04_RESOURCES/` | 竞品、市场、原始资料。 |
| 生成/审查/调研报告 | `ai-agent-workspace/reports/` | 任务日志、Issue、PR 描述 | 生成过程证据不得写入生效协议正文。 |
| 共享词汇与跨域决策 | `ai-agent-workspace/shared/` | 项目已有 glossary、ADR、decision log | 用于跨协议和产品域共享的稳定信息。 |

## 选择规则

1. 新项目默认创建 `ai-agent-workspace/`。
2. 目标仓已存在 `ai-agent-workspace/` 时，优先继承其目录职责。
3. 目标仓已存在 `docs/`、`ai-agent-protocols/` 或根级 `playbooks/` 时，先判断是否继续作为真值源。
4. 兼容旧路径时，`ai-agent-workspace/README.md` 必须声明映射；兼容入口只写跳转、映射和真值源说明，不复制完整正文。
5. 生效入口中的任务手册、工程路由和检查清单路径应写成真实路径；除非映射明确声明，不得把 `@playbooks` 自动解释为根级 `playbooks/`。
6. 不允许同一产物在推荐路径和兼容路径中同时保存两份可编辑正文。
7. 用户明确指定目录时，按用户当前要求执行，但应说明与推荐布局的差异和维护风险。

## 生成预览要求

任何技能准备在目标仓创建或迁移 AI 协作产物前，应先输出生成方案预览，至少包含：

- 是否使用 `ai-agent-workspace/`。
- 根级模型入口文件：`AGENTS.md`、`CLAUDE.md` 或既有兼容入口。
- 各产物域的真值源：protocols、product、reports、shared。
- 是否继承旧路径，以及旧路径与推荐路径的映射。
- 将创建、修改、跳过或仅写索引的文件。
- 双写风险、路径迁移风险和用户需要确认的点。

## 新技能接入要求

新增技能若会在用户目标仓落盘文件，必须在技能说明中声明：

- 产物域属于 `protocols`、`product`、`reports`、`shared` 或新增域。
- 推荐写入路径。
- 兼容旧路径。
- 写入触发条件。
- 是否允许轻量讨论不落盘。

若确需新增顶层域，先更新本文件并说明原因。
