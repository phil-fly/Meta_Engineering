---
name: maintain-agent-protocols
description: "创建、审查、升级和维护 AI Agent 协作协议与规则路由。Use for Protocol Engineer reviews, trigger-stability reviews, constraint-to-workflow gate design, rule ingestion, protocol-package creation/upgrade sync, Spec-first workflow routing, trigger-entry decisions, maintenance-location decisions, AGENTS.md/CLAUDE.md and legacy CODEX.md migration, model-aware entry selection, ai-agent-workspace/protocols or compatible ai-agent-protocols layout, user/project protocol templates, route-based engineering rules, execution-rate/token-cost/conflict analysis, UI/frontend/backend/API/security/performance/platform route design, and AI coding workflow agreements. Do not use for ordinary feature implementation, product design, normal code review, generic architecture discussion, external spec governance, service onboarding, or project debugging unless the user is maintaining agent collaboration protocols or rule routing."
---

# Maintain Agent Protocols

## 概览

使用本技能创建和维护 AI Agent 协作协议，使规则清晰分层、入口稳定、执行细节可按需加载。

技能维护本身按技能创建流程处理，不需要项目规格变更流程。`SKILL.md` 只保留触发、流程和引用导航；执行细节必须下沉到 `references/` 分层文件。

## 技能内部分层

按任务场景读取以下目录，不要默认全量加载。需要总览时先读 `references/index.md`。

- `references/protocol/`：协议生成与维护场景，包含层级、目标仓目录结构、入口模板和冲突处理。
- `references/engineering/`：工程规则路由场景；企业级 SaaS 设计、前端、后端、安全、性能、平台、治理必须用目录隔离。
- `references/scenarios/`：任务流程场景，覆盖开发、架构、安全审查、性能审查、排障和调研。
- `references/checks/`：审查检查场景，覆盖维护、安全与性能检查清单。
- `references/shared/`：随 Skill 安装的跨技能规则运行时资产；源码仓根级 `references/` 是跨技能编辑真值源，发布前必须验证精确副本或当前 Skill 专用投影同步。
- `templates/`：可复制到目标仓统一产物目录的协议模板资产；新项目默认使用 `ai-agent-workspace/protocols/templates/`，旧项目可兼容 `ai-agent-protocols/templates/`；维护模板正文时必须同步 `user-protocol-template.md`、`project-protocol-template.md` 和 `route-card-template.md`。
- `scripts/`：技能维护验证脚本与协议包工具链；`protocol-package.py` 用于目标仓探测、生成计划、协议包 scaffold 和结果验证，其他检查脚本用于模板同步、编号、占位符和引用校验。

## 工作流

1. 识别请求类型。
   - `创建`：起草新的用户级协议、项目级协议或目标仓协议包。
   - `维护`：更新、合并、拆分或重构已有规则。
   - `升级同步`：对照最新技能规则，审查并升级已落盘的项目协议包，保持现有真值源并按最小修改同步新增或变更约束。
   - `审查`：检查规则是否存在遗漏、歧义、冲突、范围缺失或过期约束。
   - `触发稳定性审查`：检查任务类型、场景手册、工程路由、项目约束、工作流节点门禁和检查项之间的触发链路是否稳定。
   - `转换`：把零散说明、口头约定或草稿转成结构化协议和路由文件。
   - `协议工程`：从执行率、复杂度、冲突、Token 成本和长期维护性审查协议体系。
   - `规则摄入`：判断原则、约束、执行流程、模板、检查项和知识应维护在哪里，是否作为触发入口。
   - 请求命中多个类型时，读取 `references/protocol/workflow-routing.md`，按最终交付物选出唯一主流程；写入任务以创建、升级同步、维护或转换为主，审查、触发稳定性审查和协议工程只作为辅助分析维度。
   - 只读任务依次优先选择触发稳定性审查、协议工程、一般审查；规则只问“放哪里”时走规则摄入，要求直接合并时走维护主流程并以规则摄入为辅助流程。
   - 首次进度说明和最终回复必须声明主流程及必要的辅助流程；只有候选主流程会改变写入范围、覆盖策略或真值源且证据无法裁决时才询问用户，否则按保守范围继续。
   - 仅当用户明确要求创建、落盘、补齐或维护目标仓协议包时，才进入生成流程；读取或触发技能本身不会自动生成任何文件。

2. 判断目标层级。
   - `用户级`：长期有效的个人协作偏好、默认任务路由、全局安全边界、回复风格、跨项目原则。
   - `项目级`：仓库专属架构、命令、测试要求、编码约定、发布流程、业务领域约束。
   - `工程路由`：UI、JavaScript/TypeScript、Go、Java、Rust、Python、API、安全、性能等功能类型的执行细节入口。
   - `场景手册`：开发、架构、安全审查、性能审查、排障、调研等任务方法。
   - `临时规则`：短期本地约定，除非变成可复用规则，否则不要沉淀为长期协议。

3. 编辑前先收集上下文。
   - 优先检查 `AGENTS.md`、`CODEX.md`、`CLAUDE.md`、`.cursor/rules`、`.github/copilot-instructions.md`、`ai-agent-protocols/**/*.md`、历史 `playbooks/*.md`、项目文档和用户当前指令。
   - 保留历史决策和项目术语，除非它们已经明确过期或冲突。
   - 仓库扫描得到的来源证据、文件清单和生成过程记录只用于本轮判断，默认不写入生效协议正文。
   - 升级同步类任务先识别当前项目的生效入口、正文真值源和兼容入口，再对照最新技能 `references/` 做差异审查，区分新增约束、变更约束、项目特例和不适用规则。
   - 生成协议包前必须先输出生成方案预览，说明生效入口、生成模式、拟生成文件、项目事实证据和待确认项。
   - 创建或补齐协议包时，优先使用 `scripts/protocol-package.py detect` 和 `scripts/protocol-package.py plan` 生成结构化项目证据和生成计划；用户确认后再使用 `scaffold` 落盘，维护根级生效入口，最后用 `validate` 检查入口、引用和协议包结果。`scaffold` 不写入口，入口未维护时验证失败是预期门禁。
   - 升级同步类任务在修改前也必须先输出升级预览，说明当前真值源、拟修改文件、编号变化、规则来源、待确认项和潜在冲突。
   - 创建、升级同步和协议工程审查类任务应检查触发链路：工作流是否能读到必要场景手册、条件适用路由是否有触发条件、项目级约束是否能被相关流程节点门禁触达、闭环是否映射检查项。
   - 预览后对关键决策使用交互式选择（AskUserQuestion）：模型入口文件、生成模式、真值源冲突解决、工程路由裁剪策略；读取 `references/shared/interactive-decision-protocol.md`。
   - 交互式选择不可用时降级为结构化文本问询。
   - 审查类任务必须说明检查范围、未检查范围和结论适用范围。

4. 应用协议设计规则。
   - 读取 `references/protocol/index.md`，再按场景读取 `references/protocol/guide.md`。
   - 涉及协议工程审查、执行率、Token 成本、协议膨胀或冲突分析时，读取 `references/protocol/protocol-engineer.md`。
   - 涉及触发稳定性审查、条件适用路由触发、项目约束嵌入流程、工作流节点门禁或检查项映射时，读取 `references/protocol/trigger-stability-guide.md`。
   - 涉及原则摄入、约束摄入、执行流程摄入、约束触发项绑定或触发入口判断时，读取 `references/protocol/rule-ingestion.md`。
   - 涉及 OpenSpec、Spec-first、规范驱动开发、审查修复闭环或 Epic/Subtask 拆分时，读取 `references/protocol/openspec-workflow.md`。
   - 涉及目标仓统一产物入口、跨技能产物目录或新旧路径兼容时，读取 `references/shared/target-workspace-layout.md`。
   - 涉及协议包落盘、三档生成模式、模板目录、playbooks 内容来源或目标仓文件生成时，读取 `references/protocol/package-blueprint.md`。
   - 涉及本技能自身目录结构、`templates/` 目录或结构校验 warning 处理时，读取 `references/protocol/skill-structure.md`。
   - 需要工程规则细节时先读取 `references/engineering/index.md`，再进入对应领域目录读取路由文件。
   - 区分“入口”和“执行细节”：用户协议定义路由，工程路由和场景手册定义执行细节。
   - 升级同步类任务默认保持目标仓既有真值源不变；除非用户明确要求迁移，不生成两套可编辑正文，不重建整包。
   - 落盘前必须先声明唯一生效入口和各资产真值源，例如项目协议、用户协议、playbooks、routes、checks 和 templates 分别由哪个目录维护。
   - 生成协作协议时必须按用户明确要求、当前模型/工具环境、既有协议文件和默认规则选择入口文件；Codex 场景默认生成或维护 `AGENTS.md`，Claude 场景默认生成或维护 `CLAUDE.md`，不得为 Codex 新建 `codex.md` 或 `CODEX.md`。
   - 工作流、约束和检查项必须使用分类编号，便于管理和引用；工作流使用 `WF-*`，约束使用 `CON-*`，检查项使用 `CHK-*`。
   - 在用户仓库新建协议包时，默认创建或维护 `ai-agent-workspace/protocols/`，并按功能类型做好入口分层；目标仓已存在 `ai-agent-protocols/` 时可作为兼容真值源，但必须声明映射并避免双写。
   - 用户协议中禁止写执行细节；用户协议只保留执行细节入口。
   - 生成用户协议时，工程路由和检查入口只能列出本次实际生成、既有存在或已生成兼容入口的路径；未采用入口只写入生成报告，不写入生效协议。
   - 用户协议使用 `@playbooks`、`@routes` 或 `@checks` 时，必须声明真实路径映射或生成兼容入口；任务分类、场景手册、工程路由和检查入口应写展开后的真实路径，避免模型把抽象入口误猜成根级目录。
   - 默认采用项目版生成模式：按当前仓库已验证技术栈裁剪 `routes/`，只为有证据的语言、框架和工程域生成入口。
   - 项目版路由索引必须标注 `项目证据支持`、`条件适用` 或 `通用治理`，并尽量裁剪到文件级路由。
   - 条件适用路由应在路由索引、对应路由或场景手册中写明触发条件；不要求把所有约束原文复制进 playbooks，但高风险或易漏读约束应绑定到相关 `WF-*` 的预检门、变更门、验证门或报告门，并保留短路径引用。
   - 完整路由覆盖仅在用户明确要求完整版时采用；未验证、跨项目通用或架构未启用的规则只能写成 `应`、`建议` 或 `如项目采用...`。
   - OpenSpec、风险控制等高频规则优先用锚点式引用压缩，避免在结构化约束和详情章节重复展开。
   - 默认采用最小修改，避免大范围重写。

5. 闭环。
   - 创建类任务：先给生成方案预览；落盘后给出生成报告、验收清单和使用者下一步。
   - 维护类任务：把每个发现归类为已解决、延后处理、明确排除或转入后续任务。
   - 升级同步类任务：输出升级前后差异、编号变更、适用性结论和触发稳定性变化；把每个发现归类为已解决、延后处理、明确排除或转入后续任务。
   - 触发稳定性审查类任务：输出高/中/低稳定触发清单、不能稳定触发的约束或路由、建议强化位置和剩余风险。
   - 高风险治理变更：编辑前说明影响和验证方式。
   - 若结构校验出现 `templates/` 或多层 `references/` warning，先按 `references/protocol/skill-structure.md` 判断是显式结构例外还是真缺陷，并在结果中说明。
   - 除非用户或项目协议明确要求，不自动提交。

## 工作流 Checkpoints

每完成一步必须先输出对应 Checkpoint 的实际计数再进入下一步，以下中间门禁不可跳过：

- Step 1：`主流程数 == 1`；输出主流程及辅助流程，无法唯一仲裁且会改变写入范围时停在写入前询问。
- Step 2：`已分类目标层级数 == 已识别目标层级总数`；归属不明项标为待确认，不静默丢弃。
- Step 3：`已读取必要来源数 == 上下文清单中的必要来源总数`；文件缺失或不可读时记录证据缺口并限制结论。
- Step 4：`已读取参考数 == 已选择参考数`；未读参考不得作为强结论依据。
- Step 5：`已解决数 + 延后数 + 排除数 + 后续任务数 == 发现总数`；等式不成立时不得宣告闭环。
- 任一 Checkpoint 失败时回到对应步骤；若用户改变最终交付物，必须从 Step 1 重新仲裁，禁止沿用旧写入范围。

## 行为准则

以下规则在整个会话期间有效，不因对话长度而放松：

1. ❗ 用户协议只保留入口和长期原则，执行细节必须下沉到 `references/` 或目标仓统一产物目录；每次修改前自检。
2. ❗ 新增规则必须先评估合理性、适用范围、反例和规范词强度，再按原则、约束、执行流程、模板、检查项、知识或临时约定分类并决定维护位置；约束类规则还必须判断是否绑定到 `WF-*` 节点门禁；每次输出前自检。
3. ❗ 审查和优化结论必须说明范围、证据和剩余风险；每次输出前自检。

## 工具优先级

| 操作 | 首选工具 | 降级条件 | 降级工具 |
| --- | --- | --- | --- |
| 查找文件 | `rg --files` / `find` | 首选命令不可用 | `ls` |
| 搜索规则 | `rg` | `rg` 不可用 | `grep` |
| 修改文件 | `apply_patch` | patch 无法唯一匹配 | 缩小上下文后重试 |
| 验证技能 | `skill-craft` 验证脚本 + `scripts/check-template-sync.py` + `scripts/check-cross-references.ts` | 脚本缺失、不可运行或连续 2 次失败 | 手动同步与引用检查 |

- 单次失败不等于工具不可用；先重试或缩小范围，连续 2 次同类失败后才降级。
- 降级时说明原因。

## 依赖链

- Step 2 的目标层级判断必须继承 Step 1 的请求类型，不能重新猜测任务。
- Step 1 必须只有一个主流程；审查维度不得与写入动作并列为主流程。
- Step 4 的输入 = Step 2 的完整层级分类 + Step 3 的完整证据清单；不得脱离前序产出重新猜测，出现新证据时先回到 Step 3 更新清单。
- Step 5 的输入 = Step 4 的全部决定与发现；不得重新生成问题清单，闭环分类数量之和必须等于发现总数。
- 写入或修改协议前，先核对规则类型、维护位置、触发入口和反证检查是否一致。
- 新增、移动或重命名工作流、约束和检查项前，先核对编号前缀、唯一性和引用是否同步。
- 修改模板正文后，必须验证 `templates/` 与 `references/protocol/` 下对应模板参考文件同步；自动脚本不可用时执行手动 `cmp` 检查。
- 修改跨技能共享规则后，必须验证源码仓根级 `references/` 与 `references/shared/` 的精确副本或当前 Skill 专用投影同步；独立安装态要求运行时资产存在、自包含且引用可达。

## 输出约束

禁止输出：

- 未标明来源的强结论。
- 把普通工程建议包装成协议规则。
- 把低频细则写进用户级入口。
- 把“已验证项目事实来源”、“生成依据”、读取文件清单或生成过程证据写入生效协议、协议包 README 或入口说明正文。
- 把缺少目标仓证据的通用模板内容写成项目级 `必须`。
- 让 `<project>`、`<install-command>` 等模板占位符进入生效协议、协议包 README 或入口说明正文。
- 让抽象入口引用悬空，例如用户协议写 `@playbooks/coding.md` 但未声明映射或生成兼容入口。
- 让未生成、未存在、未兼容的 `@routes`、`@checks` 或 `@playbooks` 入口进入生效协议。
- 让任务执行入口依赖未展开的路径变量，例如把开发任务手册写成 `@playbooks/coding.md` 而不是已确认的真实路径。
- 让工作流、约束或检查项缺少分类编号，或混用错误前缀。
- 在项目协议中同时用结构化约束和详情章节重复展开同一 OpenSpec、风险控制或审查闭环规则。
- 在推荐目录和兼容目录中全文双写同一 playbook、协议或检查清单，除非用户明确要求迁移并确认双写维护策略。
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
- 执行细节必须写入目标仓统一产物目录的协议子域，新项目默认 `ai-agent-workspace/protocols/`，旧项目可兼容 `ai-agent-protocols/`。
- 不要保留外部仓库路径、来源痕迹或外部规格依赖；规则应成为技能内自包含内容。
- 不要把重要约束藏在示例里。

维护规则时：

- 保留无关内容和原有格式。
- 用最小修改消除歧义或冲突。
- 移动规则时说明它为什么属于用户级、项目级、工程路由、场景手册或临时规则。
- 更新长期知识库或 Wiki 前先征求用户确认。
