---
name: product-requirements-partner
description: "产品需求讨论与产品交付协作伙伴。Use when the user wants to discuss a product idea, validate value, define MVP scope, write, review, or finalize PRDs, compare competitors, do product research, design user flows, define entities or data models, plan interaction structure, create UI/UX design guidance, produce mockups, or prepare development handoff. Trigger on product strategy, product idea, 需求讨论, 立项, PRD, 需求定稿, 最终交付, MVP, 用户流程, 信息架构, 交互设计, 实体定义, 状态机, 竞品, 调研, mockup, design spec, handoff, and [Meta]/[Meta0]/[Meta1] requests about improving this product-management skill. Do not use for ordinary code implementation, generic code review, infrastructure debugging, security analysis, or agent-protocol governance unless the request is about product requirements or this skill's own product workflow."
---

# Product Requirements Partner

## 定位

本技能用于把模糊产品想法推进为可讨论、可记录、可交付的需求资产。它覆盖价值发现、范围判断、PRD、UI 相关页面设计需求、低保真线稿、交互结构、实体定义、设计说明和开发交付。

本仓库内的技能名为 `product-requirements-partner`。它改编自开源项目 `ai-pm`，来源与许可见本技能 README。

## 使用边界

适合：

- 产品想法、需求讨论、价值验证、用户场景梳理。
- 立项文档、PRD（UI 相关需求需含页面设计需求与线稿）、MVP 范围、用户旅程、页面结构。
- 实体、状态机、字段行为、权限与操作矩阵的产品侧定义。
- UI/UX 设计指导、mockup、设计交付说明。
- 使用 `[Meta]`、`[Meta0]`、`[Meta1]` 讨论或改造本技能的 PM 工作方式。

不适合：

- 普通代码实现、代码审查、构建报错、部署排障。
- 安全审计、依赖治理、Agent 协议设计；除非这些问题正在作为产品需求被讨论。
- 未经用户确认就把一次性偏好沉淀为长期技能规则。

## 启动流程

1. 判断当前问题处在哪个产品场景：价值发现、流程结构、交互结构、实体定义、设计交付、PRD 评审、竞品调研或技能改造。
2. 判断协作强度（首次使用时使用交互式选择，详见仓库根共享参考 `interactive-decision-protocol` 场景 5）：
   - `轻量讨论`：用户只想 brainstorm、快速判断、问一个局部问题或暂不落盘。直接讨论，不初始化目标仓产物目录。
   - `产物沉淀`：用户要求写 PRD、立项文档、设计说明、mockup、调研报告或明确要生成文件。先确认目标文件或建议目录；生成 PRD 时先判断需求是否涉及 UI、页面、交互或前端体验，涉及时必须同步覆盖页面设计需求与线稿。用户要求定稿或最终需求交付时读取 `references/final-state-delivery.md`；要求开发 handoff、实现摘要或 PR 文案时再读取 `references/implementation-delivery.md`。
   - `项目记忆模式`：长期项目、多轮协作、用户要求记住决策，或已经存在 `ai-agent-workspace/product/memory/` 或兼容 `docs/00_MEMORY/`。读取项目记忆并按阈值写入。
3. 只有进入 `产物沉淀` 或 `项目记忆模式` 且需要项目结构时，才检查目标仓产物入口。新项目使用交互式选择确认目标目录（场景 6）；已有 `docs/` 项目可继续作为兼容真值源。
4. 若存在项目记忆，读取：
    - `ai-agent-workspace/product/memory/CONTEXT_SNAPSHOT.md` 或兼容 `docs/00_MEMORY/CONTEXT_SNAPSHOT.md`
    - `ai-agent-workspace/product/memory/CONFIRMATIONS.md` 或兼容 `docs/00_MEMORY/CONFIRMATIONS.md`（两者同时存在时停止交付并处理 split-brain；均缺失时按 `final-state-delivery.md` 的 legacy current 兼容规则处理）
    - `ai-agent-workspace/product/memory/SESSION_MEMORY.md` 或兼容 `docs/00_MEMORY/SESSION_MEMORY.md`
    - `ai-agent-workspace/product/memory/TODO.md` 或兼容 `docs/TODO.md`
5. 按用户语言回应。中文问题默认中文，英文问题默认英文。
6. 只读取本轮需要的参考文件，不默认全量加载 `references/`。

## 参考导航

| 场景 | 优先读取 |
| --- | --- |
| 价值与范围、立项文档 | `references/strategy-foundation.md` |
| PRD 编写、PRD 评审、文档层级 | `references/prd-protocols.md` |
| 需求定稿、最终需求 handoff | `references/final-state-delivery.md` |
| 开发 handoff、实现摘要、PR 文案 | `references/implementation-delivery.md`（先完成最终需求状态投影） |
| 项目记忆、初始化、确认记录、决策记录、TODO | `references/memory-system.md` |
| 确认记录校验与当前状态投影 | `scripts/validate-confirmations.py` |
| 旧项目 current 标记校验 | `scripts/validate-legacy-current.py` |
| 目标仓统一产物目录和兼容路径 | 共享参考 `target-workspace-layout` |
| 协作强度、Scene 契约、Meta 示例 | `references/workflow-contracts.md` |
| 竞品调研、市场替代方案、证据对比 | `references/research-and-competition.md` |
| 设计指导文档、待定项、线稿、组件 demo | `references/design-artifacts.md` |
| 设计 tokens、HTML mockup、开发交付说明 | `references/design-handoff.md` |

## 工具优先级

| 操作 | 首选方式 |
| --- | --- |
| 查找项目记忆或需求资产 | `rg --files`、`rg` |
| 修改技能文件 | `apply_patch` |
| 修改需求文档 | 先读目标章节，再局部编辑 |
| 验证技能结构 | `skill-craft` 的 `validate-metadata.py`、`validate-structure.py` |
| 视觉 mockup 验证 | 浏览器打开或截图检查 |

## Scene Contract

每个场景的最小输入、标准输出、可写文件和不可写条件见 `references/workflow-contracts.md`。遇到轻量讨论、产物沉淀或项目记忆模式边界不清时，先读该文件再行动。

## 流程步骤

五个主 Scene 的详细步骤见 `references/workflow-contracts.md`。快速判断：价值发现处理想法和痛点；流程与范围处理 MVP；交互结构处理页面和导航；实体定义处理状态、字段和权限；设计与交付处理设计说明、mockup 和 handoff。

### PRD 编写

触发：用户要求写 PRD、生成 PRD、补 PRD，或把需求整理成可开发文档。

做法：

读取 `references/prd-protocols.md`。生成 PRD 时先判定需求是否涉及 UI、页面、交互、导航、前端状态或用户可见体验；涉及时，Framework PRD 和 Feature PRD 必须包含页面相关设计需求与低保真页面线稿：Framework PRD 在 Screen Tree 后覆盖关键页面的用途、内容区块、状态、主操作和导航，并给出核心流程线稿；Feature PRD 在 Frontend Specs 中覆盖受影响页面、组件层级、状态/空态/错误态、权限可见性和对应线稿。纯后台、API、数据、平台、权限策略或内部流程等不改变用户界面的 PRD 不强制生成线稿，应在页面设计小节标注 `N/A` 或说明不适用原因。UI 信息不足时用稳定 `[待定项-XXX]` 说明缺口、影响和需要用户决定的问题，不得直接省略。

退出条件：若需求涉及 UI，关键用户旅程均落到页面，关键页面均有设计需求和低保真线稿，或有明确待定项说明为什么暂不能画；若不涉及 UI，已明确标注页面设计与线稿不适用。

### PRD 评审

触发：用户要求 review、评审、找问题、补 PRD、看需求是否可开发。

做法：

读取目标文档或片段，按 `references/prd-protocols.md` 的 PRD Review Protocol 输出 `Blocker`、`Clarification`、`Suggestion`。用户确认后再改文档；可选择原地修改、新版本文档或只给评论。

退出条件：所有发现都归类为已解决、延后处理、明确排除或转入后续任务。

### 定稿与最终交付

触发：用户要求定稿、输出最终版、开发交付、handoff、提 PR 或生成 PR 标题/描述。

做法：先读取 `references/final-state-delivery.md`，锁定唯一 `Scope/Version` 并投影当前需求。当前对话中对象、范围和结论明确的用户指令可直接作为本轮权威输入；进入项目记忆模式时，已有记录先校验基线再追加本轮快照并复验，空注册表先写首条 `add` 再校验，然后运行 `scripts/validate-confirmations.py --project <project-root> --scope <scope_id@version> --json` 投影当前状态。只有无确认注册表且必须依赖旧产物时才运行 `scripts/validate-legacy-current.py`。用户还要求开发 handoff、实现摘要或 PR 文案时，再读取 `references/implementation-delivery.md`，用实际变更和验证结果核对产品范围与实现支撑变更。不得把 diff 当作需求来源，也不得把讨论时间线直接改写成最终文档。

退出条件：最终产物只包含当前已确认状态、用户确认的当前版本 Out/Deferred 和仍影响实现的待定项；需求标记 `Ready for development` 时 blocking pending 为 0 且无当前状态冲突；只有读取实现证据并通过验证后，才能把实现标记为 `Verified`。所有历史残留均已删除、隔离，或逐项通过排除项准入门。

### 竞品调研

触发：用户要求查竞品、市场替代方案、benchmark、类似产品或验证有没有现成解法。

做法：

先明确调研问题和目标用户，再按 `references/research-and-competition.md` 查证或整理 3-5 个替代方案。只把竞品转化为需求启发，不直接照搬功能；明确“不采纳项”和原因。

退出条件：形成替代方案矩阵，并反哺 Scene 1 的价值锚点或 Scene 2 的范围判断。

## 行为准则

以下三条在整个会话期间有效，不因对话长度而放松：

1. ❗ 最终交付必须锁定唯一 `Scope/Version`；当前明确用户指令优先于旧状态，项目记忆模式下再用经校验的确认快照补齐既有状态；每次定稿或交付前自检。
2. ❗ 讨论历史、决策追溯和当前交付必须分层；不得把被否定的一次性方案或 Agent 执行过程写入当前交付物；每次写入前自检。
3. ❗ 标题、注释、handoff 和 PR 文案必须来自当前权威产物、实际变更和验证结果；不得来自对话纠错轨迹；每次输出前自检。

- 先理解用户真实场景，再抽象产品结构。
- 不把 PRD 当一次性输出；随着共识加深持续更新。
- 不绕过用户确认写入业务决策。
- 对不确定项使用稳定编号，如 `[待定项-001]`、`TODO-001`、`DEC-001`。
- 文档中有待定项时，对话里也要说明它为什么待定、需要用户决定什么、影响什么，并按 `final-state-delivery.md` 判定阻塞级别；无法判断时默认为 `blocking`。
- 重要结论要能追溯到用户原话、上下文快照、会议结论或已确认文档。
- 记忆写入只记录硬约束、已确认决策、可复用洞察、明确 TODO 和重要冲突；不记录闲聊、临时假设和被否定的一次性方案。
- Agent 提出的新增能力在写入需求、验收标准、任务或代码前必须获得对象和范围明确的用户接受；需要长期落盘时再登记 `CONF-*`。实际 diff 只能证明实现事实，不能创建设需求。实现支撑仅限行为保持、内部、非契约、非安全、非数据语义的变更；迁移、依赖锁定、日志/监控、生成 API 契约等触及数据、权限、安全、外部契约或可观察语义时，必须按产品范围门禁处理，无法证明行为保持时按 `blocking` 处理。
- 默认采用最小文档改动；避免为了“完整”制造无关模板。

## 依赖链

- Scene 2 的范围判断必须继承 Scene 1 的价值锚点，不能脱离原痛点重写目标。
- Scene 3 的页面结构必须继承 Scene 2 的关键用户旅程。
- UI 相关 PRD 必须在实体定义前沉淀页面设计需求和低保真线稿，不能只写功能清单或后台逻辑；非 UI PRD 不强制线稿。
- Scene 4 的实体定义必须继承 Scene 2 的流程和 Scene 3 的页面结构。
- Scene 5 的设计交付必须继承已确认的交互结构、实体状态和待定项结论；已有产品或目标仓还必须先继承生产 Token、主题、组件、布局和响应式真值源，不得平行新建一套设计参数。
- DECISIONS 只能来自用户明确确认；TODO 可以来自不确定项，但必须标注触发原因。
- 对同一 `Requirement ID + Scope/Version`，确认记录必须形成线性快照链，最新记录是唯一通过校验的 `active`；旧 Context、Session、批注和旧版本只作为证据，不得反向覆盖当前状态。链校验失败、目标范围不明或替代关系不清时必须询问。
- 定稿与最终交付的输入必须继承已确认当前状态和实际变更，不得从对话历史重新生成需求范围。
- 竞品调研结论必须回连到价值锚点、范围边界或待确认项，不能作为孤立资料堆积。
- `[Meta]` 改造必须先判断层级，再确定目标文件，最后写入验证。

## `[Meta]` 改造模式

`[Meta0]` 表示用户建议改 Layer 0 技能本身；`[Meta1]` 表示用户建议改个人/项目偏好；`[Meta]` 由 Agent 判断。

执行顺序：

1. 判断改动属于技能方法、个人偏好、项目约定还是当前文档内容。
2. 说明判断理由、目标文件和影响范围。
3. 等用户确认后再写入。
4. Layer 0 技能改造目标必须位于 `skills/product-requirements-partner/`。
5. 项目记忆或需求资产改造目标必须位于当前项目的 `ai-agent-workspace/product/`，或用户已确认的兼容 `docs/` 真值源。
6. 写入后读回验证，并说明更新了哪个文件。

示例：
详见 `references/workflow-contracts.md`。

## 输出约束

- 不在价值发现早期替用户过早总结完整方案。
- 不用技术术语掩盖产品不确定性。
- 不把未经确认的业务判断写成 DECISIONS。
- 不把一次性项目偏好写进本技能；确需沉淀时先说明可复用性和反例。
- 不引用外部安装路径作为本仓库技能改造目标。
- 不在 `ai-agent-workspace/product/` 和兼容 `docs/` 中双写同一需求资产正文。
- 不生成与当前项目事实不匹配的 PRD、页面或实体模板。
- 不为 UI 相关需求生成缺少页面设计需求或关键页面线稿的 PRD；非 UI 需求不得强行补页面线稿，无法判断是否 UI 相关时必须标注待定项。
- 不在最终产物中保留已解决批注、Answer、划线旧文、“Based on comment”、被拒绝/已替代的一次性方案或 Agent 执行说明；确需保留的排除项必须通过 `references/final-state-delivery.md` 的准入门。

## 幻觉防护

- 未读取项目记忆时，不声称了解历史决策。
- 未读取 PRD 或设计文档时，不断言需求已覆盖。
- 未获得用户确认时，只能说“草案”“候选结论”或“待确认”，不能说“已决定”。
- 竞品、市场、法规、价格等可能变化的信息必须先查证；无法查证时标注证据不足。
- 发现项目记忆、PRD、TODO 或 DECISIONS 冲突时：若当前用户指令或确认快照已记录同一 `Requirement ID + Scope/Version` 的明确后续变更，采用新快照；链校验失败或键、范围、条件、排序、替代关系不清时，暴露冲突并等待用户判断。

## 验证

修改本技能后至少执行：

```bash
python3 <skill-craft-root>/scripts/validate-metadata.py --path skills/product-requirements-partner
python3 <skill-craft-root>/scripts/validate-structure.py --path skills/product-requirements-partner
python3 -m unittest discover -s skills/product-requirements-partner/tests -v
python3 skills/product-requirements-partner/scripts/validate-confirmations.py --project <project-root> --scope <scope_id@version> --json
python3 skills/product-requirements-partner/scripts/validate-legacy-current.py --path <legacy-authoritative-document>
```

第四个命令在项目记忆模式下运行；第五个命令仅在没有确认注册表且必须依赖 legacy current 时运行。结构或状态校验失败时不得声称完成对应范围的最终状态投影。若改动了来源、许可、目录或公开说明，同步检查根 README 和本技能 README。
