---
name: product-requirements-partner
description: "产品想法、价值验证、MVP、竞品调研、用户流程、交互设计、PRD 编写/评审/定稿、设计与开发交付，含项目记忆、确认快照与 [Meta] 技能改造。Use for end-to-end product work, PRD, or design handoff; not for code-only tasks."
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

与宿主插件的分工：

- 只写一份常规 PRD、不需要项目记忆或交付状态治理时，优先使用宿主提供的 `prd-authoring`。
- 需要从价值发现推进到 MVP、实体、设计交付或实现交付，或需要 `CONFIRMATIONS.md`、`Scope/Version`、定稿状态投影时，使用本技能。
- 两者同时可用时，按用户是否要求项目记忆、确认链、设计/实现交付来判断，不按“谁先被提到”判断；没有插件时，本技能仍可执行单次 PRD。

## 启动流程

1. 判断当前问题处在哪个产品场景：价值发现、流程结构、交互结构、实体定义、设计交付、PRD 评审、竞品调研或技能改造。
2. 判断协作强度（首次使用时使用交互式选择，详见 `references/shared/interactive-decision-protocol.md` 场景 5）。判定顺序固定为：先看是否把交付物作为本轮产出物索取，再看是否需要长期记忆，最后才看是否要求落盘。三档触发与行为以 `references/workflow-contracts.md` 的协作强度表为唯一权威：
   - `轻量讨论`：brainstorm、快速判断、局部问题，或仅提及交付物名词做方法咨询（如“PRD 该怎么写”）。直接讨论，不初始化目标仓产物目录。
   - `产物沉淀`：把 PRD、立项、设计说明、mockup、调研报告等作为本轮产出物索取，或明确要求生成文件。“先别写文件”只停止落盘，不降低内容完整度。
   - `项目记忆模式`：长期项目、多轮协作、用户要求记住决策，或已存在项目记忆目录。
3. 只有进入 `产物沉淀` 或 `项目记忆模式` 且需要项目结构时，才检查目标仓产物入口。新项目使用交互式选择确认目标目录（场景 6）；已有 `docs/` 项目可继续作为兼容真值源。
4. 若存在项目记忆，读取：
    - `ai-agent-workspace/product/memory/CONTEXT_SNAPSHOT.md` 或兼容 `docs/00_MEMORY/CONTEXT_SNAPSHOT.md`
    - `ai-agent-workspace/product/memory/CONFIRMATIONS.md` 或兼容 `docs/00_MEMORY/CONFIRMATIONS.md`（两者同时存在时停止交付并处理 split-brain；均缺失时按 `final-state-delivery.md` 的 legacy current 兼容规则处理）
    - `ai-agent-workspace/product/memory/SESSION_MEMORY.md` 或兼容 `docs/00_MEMORY/SESSION_MEMORY.md`
    - `ai-agent-workspace/product/memory/TODO.md` 或兼容 `docs/TODO.md`
5. 按用户语言回应。中文问题默认中文，英文问题默认英文。
6. 只读取本轮需要的参考文件，不默认全量加载 `references/`。

## 参考导航

| 编号 / 触发词 | 优先读取 |
| --- | --- |
| WF-M1~M5、协作强度、CX-1~CX-5、Meta 示例 | `references/workflow-contracts.md` |
| 价值与范围、立项文档 | `references/strategy-foundation.md` |
| WF-T1 / WF-T2：PRD 编写、PRD 评审、文档层级、输入分级、深度选择、交付终检 | `references/prd-protocols.md` |
| WF-G1：需求定稿、最终需求 handoff | `references/final-state-delivery.md` |
| WF-G1 实现交付：开发 handoff、实现摘要、PR 文案 | `references/implementation-delivery.md`（先完成最终需求状态投影） |
| CX-3：项目记忆、初始化、确认记录、决策记录、TODO | `references/memory-system.md` |
| 确认记录校验与当前状态投影 | `scripts/validate-confirmations.py` |
| 旧项目 current 标记校验 | `scripts/validate-legacy-current.py` |
| 目标仓统一产物目录和兼容路径 | `references/shared/target-workspace-layout.md` |
| WF-T3：竞品调研、市场替代方案、证据对比 | `references/research-and-competition.md` |
| WF-M5：设计指导文档、待定项、线稿、组件 demo | `references/design-artifacts.md` |
| WF-M5：设计 tokens、HTML mockup、开发交付说明 | `references/design-handoff.md` |

## 工具优先级

工具名以宿主原生能力为准；下表以 Trae 为例，不构成对其他宿主的硬依赖。

| 操作 | 首选方式 | 降级条件 | 降级方式 |
| --- | --- | --- | --- |
| 查找项目记忆或需求资产 | 宿主文件/内容搜索（Trae：Glob、Grep） | 工具不可用 | 逐层目录浏览 |
| 修改技能或需求文件 | 宿主编辑工具（Trae：Edit、Write） | 无法唯一匹配 | 缩小上下文后重试 |
| 修改需求文档 | 先读目标章节，再局部编辑 | 文件过大或结构不明 | 只改命中章节，不动无关段落 |
| 验证技能结构 | `python3 -m unittest discover -s tests -v`；可选 `skill-craft` | Python 或外部工具链不可用 | 声明未运行，保留测试缺口 |
| 视觉 mockup 验证 | 浏览器打开或截图检查 | 无法渲染 | 标注未做视觉验证，不声称已确认 |

## 流程步骤

工作流分四层：`WF-M1`~`WF-M5` 是主干顺序流水线（价值发现、流程与范围、交互结构、实体定义、设计与交付），可停在任意环节；`WF-T1`~`WF-T3` 是任务型工作流（PRD 编写、PRD 评审、竞品调研），可独立触发并回填主干；`WF-G1` 定稿与最终交付是唯一出口门；`CX-1`~`CX-5` 是横切协议，在标注步骤生效。每个 WF 的完整定义（触发、输入、步骤、输出、退出条件）以 `references/workflow-contracts.md` 的 WF 注册区为唯一权威；遇到协作强度或 WF 边界不清时，先读该文件再行动。

| 编号 | 触发 | 优先读取 |
| --- | --- | --- |
| WF-M1~M5 | 价值发现、流程与范围、交互结构、实体定义、设计与交付 | `references/workflow-contracts.md` |
| WF-T1 | 写 PRD、生成 PRD、补 PRD、整理成可开发文档 | `references/prd-protocols.md` |
| WF-T2 | review、评审、找问题、看需求是否可开发 | `references/prd-protocols.md` |
| WF-T3 | 查竞品、市场替代方案、benchmark、现成解法 | `references/research-and-competition.md` |
| WF-G1 | 定稿、输出最终版、开发交付、handoff、提 PR | `references/final-state-delivery.md`（实现交付再读 `references/implementation-delivery.md`） |
| CX-1~CX-5 | 领域约束、UI 线稿、记忆确认链、`[Meta]` 改造、发现项闭环 | `references/workflow-contracts.md` |

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
详见 `references/workflow-contracts.md` 的 CX-4。

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

修改本技能后至少执行（以技能根目录为工作目录）：

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate-confirmations.py --project <project-root> --scope <scope_id@version> --json
python3 scripts/validate-legacy-current.py --path <legacy-authoritative-document>
```

第二条命令在项目记忆模式下运行；第三条命令仅在没有确认注册表且必须依赖 legacy current 时运行。结构或状态校验失败时不得声称完成对应范围的最终状态投影。若改动了来源、许可、目录或公开说明，同步检查根 README 和本技能 README。

`validate-metadata.py`、`validate-structure.py` 由外部 `skill-craft` 工具链提供，未随本仓库分发；若宿主已提供则作为可选结构校验，不可用时跳过并说明未运行，改跑 `tests/` 与状态校验脚本。
