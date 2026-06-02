# AI Agent 协作协议指南

创建或维护用户级、项目级 AI Agent 协作协议时使用本参考。协议文件负责入口和边界，工程路由与场景手册负责执行细节。

## 协议层级

| 层级 | 目的 | 常见文件 | 适合放置 | 避免放置 |
| --- | --- | --- | --- | --- |
| 用户级 | 跨项目生效的默认协作规则 | `AGENTS.md`、`ai-agent-protocols/user/AGENTS.md` | 协作风格、指令优先级、任务分类、入口路由、长期原则 | 命令、步骤、检查清单、语言细节、项目约束 |
| 项目级 | 仓库专属约束和执行要求 | `AGENTS.md`、`CODEX.md`、`CLAUDE.md`、`ai-agent-protocols/project/AGENTS.md` | 架构、命令、测试、编码约定、发布、业务边界 | 个人偏好、全局哲学、跨项目长流程、生成过程证据 |
| 工程路由 | 按功能类型承载执行细节 | `ai-agent-protocols/routes/*.md` | UI、Go、Java、Rust、API、安全、性能等规则 | 用户协议入口、项目私有例外 |
| 场景手册 | 某类任务的执行方法 | `ai-agent-protocols/playbooks/*.md` | 开发、架构、安全审查、性能审查、排障、调研流程 | 稳定项目事实、全局优先级 |
| 检查清单 | 审查和验收项 | `ai-agent-protocols/checks/*.md` | 维护、安全、性能检查项 | 入口路由、项目实施细节 |
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

1. 明确目标：用户级协议、项目级协议、工程路由、场景手册，或完整协议包。
2. 收集已有规则：用户请求、仓库文档、现有协议文件、命令、测试要求和反复出现的问题。
3. 盘点已有入口：根级 `AGENTS.md`、`CODEX.md`、`CLAUDE.md`、根级 `playbooks/`、既有 `ai-agent-protocols/`、OpenSpec 或其他项目协议。
4. 先选择唯一生效入口和各资产真值源，再写入文件；不要同时生成两套可编辑正文。
5. 在用户仓库中创建或维护 `ai-agent-protocols/` 目录。
6. 默认生成完整路由骨架，避免遗漏 UI、Go、Java、Rust、通用安全、通用性能和通用质量入口。
7. 用户协议只写入口和原则，不写执行细节。
8. 工程路由写执行细节，并按功能类型互相引用。
9. 检查重复、歧义、冲突、遗漏和意外约束。

## 生效入口与真值源

落盘前必须先做入口决策：

- 项目协议只能有一个生效正文。若根级 `AGENTS.md` 生效，`ai-agent-protocols/project/AGENTS.md` 只写定位、读取顺序和维护说明；反之亦然。
- 用户协议只能有一个生效正文。若根级 `CODEX.md` 或用户级协议已存在，应优先保持现有入口，不在协议包内复制全文。
- 场景手册只能有一个可编辑正文目录。若目标仓已有根级 `playbooks/`，默认继承它作为真值源；除非用户明确要求迁移，否则不要把同一正文复制到 `ai-agent-protocols/playbooks/`。
- 若必须同时保留两个入口，其中一个应是别名、索引或跳转说明，不承载完整流程正文。
- 生成或维护后，最终回复应说明本次选择的生效入口和真值源，以及哪些旧入口被保留为兼容入口。

路径规则：

- 每个入口文件应明确路径口径：仓库根相对路径，或当前文件相对路径。
- 嵌套目录中的文件引用根级文件时，应使用可解析路径，例如 `../../AGENTS.md`，或明确标注 `仓库根：AGENTS.md`。
- 禁止在嵌套文件中写无法判断基准目录的裸路径，例如只写 `AGENTS.md`、`CODEX.md` 或 `playbooks/<task>.md`。

## 落盘触发边界

使用本技能不会自动创建目录或文件。只有用户明确要求创建、补齐、落盘或维护目标仓协议包时，才写入 `ai-agent-protocols/` 或相关入口文件。

目标仓协议包的文件清单、内容来源和最小生成范围见 `package-blueprint.md`。如果只是解释协议设计、回答目录来源或审查现有规则，应先输出结论，不自动落盘。

## 仓库目录分层

使用本技能在用户仓库中落盘协议时，默认创建以下结构。保留目录名 `ai-agent-protocols`，不要擅自改写拼写。

```text
ai-agent-protocols/
├── README.md
├── user/
│   └── AGENTS.md
├── project/
│   └── AGENTS.md
├── routes/
│   ├── index.md
│   ├── frontend/
│   │   ├── index.md
│   │   └── ui-development.md
│   ├── backend/
│   │   ├── index.md
│   │   ├── go.md
│   │   ├── java.md
│   │   └── rust.md
│   ├── core/
│   │   ├── index.md
│   │   ├── api-design.md
│   │   ├── auth-and-permission.md
│   │   ├── data-access.md
│   │   ├── common-quality.md
│   │   └── error-and-logging.md
│   ├── security/
│   │   ├── index.md
│   │   ├── common-security.md
│   │   ├── trust-boundary.md
│   │   ├── secrets-and-audit.md
│   │   ├── unsafe-selectors.md
│   │   ├── sensitive-operations.md
│   │   ├── safe-integers.md
│   │   ├── dependency-and-config.md
│   │   └── owasp.md
│   ├── performance/
│   │   ├── index.md
│   │   └── common-performance.md
│   ├── platform/
│   │   ├── index.md
│   │   ├── gateway.md
│   │   ├── deployment.md
│   │   └── observability.md
│   └── governance/
│       ├── index.md
│       └── agent-governance.md
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

推荐职责：

- `README.md`：说明目录职责、入口策略和维护边界。
- `user/`：用户级入口协议，只放定位、优先级、任务路由、长期原则。
- `project/`：项目级协议或模板，可包含项目命令和项目约束。
- `routes/`：按工程功能承载执行细节，是规则细节的主要落点；前端、后端、安全、性能等必须目录级隔离。
- `playbooks/`：按任务类型承载流程方法。
- `checks/`：承载审查和验收检查项。
- `templates/`：承载可复用协议模板。

## 用户协议入口规则

用户协议禁止包含执行细节。以下内容视为执行细节，必须下沉到 `ai-agent-protocols/` 下方子目录：

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

## 用户级协议模板

技能内可复用模板见 `user-protocol-template.md`。

- 可复制模板资产：`../../templates/user-protocol.md`。
- 维护模板正文时，必须同步更新 `user-protocol-template.md` 与 `../../templates/user-protocol.md`，避免目标仓落盘内容漂移。
- 目标仓建议落盘位置：`ai-agent-protocols/templates/user-protocol.md`。
- 实际生效时，可按目标仓约定复制到根 `AGENTS.md` 或 `ai-agent-protocols/user/AGENTS.md`。

## 项目级协议模板

技能内可复用模板见 `project-protocol-template.md`。

- 可复制模板资产：`../../templates/project-protocol.md`。
- 维护模板正文时，必须同步更新 `project-protocol-template.md` 与 `../../templates/project-protocol.md`，避免目标仓落盘内容漂移。
- 项目级模板中的约束信息应写成结构化记录，至少包含 `约束名称`、`适用范围`、`生效条件`、`规则正文` 和 `验证方式`，不要只留标签词。
- 项目级协议可以记录长期有效的项目事实和项目约束，但不要保留“已验证项目事实来源”、读取文件清单或生成过程证据；这些内容应进入生成报告、任务日志、Issue 或 PR 描述。
- 目标仓建议落盘位置：`ai-agent-protocols/templates/project-protocol.md`。
- 实际生效时，可按目标仓约定复制到根 `AGENTS.md`、`CODEX.md`、`CLAUDE.md` 或 `ai-agent-protocols/project/AGENTS.md`。

## 路由卡片模板

技能内可复用模板见 `route-card-template.md`。

- 可复制模板资产：`../../templates/route-card.md`。
- 维护路由卡片模板时，必须同步更新 `route-card-template.md` 与 `../../templates/route-card.md`，避免目标仓落盘内容漂移。
- 目标仓建议落盘位置：`ai-agent-protocols/templates/route-card.md`。
- 新增工程路由时，可按该模板创建具体 `routes/**.md` 文件，再补充领域规则正文。

## 维护检查清单

审查或编辑已有协议文件时使用：

- 范围：每条规则是否明确说明适用位置和对象？
- 归属：规则属于用户级、项目级、工程路由、场景手册、检查清单还是临时规则？
- 分层：用户协议是否只保留入口，执行细节是否已下沉？
- 覆盖：UI、Go、Java、Rust、通用安全、通用性能、通用质量是否都有入口？
- 可执行性：Agent 是否能不靠猜测直接遵循？
- 可验证性：是否能通过行为、输出或验证结果判断是否遵守？
- 约束完整性：每条约束是否写明适用范围、生效条件、规则正文和验证方式，而不是只留标签词？
- 重复：同一规则是否在多个层级重复出现？
- 冲突：低层级规则是否违背高优先级规则？
- 新鲜度：命令、路径、工具或政策是否过期？
- 风险：是否影响认证、权限、数据迁移、删除、安全控制逻辑或 Git 历史？
- 生成证据：是否误把读取文件清单、已验证来源或本次审计记录写入协议正文？
- 真值源：是否出现根级目录和 `ai-agent-protocols/` 同时承载同一完整正文？
- 路径：嵌套文件中的路径引用是否能按声明口径解析？
- 闭环：发现的问题是否归类为已解决、延后处理、明确排除或后续任务？

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
