# Maintain Agent Protocols 使用手册

## 目录

- [定位](#定位)
- [快速入口](#快速入口)
- [通用使用流程](#通用使用流程)
- [不同场景怎么快用](#不同场景怎么快用)
  - [1. 创建用户级协议](#1-创建用户级协议)
  - [2. 创建项目级协议](#2-创建项目级协议)
  - [3. 维护或合并规则](#3-维护或合并规则)
  - [4. 协议包升级同步](#4-协议包升级同步)
  - [5. 审查协议体系](#5-审查协议体系)
  - [6. 判断原则、约束与工作流](#6-判断原则约束与工作流)
  - [7. 生成工程路由](#7-生成工程路由)
  - [8. 维护技能自身](#8-维护技能自身)
- [常用验证](#常用验证)
- [协议包工具链](#协议包工具链)
- [输出闭环](#输出闭环)

## 定位

`maintain-agent-protocols` 用于创建、审查、重构和维护 AI Agent 协作协议与规则路由。

新项目默认把协议产物放入目标仓统一入口 `ai-agent-workspace/protocols/`；已有项目若采用 `ai-agent-protocols/`，可继续作为兼容真值源，但必须声明映射并避免双写。

它适合处理这类问题：

- 如何把零散协作规则整理成稳定协议。
- 如何区分用户级、项目级、工程路由、场景手册和临时规则。
- 如何判断一条规则属于原则、约束、工作流、模板、检查项或知识背景。
- 如何降低协议冲突、误触发、重复维护和上下文成本。
- 如何为目标仓生成或维护 `AGENTS.md`、`CLAUDE.md`、既有 `CODEX.md` 迁移兼容、`ai-agent-workspace/protocols/` 或兼容 `ai-agent-protocols/`。

不适合直接处理普通功能开发、普通代码审查、一般架构讨论或项目调试；除非任务目标是维护 Agent 协作协议、规则路由或技能本身。

## 快速入口

| 场景 | 你可以这样提问 | 优先读取 |
| --- | --- | --- |
| 创建协议 | `帮这个仓库生成 AI Agent 协作协议` | `references/protocol/index.md`、`references/protocol/package-blueprint.md` |
| 维护协议 | `把这些规则合并进现有 AGENTS.md` | `references/protocol/index.md`、`references/protocol/guide.md` |
| 协议升级同步 | `对照最新协议技能，升级当前项目协议包` | `references/protocol/index.md`、`references/protocol/guide.md`、`references/protocol/package-blueprint.md` |
| 多类型请求仲裁 | `先审查触发问题，再修复当前协议` | `references/protocol/workflow-routing.md` |
| 审查协议 | `审查这套协议有没有冲突和遗漏` | `references/protocol/protocol-engineer.md`、`references/checks/index.md` |
| 规则摄入 | `这条规则应该放在哪里` | `references/protocol/rule-ingestion.md` |
| 工作流整理 | `把这些任务流程整理成 playbook` | `references/scenarios/index.md`、`references/scenarios/playbooks.md` |
| 工程路由 | `给前端/API/安全规则做路由` | `references/engineering/index.md` |
| 企业级 SaaS 设计协议 | `把企业级 SaaS 控制台设计规则吸收到协议里` | `references/scenarios/playbooks.md`、`references/engineering/frontend/enterprise-saas-design.md`、`references/checks/checklists.md` |
| 前端路由 | `补充前端结构、状态、测试、UI 稳定性、可访问性或组件系统规则` | `references/engineering/frontend/index.md` |
| 前端设计系统维护 | `存在前端实现时，帮我建立并持续维护 design-tokens.md` | `references/engineering/frontend/design-system-maintenance.md`、`templates/design-tokens.md`；独立审查再读 `templates/frontend-design-system-review-prompt.md` |
| Spec-first | `开发任务是否需要先更新规范` | `references/protocol/openspec-workflow.md` |
| 技能结构维护 | `检查这个技能目录结构是否合理` | `references/protocol/skill-structure.md` |

## 通用使用流程

1. 先识别请求类型；同时命中多个类型时按最终交付物选一个主流程，审查维度作为辅助流程。
2. 再判断目标层级：用户级、项目级、工程域、场景手册、检查项、模板、知识或临时约定。
3. 只读取对应参考文件，避免一次性加载全部资料。
4. 修改前声明生效入口、真值源和影响范围。
5. 修改时采用最小变更，避免重复写同一规则正文。
6. 结束时说明变更范围、验证结果、剩余风险和未覆盖范围。

主流程仲裁规则：写入任务以创建、升级同步、维护或转换为主流程；一般审查、触发稳定性审查和协议工程只作为辅助分析维度。只读任务依次优先选择触发稳定性审查、协议工程、一般审查。只有候选流程会改变写入范围、覆盖策略或真值源且证据无法裁决时才询问用户。

入口文件默认规则：

- 用户明确指定入口文件时，按用户当前要求执行。
- 用户未指定时，先识别当前模型或工具环境：Codex/OpenAI 场景默认生成或维护 `AGENTS.md`；Claude/Anthropic 场景默认生成或维护 `CLAUDE.md`。
- 无法识别模型时默认使用 `AGENTS.md`。
- `CODEX.md` 或 `codex.md` 只作为既有历史文件的兼容、迁移或显式用户要求对象；不得在 Codex 场景默认新建。

编号默认规则：

- 工作流编号使用 `WF-*`，例如 `WF-CODING`。
- 约束编号使用 `CON-*`，例如 `CON-PROJECT-001`。
- 检查项编号使用 `CHK-*`，例如 `CHK-MAINT-001`。
- 生成或维护协议时，新增、移动或重命名以上项目必须同步编号引用。

## 不同场景怎么快用

### 1. 创建用户级协议

适用：想建立跨项目通用协作偏好、任务分类、优先级和长期原则。

快速做法：

1. 读取 `references/protocol/user-protocol-template.md`。
2. 只保留长期原则、入口路由和优先级。
3. 不写具体命令、工程细节或长检查清单。
4. 若引用 `@playbooks`、`@routes` 或 `@checks`，必须声明真实路径或生成兼容入口。
5. 工程路由和检查入口只保留本次实际生成、既有存在或已兼容的路径。

示例请求：

```text
基于我的协作偏好生成一份用户级 AGENTS.md，只保留入口和长期原则。
```

### 2. 创建项目级协议

适用：想记录仓库专属架构、命令、测试、发布、业务边界和项目例外。

快速做法：

1. 先扫描项目事实，不凭模板编造项目约束。
2. 读取 `references/protocol/project-protocol-template.md`。
3. 涉及 API、数据结构、配置、权限或架构时，检查是否需要同步项目 Spec。
4. 缺少证据的通用规则只能写成 `应`、`建议` 或 `如项目采用...`。

示例请求：

```text
为当前仓库生成项目级 Agent 协议，按已验证技术栈裁剪规则。
```

### 3. 维护或合并规则

适用：已有协议，需要添加、合并、拆分或降级规则。

快速做法：

1. 先判断新规则类型和适用范围。
2. 检查是否已有等价规则。
3. 只选择一个主真值源，其他位置只保留入口或引用。
4. 对每个发现标记为已解决、延后处理、明确排除或转入后续任务。

示例请求：

```text
把下面这些协作规则摄入当前协议，说明每条规则应该放在哪里。
```

### 4. 协议包升级同步

适用：项目仓库已经用本技能生成过 `AGENTS.md`、`CLAUDE.md`、根级 `playbooks/`、`ai-agent-workspace/protocols/` 或兼容 `ai-agent-protocols/`，现在技能新增或更新了长期约束，需要把项目仓库同步到新规则。

快速做法：

1. 先识别当前项目的生效入口、真值源和兼容入口，不假设目录结构。
2. 对照最新技能 `references/` 与目标仓现有协议做差异审查，区分新增约束、变更约束、项目特例和不适用规则。
3. 先输出升级预览，说明拟修改文件、编号变化、待确认项和不适用项。
4. 确认后按最小修改同步，保持单一真值源，不重建整包，不平行生成两套正文。
5. 最后按已解决、延后处理、明确排除、转入后续任务归类发现，并说明验证结果和剩余风险。

标准提示词：

```text
对照最新的 maintain-agent-protocols 技能规则，审查并升级当前项目仓库的协议包。

要求：
1. 先识别当前项目的生效入口和真值源，包括 AGENTS.md、CLAUDE.md、根级 playbooks/、ai-agent-workspace/protocols/ 或 ai-agent-protocols/，不要假设路径。
2. 保持现有真值源不变，除非我明确要求迁移；不要生成两套可编辑正文。
3. 先输出升级预览，再执行修改。预览中说明：
   - 当前真值源和兼容入口
   - 拟修改文件
   - 新增、变更、迁移或弃用的 WF-*、CON-*、CHK-* 编号
   - 新增约束来自哪些技能 reference
   - 待确认项、不适用项和潜在冲突
4. 只按最小修改同步新增或变更的长期约束，不重写无关内容，不覆盖项目特有规则。
5. 如果新约束涉及 API、数据结构、配置、权限模型或系统架构，先检查是否需要同步项目规范、OpenSpec、ADR 或设计文档。
6. 如目标仓已有根级 playbooks/ 或既有兼容目录，继续沿用现有真值源；除非我明确要求迁移，不要复制同一正文到新目录。
7. 最终按 已解决 / 延后处理 / 明确排除 / 转入后续任务 归类所有发现，并给出验证结果、剩余风险和未覆盖范围。
```

示例请求：

```text
对照最新协议技能，升级当前项目仓库的协议包，保持现有真值源不变，先给升级预览，再按最小修改同步新增约束。
```

### 5. 审查协议体系

适用：担心协议膨胀、冲突、误触发、执行率低或维护成本高。

快速做法：

1. 声明检查范围、未检查范围和结论适用范围。
2. 从入口、层级、触发、重复、冲突、真值源和闭环要求检查。
3. 只给有证据的强结论；证据不足时标注待确认。
4. 输出问题、影响、建议和归类闭环。

示例请求：

```text
审查当前技能的协议设计，重点看执行率、冲突和 Token 成本。
```

### 6. 判断原则、约束与工作流

适用：有一条新规则，不确定它应如何分类、放在哪里、是否需要进入触发入口。

快速做法：

1. 问规则目标是什么，是否长期有效。
2. 原则用于指导取舍，不包含具体命令或长流程。
3. 约束必须有范围、生效条件、规则正文、验证方式和例外。
4. 工作流必须有任务类型、步骤顺序、输入输出、验证方式和闭环。
5. 判断它是否会改变入口选择；不会改变入口的细则不要写到用户级顶层。

示例请求：

```text
判断这条规则属于原则、约束还是工作流，并建议维护位置。
```

### 7. 生成工程路由

适用：想把企业级 SaaS 产品设计、管理后台/控制台设计、UI、前端结构、状态缓存、测试、UI 稳定性、可访问性、组件系统、工具链、API、安全、性能、后端语言等执行细节做成按需加载的路由。

快速做法：

1. 读取 `references/engineering/index.md`；前端任务再进入 `references/engineering/frontend/index.md`。
2. 企业级 SaaS、管理后台或控制台设计任务先读取 `references/scenarios/playbooks.md` 的 `WF-ENTERPRISE-SAAS-DESIGN`，再读取 `references/engineering/frontend/enterprise-saas-design.md` 和对应检查清单。
3. 只为项目已有证据支持的技术栈生成入口。
4. 路由中标注规则状态：项目证据支持、条件适用或通用治理。
5. 用户级协议只保留入口，不复制工程细则正文。

示例请求：

```text
按当前仓库技术栈生成工程规则路由，只覆盖有项目证据的领域。
```

### 8. 维护技能自身

适用：修改本技能的 `SKILL.md`、`references/`、`templates/`、`agents/` 或 `scripts/`。

快速做法：

1. 修改触发能力时同步 `SKILL.md` frontmatter description。
2. 修改读取顺序时同步 `SKILL.md` 工作流和 `references/index.md`。
3. 修改模板正文时同步 `templates/` 与对应的 `references/protocol/` 模板参考文件。
4. 运行 `scripts/check-template-sync.py` 验证镜像模板同步、共享投影和独立审查模板的必备调查维度。

前端设计系统维护规则的完整流程以 `references/engineering/frontend/design-system-maintenance.md` 为真值源。真实前端实现证据成立时，`templates/design-tokens.md` 直接实例化到目标仓 `ai-agent-workspace/product/design/design-tokens.md` 或继承兼容旧路径，并在前端设计和开发前读取；只有 `package.json`、设计稿或文档时不创建。`templates/frontend-design-system-review-prompt.md` 是独立、自包含的只读审查执行模板，不替代设计和开发过程中的门禁。审查项左移时只提炼短门禁，不删除模板中的逐域问题和报告契约。

示例请求：

```text
更新这个技能，让它支持协议审查报告，并同步触发入口和参考导航。
```

## 常用验证

修改后至少检查：

```bash
python3 skills/maintain-agent-protocols/scripts/check-template-sync.py
node skills/maintain-agent-protocols/scripts/check-cross-references.ts
node skills/maintain-agent-protocols/scripts/check-rule-ids.ts
node skills/maintain-agent-protocols/scripts/check-placeholders.ts
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/maintain-agent-protocols/scripts -p 'test_*.py' -v
```

如果本轮没有修改模板、共享运行时资产或协议包工具链，仍应说明哪些检查未运行及其剩余风险。

## 协议包工具链

创建或补齐目标仓协议包时，优先用脚本把生成过程结构化：

```bash
python3 skills/maintain-agent-protocols/scripts/protocol-package.py detect <target-repo>
python3 skills/maintain-agent-protocols/scripts/protocol-package.py plan <target-repo> --mode project
python3 skills/maintain-agent-protocols/scripts/protocol-package.py scaffold <target-repo> --mode project
python3 skills/maintain-agent-protocols/scripts/protocol-package.py validate <target-repo>
```

`detect` 输出项目证据，`plan` 输出拟生成文件、条件设计产物和路由裁剪结果，`scaffold` 默认跳过既有文件，并且即使使用 `--overwrite` 也不会用模板覆盖既有 `design-tokens.md`。`validate` 还会检查根级生效入口、本地 Markdown 引用、`WF-*` 工作流、`CHK-*` 检查项、协议包目录、模板资产、路由索引状态和占位符泄漏；存在前端实现时还检查唯一 `design-tokens.md`、必备明细和回填状态。`scaffold` 不写根级入口，也不会替 Agent 猜测项目实际 Token，因此这些门禁完成前验证会失败；用户确认预览后再运行 `scaffold`。

## 输出闭环

最终回复建议包含：

- 变更范围。
- 读取或检查过的文件。
- 验证结果。
- 已解决、延后处理、明确排除或转入后续任务的发现归类。
- 剩余风险和未覆盖范围。
