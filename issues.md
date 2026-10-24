# 问题清单

本文件是当前仓库的问题台账唯一可编辑真值源。排障、审查或开发发现可执行问题时，应先在这里登记，再进入修复；外部 Issue 只作为关联记录。

## 状态与流转

```text
candidate → investigating → confirmed → planned → in_progress → verified → closed
                         ├→ rejected
                         ├→ duplicate
                         └→ deferred
```

修复前必须达到 `planned`，关闭前必须达到 `verified` 并补齐验证证据。`deferred`、`rejected` 和 `duplicate` 必须记录原因；`duplicate` 必须关联主问题 ID。

## 问题索引

| ID | 标题 | 状态 | 严重度 | 首次发现 | 最近更新 | 关联方案/变更 |
| --- | --- | --- | --- | --- | --- | --- |
| ISSUE-0001 | 排障发现未落盘且修复前缺少方案门禁 | closed | P1 | 2026-09-22 | 2026-09-22 | 协议、排障手册、模板与生成器 |
| ISSUE-0002 | 产品技能共享参考在安装态路径悬空 | closed | P0 | 2026-10-22 | 2026-10-22 | `product-requirements-partner/SKILL.md` |
| ISSUE-0003 | 协议技能工作流 Step 1 层级歧义且自述与结构不符 | closed | P1 | 2026-10-22 | 2026-10-22 | `maintain-agent-protocols/SKILL.md` |
| ISSUE-0004 | 产品技能协作强度缺少交付物判定规则 | closed | P1 | 2026-10-22 | 2026-10-22 | `product-requirements-partner/SKILL.md` |
| ISSUE-0005 | 两技能路径口径与工具降级说明漂移 | closed | P2 | 2026-10-22 | 2026-10-22 | 两技能 SKILL.md 与 `workflow-contracts.md` |
| ISSUE-0006 | 协议技能未定义「只要方案预览」的任务分类 | closed | P2 | 2026-10-22 | 2026-10-22 | `maintain-agent-protocols/SKILL.md` |
| ISSUE-0007 | 协议技能宿主信号覆盖既有入口，产出双入口方案 | closed | P2 | 2026-10-23 | 2026-10-23 | `protocol-package.py`、`CON-PACKAGE-ENTRY-MODEL-AWARE` |
| ISSUE-0008 | 共享协议场景 5 判据未同步，首次交互绕过协作强度修复 | closed | P1 | 2026-10-23 | 2026-10-23 | `interactive-decision-protocol.md` 及其投影 |
| ISSUE-0009 | `规则摄入` 在主流程身份上三处表述互相矛盾 | closed | P2 | 2026-10-23 | 2026-10-23 | `SKILL.md`、`workflow-routing.md` |
| ISSUE-0010 | 编号检查把标准名误判为裸编号或未知命名空间 | closed | P3 | 2026-10-23 | 2026-10-24 | `check-rule-ids.ts` |
| ISSUE-0011 | `skill-structure.md` 出现连续空行 | closed | P3 | 2026-10-23 | 2026-10-24 | `references/protocol/skill-structure.md` |
| ISSUE-0012 | 编号统计把未命名空间显示为 `(未命名空间)-*` | closed | P3 | 2026-10-23 | 2026-10-24 | `check-rule-ids.ts` |
| ISSUE-0013 | 标准名白名单静默吞掉同前缀编号 | closed | P3 | 2026-10-24 | 2026-10-24 | `check-rule-ids.ts`、`README.md`、`rule-ingestion.md` |

## 问题详情

### ISSUE-0001 排障发现未落盘且修复前缺少方案门禁

- 状态：closed
- 严重度：P1
- 首次发现：2026-09-22
- 最近更新：2026-09-22
- 负责人：协作协议维护
- 关联问题：无
- 关联方案/变更：`skills/maintain-agent-protocols/` 问题台账规则、排障手册、模板和协议包生成器

#### 现象与影响

- 现象：排障结果可以生成，但没有稳定写入 `issues.md`；修复可能在方案未落盘前开始。
- 影响范围：使用本技能进行排障、审查或修复的目标仓。
- 复现条件：排障流程产生可执行发现，且目标仓未声明问题台账门禁。

#### 证据与根因

- 证据：原 `WF-TROUBLESHOOTING` 只有根因、修复方案和验证报告步骤，没有台账登记、方案状态和关闭证据门禁。
- 根因：问题台账属于实际项目产物，但协议只描述了排障报告，没有定义唯一真值源、状态流转和生成器物化契约。
- 假设与验证记录：已通过协议引用、模板生成、目标台账兼容路径和完整生成器测试验证。

#### 修复方案

- 目标：让问题发现、修复方案、验证和关闭具备可追踪的文件生命周期。
- 范围与拟改动：增加 `issue-tracking.md`、`issues.md` 模板、`CON-ISSUE-*`、`CHK-ISSUE-*`；强化 `WF-TROUBLESHOOTING`；生成器物化唯一台账并阻止双写。
- 风险：已有目标仓可能存在根级 `issues.md`；需要复用既有真值源，不能自动创建第二份。
- 回滚方式：删除本次协议资产和新增台账文件，恢复原排障手册与生成器逻辑。
- 验证方式：运行协议引用、编号、模板同步和生成器单元测试；覆盖默认台账、根级兼容台账和双真值源冲突。
- Spec/ADR 影响：无；本次只修改协作协议和产物生成契约。

#### 实施与验证

- 实施结果：已完成；新增台账规则、状态机、修复前 `planned` 门禁、验证关闭门禁、发现对账、模板和生成器支持。
- 验证结果：`python3 -m unittest discover -s skills/maintain-agent-protocols/scripts -p 'test_*.py' -v` 通过 68 个测试；协议静态校验全部通过。
- 剩余风险：尚未在真实外部目标仓运行一次完整的排障任务；生成器只保证静态文件和引用契约，不证明宿主运行时触发率。
- 关闭条件：问题条目已登记，修复方案和验证证据已回填，静态检查和生成器测试通过。

### ISSUE-0002 产品技能共享参考在安装态路径悬空

- 状态：closed
- 严重度：P0
- 首次发现：2026-10-22
- 最近更新：2026-10-22
- 负责人：技能维护
- 关联问题：无
- 关联方案/变更：`skills/product-requirements-partner/SKILL.md`

#### 现象与影响

- 现象：`SKILL.md:33`、`SKILL.md:57` 用“仓库根共享参考 `interactive-decision-protocol` / `target-workspace-layout`”指代运行时依赖，未给出技能内相对路径。
- 影响范围：技能独立安装到宿主后，根级 `references/` 不存在，两条引用不可解析；协作强度选择与目标目录选择失去可执行依据。
- 复现条件：仅安装技能目录（无源码仓根级 `references/`）后触发协作强度选择或产物目录选择。

#### 证据与根因

- 证据：技能内实际可读副本为 `references/shared/interactive-decision-protocol.md`（场景 5-8）和 `references/shared/target-workspace-layout.md`；效果实测中执行 agent 明确报告“只写仓库根，未给可解析路径”。
- 根因：README 视角与运行时视角混用——README 用仓库根路径描述源码仓结构，SKILL.md 直接沿用了同一表述，未投影为安装态相对路径。
- 假设与验证记录：对照 `maintain-agent-protocols/SKILL.md:60`、`:70` 的显式相对路径写法，可确认属于表述缺失而非资产缺失。

#### 修复方案

- 目标：运行时引用在源码仓与安装态都可达。
- 范围与拟改动：把两处改为技能内相对路径，并保留“源码仓真值源在根级”的说明。
- 风险：低；只改引用表述，不改场景编号与内容。
- 回滚方式：还原该段落文本。
- 验证方式：引用检查脚本与单测。
- Spec/ADR 影响：无。

#### 实施与验证

- 实施结果：已把两处引用改为 `references/shared/interactive-decision-protocol.md` 与 `references/shared/target-workspace-layout.md`。
- 验证结果：引用检查由 145 条增至 147 条且全部有效；单测 10 个通过。
- 剩余风险：未在真实宿主安装态复跑；路径可达性由静态引用检查覆盖。

### ISSUE-0003 协议技能工作流 Step 1 层级歧义且自述与结构不符

- 状态：closed
- 严重度：P1
- 首次发现：2026-10-22
- 最近更新：2026-10-22
- 负责人：技能维护
- 关联问题：无
- 关联方案/变更：`skills/maintain-agent-protocols/SKILL.md`

#### 现象与影响

- 现象：`SKILL.md:28-45` 把 8 类请求类型与 2 条主辅流程仲裁规则共 10 个列表项缩进在 Step 1 内部，“识别请求类型”被埋进子项；`SKILL.md:12` 自称“只保留触发、流程和引用导航”，实际另有 6 个附加章节。
- 影响范围：执行 agent 需要靠缩进推断主流程；实测中执行 agent 报告“层级读起来矛盾”。
- 复现条件：任何触发本技能的写入类任务。

#### 证据与根因

- 证据：效果实测 with_skill 组 `FRICTION` 原文指出该层级矛盾。
- 根因：迭代中把请求分类表增量塞进 Step 1，未回收为独立步骤；自述句停留在早期版本。

#### 修复方案

- 目标：主流程可按序号线性执行，自述与实际结构一致。
- 范围与拟改动：把请求分类与仲裁下沉为独立步骤并指向 `references/protocol/workflow-routing.md`；修正 `:12` 自述覆盖实际章节。
- 风险：中；Step 编号变化会影响 Checkpoints 与依赖链的引用措辞，需同步。
- 回滚方式：`git revert` 本轮提交。
- 验证方式：模板同步、引用、编号、占位符脚本与单测；重跑效果实测。
- Spec/ADR 影响：无。

#### 实施与验证

- 实施结果：Step 1 拆为风险门与请求分类两步，类型定义下沉到 `references/protocol/workflow-routing.md`；Checkpoints 与依赖链重编号为 Step 2-6；概览自述改为“触发、主流程、门禁、跨会话约束和引用导航”。
- 验证结果：模板同步、引用、编号、占位符脚本与 74 个单测全部通过；SKILL.md 由 18564 字节降至 18295 字节。
- 剩余风险：编号重排后未在外部目标仓实跑一次完整生成流程。

### ISSUE-0004 产品技能协作强度缺少交付物判定规则

- 状态：closed
- 严重度：P1
- 首次发现：2026-10-22
- 最近更新：2026-10-22
- 负责人：技能维护
- 关联问题：无
- 关联方案/变更：`skills/product-requirements-partner/SKILL.md`

#### 现象与影响

- 现象：`轻量讨论` 与 `产物沉淀` 只按“是否落盘”区分，“要 PRD 但先别写文件”没有归属规则。
- 影响范围：用户明确点名交付物但不要求落盘时，UI 页面设计需求与线稿硬门禁被绕过。
- 复现条件：请求包含 PRD、立项、设计说明或 mockup 名称，同时声明暂不写文件。

#### 证据与根因

- 证据：效果实测 with_skill 组把该请求判为 `轻量讨论`，输出未覆盖线稿与实体状态机。
- 根因：协作强度定义把“落盘”与“交付物完整度”绑成同一维度。

#### 修复方案

- 目标：交付物名称决定内容完整度，落盘与否只决定是否写文件。
- 范围与拟改动：在启动流程协作强度判断处补充判定规则，并同步 `references/workflow-contracts.md` 的协作强度表。
- 风险：低；不改变三种模式的存在与边界。
- 回滚方式：`git revert` 本轮提交。
- 验证方式：单测、引用检查；重跑效果实测确认线稿门禁生效。
- Spec/ADR 影响：无。

#### 实施与验证

- 实施结果：启动流程改为固定判定顺序“交付物索取 -> 长期记忆 -> 是否落盘”，并同步 `workflow-contracts.md` 协作强度表；判据由“出现交付物名词”改为“把交付物作为本轮产出物索取”，仅提及名词的咨询仍属轻量讨论。
- 验证结果：同一 prompt 复测由误判轻量讨论转为产物沉淀，并触发 UI 线稿门禁；新增 4 条契约测试覆盖“提及但未索取”，单测 14 个通过。
- 剩余风险：仅覆盖一个典型 prompt，未覆盖纯后台需求是否被误判为需要线稿。

### ISSUE-0005 两技能路径口径与工具降级说明漂移

- 状态：closed
- 严重度：P2
- 首次发现：2026-10-22
- 最近更新：2026-10-22
- 负责人：技能维护
- 关联问题：ISSUE-0002
- 关联方案/变更：两技能 `SKILL.md`、`workflow-contracts.md`

#### 现象与影响

- 现象：`workflow-contracts.md:7`、`:122` 仍用旧 `docs/` 口径；产品技能工具表依赖外部 `skill-craft` 却无降级列；协议技能工具表列 `.ts` 脚本未写运行时要求。
- 影响范围：文档口径不一致会诱导 agent 回退旧路径；工具不可用时缺少降级动作。
- 复现条件：阅读协作强度表、`[Meta]` 层级示例或工具优先级表。

#### 证据与根因

- 证据：`workflow-contracts.md:15` 已用 `ai-agent-workspace/product/`，同文件 `:7`、`:122` 未同步；两技能工具表结构不一致。
- 根因：路径迁移与工具表加固分属不同批次，收尾未做全量口径对齐。

#### 修复方案

- 目标：同文件内路径口径唯一，工具表具备降级路径。
- 范围与拟改动：统一旧口径表述为“新路径 + 兼容旧路径”；给产品技能工具表补降级列；给协议技能 `.ts` 脚本补运行时说明。
- 风险：低。
- 回滚方式：`git revert` 本轮提交。
- 验证方式：占位符、引用、编号脚本与单测。
- Spec/ADR 影响：无。

#### 实施与验证

- 实施结果：产品技能统一 `workflow-contracts.md` 两处旧 `docs/` 口径并补工具降级列；协议技能补 `.ts` 脚本运行时说明；产品技能 Scene 计数改为五主 Scene + 三门禁。
- 验证结果：四个静态校验脚本与两技能单测全部通过。
- 剩余风险：无。

### ISSUE-0006 协议技能未定义「只要方案预览」的任务分类

- 状态：closed
- 严重度：P2
- 首次发现：2026-10-22
- 最近更新：2026-10-22
- 负责人：技能维护
- 关联问题：ISSUE-0003
- 关联方案/变更：`skills/maintain-agent-protocols/SKILL.md`

#### 现象与影响

- 现象：只读任务优先级只覆盖触发稳定性审查、协议工程和一般审查，未覆盖“要方案预览但明确不落盘”的请求；此类请求的交付物是生成计划，却按只读类型分类。
- 影响范围：用户要求先看方案、暂不写入时，主流程归属依赖 agent 自行推断。
- 复现条件：请求同时包含写入意图与“先别改文件”。

#### 证据与根因

- 证据：优化后复测中执行 agent 明确报告该缺口，并自行按“转换 + 预览”处理。
- 根因：分类维度只区分写入与只读，未区分“本轮是否落盘”。

#### 修复方案

- 目标：预览类请求有确定分类且不会误触发落盘。
- 范围与拟改动：在 Step 2 增加预览类请求的归属与停止点。
- 风险：低。
- 回滚方式：`git revert` 本轮提交。
- 验证方式：引用、占位符、编号脚本与单测。
- Spec/ADR 影响：无。

#### 实施与验证

- 实施结果：判据下沉到 `references/protocol/workflow-routing.md` 的 Checkpoint 1（写入任务，授权 pending），`SKILL.md` 只保留指向契约的短句，不再自带独立判据。
- 验证结果：四个静态校验脚本与单测通过；两处表述一致，`SKILL.md` 无与契约相反的判据。
- 剩余风险：未再跑一次独立复测验证该分支；静态契约已闭合。

### ISSUE-0007 协议技能宿主信号覆盖既有入口，产出双入口方案

- 状态：closed
- 严重度：P2
- 首次发现：2026-10-23
- 最近更新：2026-10-23
- 负责人：技能维护
- 关联问题：无
- 关联方案/变更：`skills/maintain-agent-protocols/scripts/protocol-package.py`、`references/protocol/package-blueprint.md`、`README.md`、`references/protocol/guide.md`

#### 现象与影响

- 现象：`collect_protocol_entries` 命中宿主信号后直接取 `HOST_DEFAULT_ENTRY[host]`，忽略 `existing_entries`。目标仓已有 `AGENTS.md` 且存在 `.claude/` 时，方案预览提出新建 `CLAUDE.md`，`selection_reason` 不提既有入口，`--apply-entry` 会写出第二个入口。
- 影响范围：同时维护 `AGENTS.md`（跨工具通用）与 `.claude/`（Claude Code 配置）的仓库。
- 复现条件：根级 `AGENTS.md` 存在，同时存在 `.claude/` 或 `.claude/settings.local.json`。

#### 证据与根因

- 证据：构造 `/tmp/dualentry` 复现，`existing_entries: ['AGENTS.md']` 而 `selected_entry: CLAUDE.md`。
- 根因：入口选择把「宿主默认入口」当成唯一判据，缺少「既有入口优先」的优先级；`artifact_conflicts` 只覆盖问题台账与条件产物，不覆盖入口文件。

#### 修复方案

- 目标：宿主信号不得推翻既有入口，且预览可见未生成的宿主默认入口。
- 范围与拟改动：`collect_protocol_entries` 增加既有入口优先分支并返回 `entry_advisory`，`plan_package` 把该提示并入 `advisories`；同步 README、`guide.md` 与 `CON-PACKAGE-ENTRY-MODEL-AWARE`。
- 风险：低；仅改变「有既有入口且宿主默认入口不存在」这一分支的选择结果。
- 回滚方式：按 PR #1 的实际合并形态选择——merge commit 合并时 `e2cd55f` 是 `v1.0` 的祖先，`git revert e2cd55f` 可用；squash 合并时该提交不进入 `v1.0`，须 `git revert <squash 提交>`（会连同 PR #1 其余改动一并回退），或按文件手工还原 `collect_protocol_entries` 的入口选择分支。
- 验证方式：新增 3 条单测（继承、复用、预览告警）与 `/tmp/dualentry` 手工复现。
- Spec/ADR 影响：无。

#### 实施与验证

- 实施结果：入口选择改为「宿主默认入口存在则复用，否则继承既有入口」，并在 `advisories` 中说明该宿主默认入口未生成。
- 验证结果：`/tmp/dualentry` 下 `selected_entry` 由 `CLAUDE.md` 变为 `AGENTS.md`，`entry_patch.entry` 同为 `AGENTS.md`，未生成 `CLAUDE.md`；MAP 单测 74 → 77 通过，四个静态脚本 PASS。
- 剩余风险：修复提交位于 PR #1（`e2cd55f`），本条随 PR #2 台账一并登记；若 #1 先合并，中间存在「已修复但未登记」的短暂窗口。

### ISSUE-0008 共享协议场景 5 判据未同步，首次交互绕过协作强度修复

- 状态：closed
- 严重度：P1
- 首次发现：2026-10-23
- 最近更新：2026-10-23
- 负责人：技能维护
- 关联问题：ISSUE-0004
- 关联方案/变更：`references/interactive-decision-protocol.md`、`skills/product-requirements-partner/references/shared/interactive-decision-protocol.md`

#### 现象与影响

- 现象：场景 5「协作强度选择」的决策依据仍写「是否提到 "写文档"、"生成 PRD" 等关键词」，与 ISSUE-0004 修正后的「把交付物作为本轮产出物索取」相反。
- 影响范围：`SKILL.md` 启动流程在首次使用时会直接指向该场景，首次交互按关键词判、主路径按索取判，两条路径给出相反答案。
- 复现条件：首次使用产品技能，用户只说「PRD 该怎么写」这类提及型咨询。

#### 证据与根因

- 证据：根级 `interactive-decision-protocol.md:143-146` 与产品技能投影 `:41-43` 均为旧判据。
- 根因：ISSUE-0004 只在 `SKILL.md` 与 `workflow-contracts.md` 落地，漏掉共享协议这一处运行时资产；新增的契约测试也只断言前两处。

#### 修复方案

- 目标：场景 5 判据与主路径同口径，且真值源与投影一致。
- 范围与拟改动：两处决策依据第三条改为「是否把交付物作为本轮产出物索取（仅提及 "写文档"、"PRD" 等名词不算）」。
- 风险：低；`check-template-sync.py` 会拦截单边修改。
- 回滚方式：`git revert` 本轮提交。
- 验证方式：模板同步脚本与产品技能单测。
- Spec/ADR 影响：无。

#### 实施与验证

- 实施结果：根级与投影同时改为索取判据；`test_collaboration_mode_contract.py` 新增 3 条断言，覆盖投影判据、根级判据与两者一致。
- 验证结果：`check-template-sync.py` PASS；产品技能单测 14 → 17 通过。
- 剩余风险：无。

### ISSUE-0009 `规则摄入` 在主流程身份上三处表述互相矛盾

- 状态：closed
- 严重度：P2
- 首次发现：2026-10-23
- 最近更新：2026-10-23
- 负责人：技能维护
- 关联问题：ISSUE-0003
- 关联方案/变更：`skills/maintain-agent-protocols/SKILL.md`、`references/protocol/workflow-routing.md`、`README.md`

#### 现象与影响

- 现象：`SKILL.md` 一处称 `规则摄入` 不是主流程并列项，另一处又称「走规则摄入」，而 `workflow-routing.md` 把它列为写入任务仲裁表的一行主流程。
- 影响范围：只问「这条规则该放哪里」的请求，主流程归属在契约与说明书之间不一致。
- 复现条件：请求只判断规则维护位置，不要求落盘。

#### 证据与根因

- 证据：三处表述无法同时为真；`规则摄入` 的交付物是放置结论而非文件，按 Checkpoint 1 应属只读。
- 根因：把 `规则摄入` 与写入主流程并列在写入表内，导致其只读身份与写入身份冲突。

#### 修复方案

- 目标：`规则摄入` 身份唯一——只读主流程，写入场景下仅作辅助流程。
- 范围与拟改动：从写入任务表移出该行，改为只读优先级第 1 项；`SKILL.md` 限定改为「不作为创建、维护、升级同步、转换四类写入主流程的并列项」；README 仲裁摘要同步。
- 风险：低。
- 回滚方式：`git revert` 本轮提交。
- 验证方式：引用、编号、占位符脚本与单测。
- Spec/ADR 影响：无。

#### 实施与验证

- 实施结果：`workflow-routing.md` 把该行从写入表移入只读优先级第 1 项；`SKILL.md` 与 README 的限定与摘要同步为「只读主流程 + 写入时辅助」。
- 验证结果：四个静态校验脚本与 77 个单测通过。
- 剩余风险：只读优先级由 3 项变 4 项，外部目标仓若引用旧序号需重新对齐。

### ISSUE-0010 编号检查把标准名误判为裸编号或未知命名空间

- 状态：closed
- 严重度：P3
- 首次发现：2026-10-23
- 最近更新：2026-10-24
- 负责人：技能维护
- 关联问题：ISSUE-0013
- 关联方案/变更：`skills/maintain-agent-protocols/scripts/check-rule-ids.ts`

#### 现象与影响

- 现象：`BARE_ID`（`^[A-Z]{2,}[0-9]{2,}$`）与 `NAMESPACED_ID` 把标准名当成规则编号——`- SHA256 校验` 被判为未命名空间裸编号，`- ISO-8601 时间格式` 被判为未知命名空间 `ISO-*`。
- 影响范围：含时间、编码、协议标准名的文档（排障手册、安全约束）容易被误报为编号缺陷；审查当时全仓零命中，属潜在缺陷。
- 复现条件：在 `references/` 或 `skills/` 的 md 定义位写入 `- SHA256 校验` 或 `- ISO-8601 时间格式`。

#### 证据与根因

- 证据：审查期探针文件写入上述两行后，脚本 FAIL，分别报 `SHA256` 缺少命名空间前缀、`ISO-8601` 使用未注册命名空间 `ISO-*`。
- 根因：编号识别只假设「命名空间 + 数字」一种形态，没有区分标准名与协议规则编号。

#### 修复方案

- 目标：标准名不再被判为编号缺陷，同时不放松对真缺陷的拦截。
- 范围与拟改动：新增 `STANDARD_ID` 白名单（ISO/IEC/IEEE/RFC/ANSI/ECMA/W3C/UTF/SHA/AES/RSA/TLS/SSL/HTTP/UUID/MD/SEMVER + 可选数字后缀），`parseDefinition` 命中即跳过。
- 风险：白名单按前缀整体放行，可能连带放行同前缀的疑似规则编号；由 ISSUE-0013 跟进。
- 回滚方式：merge commit 合并 PR #1 时 `git revert e2cd55f`；squash 合并时该提交不进入 `v1.0`，改为 revert 对应的 squash 提交，或手工移除 `STANDARD_ID` 判断。
- 验证方式：探针文件（标准名 PASS、假编号 FAIL）、四个静态脚本与单测。
- Spec/ADR 影响：无。

#### 实施与验证

- 实施结果：`STANDARD_ID` 白名单落地，`parseDefinition` 在解析前放行。
- 验证结果：探针写入 `ISO-8601`、`RFC-2119`、`SHA256`、`UTF-8` 时 PASS；写入 `FOO-001`、`BAR999` 时 FAIL 并列出文件。
- 剩余风险：白名单粒度为前缀整体，同前缀规则编号的可见性由 ISSUE-0013 补齐；本条登记晚于修复提交 `e2cd55f`，未满足台账「先登记再修复」的时序。

### ISSUE-0011 `skill-structure.md` 出现连续空行

- 状态：closed
- 严重度：P3
- 首次发现：2026-10-23
- 最近更新：2026-10-24
- 负责人：技能维护
- 关联问题：无
- 关联方案/变更：`skills/maintain-agent-protocols/references/protocol/skill-structure.md`

#### 现象与影响

- 现象：「`skill-craft` 的通用结构脚本（外部工具链，未随本仓库分发）可能提示：」之后出现两行空白，而同文件其他列表块均为单空行分隔。
- 影响范围：仅渲染与 diff 噪音，无行为影响。
- 复现条件：查看该文件第 18-22 行。

#### 证据与根因

- 证据：审查期读到该处连续两个空行，与同文件其余段落格式不一致。
- 根因：插入说明段时多留了一个换行。

#### 修复方案

- 目标：恢复单空行分隔。
- 范围与拟改动：删除多余空行。
- 风险：无。
- 回滚方式：补回空行。
- 验证方式：`check-cross-references.ts`（该文件被引用）与 `check-placeholders.ts`。
- Spec/ADR 影响：无。

#### 实施与验证

- 实施结果：删除多余空行，恢复单空行分隔。
- 验证结果：四个静态校验脚本 PASS，110 个文件占位符检查通过。
- 剩余风险：仓库没有 md 空行类 lint，同类问题只能靠审查发现。

### ISSUE-0012 编号统计把未命名空间显示为 `(未命名空间)-*`

- 状态：closed
- 严重度：P3
- 首次发现：2026-10-23
- 最近更新：2026-10-24
- 负责人：技能维护
- 关联问题：无
- 关联方案/变更：`skills/maintain-agent-protocols/scripts/check-rule-ids.ts`

#### 现象与影响

- 现象：统计输出把未命名空间编号的前缀显示为 `(未命名空间)-*`，读起来像存在一个叫「未命名空间」的命名空间。
- 影响范围：排障时误读输出，以为该编号属于某个已登记族。
- 复现条件：定义位出现裸编号（如 `PERF001`）后运行脚本。

#### 证据与根因

- 证据：`PERF001` 探针运行时输出 `- (未命名空间)-*: 1 个`。
- 根因：前缀拼接无条件追加 `-*`，没有对占位标签单独处理。

#### 修复方案

- 目标：占位标签不参与命名空间格式拼接。
- 范围与拟改动：统计输出处增加 label 判断，裸编号显示为 `(未命名空间)`。
- 风险：无。
- 回滚方式：merge commit 合并 PR #1 时 `git revert e2cd55f`；squash 合并时改为 revert 对应的 squash 提交，或手工还原统计输出处的前缀拼接。
- 验证方式：探针运行并核对统计行。
- Spec/ADR 影响：无。

#### 实施与验证

- 实施结果：裸编号的统计行改为 `(未命名空间): N 个`，不再拼接 `-*`。
- 验证结果：探针运行输出为 `(未命名空间): 1 个`；四个静态脚本 PASS。
- 剩余风险：无。

### ISSUE-0013 标准名白名单静默吞掉同前缀编号

- 状态：closed
- 严重度：P3
- 首次发现：2026-10-24
- 最近更新：2026-10-24
- 负责人：技能维护
- 关联问题：ISSUE-0010
- 关联方案/变更：`skills/maintain-agent-protocols/scripts/check-rule-ids.ts`、`README.md`、`references/protocol/rule-ingestion.md`

#### 现象与影响

- 现象：`STANDARD_ID` 白名单按前缀整体放行，定义位写入 `TLS-1`、`HTTP-2`、`SHA256`、`PERF001` 时，前三个既不计数也不报错，只有 `PERF001` 被报出。
- 影响范围：将来新增 `HTTP-01`、`TLS-2` 这类规则编号会静默通过检查。当前 `KNOWN_NAMESPACES` 与白名单无交集、297 个编号未变，属潜在缺陷。
- 复现条件：在任意 md 定义位写入 `- TLS-1 传输层检查`。

#### 证据与根因

- 证据：探针文件写入上述四行后，输出仅报 `PERF001`，总数仍为 297，`TLS-1`、`HTTP-2`、`SHA256` 完全不可见。
- 根因：`parseDefinition` 先做白名单判定并直接 `return null`，命中项从统计与报错中同时消失，没有留下计数或提示——与 ISSUE-0010 要消灭的「编号命名空间盲区」同源。

#### 修复方案

- 目标：白名单放行可见、可复核；已登记命名空间永不被白名单放行。
- 范围与拟改动：`extractRuleIds` 单独收集被放行的标准名，`checkUniqueness` 汇总后每次运行打印「按标准名跳过: N 种 / M 处（…）」；`parseDefinition` 增加 `KNOWN_NAMESPACES` 优先判断；同步 `README.md` 与 `rule-ingestion.md` 的校验说明。
- 风险：低；仅新增输出与一条优先级判断，不改变既有 297 个编号的判定。
- 回滚方式：按 PR #1 合并形态选择——merge commit 合并时 `git revert 9669125`；squash 合并时该提交不进入 `v1.0`，改为 revert 对应的 squash 提交，或手工还原 `parseDefinition` 与 `extractRuleIds`。
- 验证方式：探针复现、命名空间冲突实验、四个静态脚本与 77 个单测。
- Spec/ADR 影响：无。

#### 实施与验证

- 实施结果：白名单放行改为「已知命名空间优先」并单独收集，运行输出新增跳过行与复核提示；README 与 `rule-ingestion.md` 同步该行为。
- 验证结果：探针输出「按标准名跳过: 3 种 / 3 处（HTTP-2、SHA256、TLS-1）」，`PERF001` 仍 FAIL；临时把 `HTTP` 注册为命名空间后 `HTTP-2` 计入 `HTTP-*`，未被吞掉；全仓该行为 0 种 / 0 处，297 个编号不变；四个静态脚本 PASS、77 个单测 OK。
- 剩余风险：跳过行只给编号不给文件路径，同前缀规则编号混入时仍需人工定位；修复在 PR #1（`9669125`）、登记在 PR #2，仍属「修复先于登记」。
