# Final-State Delivery Reference

本参考用于把当前有效需求投影成干净的 PRD 或需求 handoff。确认记录 schema 与写入规则统一由 `references/memory-system.md` 定义；用户要求实现摘要、开发 handoff 或 PR 文案时，再读取 `references/implementation-delivery.md`。

## 先确定交付坐标

开始前明确两件事：

- **目标范围**：一个稳定的 `Scope/Version`，格式为 `scope_id@version`。无法确定目标版本时先询问，不能从多个 active 版本中猜“最新”。
- **交付类型**：需求交付、实现交付，或两者都有。实现交付必须额外执行 `implementation-delivery.md`。

只做对话整理且用户没有要求落盘时，不初始化项目记忆，也不因为缺少 `CONFIRMATIONS.md` 把回答降级为草案。

## 当前状态权威顺序

对目标 `Scope/Version` 内的同一 `Requirement ID`，按以下顺序判断当前状态：

1. 当前对话中对象、范围和结论都明确的用户指令。
2. 通过校验的确认记录当前快照。
3. 当前 active 决策及权威 PRD、设计或 handoff 中未被更新的内容。
4. Context、Session、旧版本和批注，仅作为证据或冲突线索。

当前用户指令可以在本轮立即成为权威输入；持久化是交付动作，不是用户意图成立的前提。若当前指令明确替代同键旧结论，直接使用新结论，不要求重复确认。若对象、范围、条件或替代关系不清，标记 `unresolved` 并询问。

进入项目记忆模式且要写入长期产物时，先处理确认事务：已有记录时先校验基线，再追加本轮新增、修改、延期或撤回并重新校验；新项目的空注册表先写入首条 `add`，再执行首次校验。确认状态通过后才更新 PRD、设计或 handoff。若用户明确禁止修改记忆文件，遵守该限制，并在交付说明中标记 `Persistence: not recorded`；不得声称已同步项目记忆。

## 确认状态投影

确认记录采用线性快照链，具体 schema 见 `references/memory-system.md`：

- `Requirement ID + Scope/Version` 是重建键，`Object` 只是展示标题。
- 每个键以一个 `add` 开始；后续记录必须通过 `Supersedes` 指向紧邻的上一条记录。
- 每条记录的 `Accepted conclusion` 都是该事件生效后的完整当前结论。`patch` 的 `Affected fields` 只说明变化位置，不承担自然语言字段合并。
- 每个键必须恰好有一个 `active`，且它必须是时间最新的记录。

项目根目录已知时运行：

```bash
python3 skills/product-requirements-partner/scripts/validate-confirmations.py \
  --project <project-root> --scope <scope_id@version> --json
```

脚本会在规范路径和兼容路径之间解析唯一来源。两份 `CONFIRMATIONS.md` 同时存在时视为 split-brain，必须先迁移到单一来源；不得任选其一。空注册表、断裂链、零个或多个 active、无目标范围状态都会校验失败。

若项目没有确认注册表且必须依赖已有历史产物，只能使用通过 `scripts/validate-legacy-current.py` 校验的唯一 `legacy-current` 基线。它只证明基线未变，不代表新的用户确认。无 `Status` 的旧决策也只有在该标记覆盖、没有后续确认或同范围冲突时才可按 active 解释。

## 定稿流程

1. **锁定坐标**：确定交付类型和唯一 `Scope/Version`。
2. **收集本轮权威输入**：提取当前用户明确新增、修改、延期或撤回的结论；模糊短语只能绑定到唯一、单独呈现的结论。
3. **登记并投影状态**：项目记忆模式按上方确认事务处理本轮变化，再运行状态投影；没有本轮变化时直接投影已有状态。无注册表且需依赖旧产物时运行 legacy 校验。
4. **解决冲突**：同键明确替代直接更新；键、范围、条件或替代关系不清时停止并询问。
5. **生成需求交付**：只保留当前 `confirmed`、本版本 `deferred` 和仍影响本次范围的 `pending`。
6. **路由实现交付**：用户要求实现摘要、开发 handoff 或 PR 文案时，转入 `implementation-delivery.md` 核对 diff 与验证结果。
7. **清理并同步**：删除过程残留；需要落盘且获授权时，把已通过投影的当前状态同步到权威产物。

## 需求状态

| 状态 | 判定 |
| --- | --- |
| `Draft` | 仍有未确认内容或 blocking pending |
| `Ready for development` | blocking pending 为 0，且目标范围无未解决冲突 |

需求状态与实现状态独立。`Ready for development` 只代表需求可开发，不能证明代码已经实现或验证。

## 可执行验收

交付前逐项检查：

- 目标范围中的每条需求声明都有稳定 `Requirement ID`，并能指向本轮明确指令、当前 `CONF-*` 或合法 legacy 基线。
- 当前版本 `deferred` 和 `pending` 都有稳定 ID；pending 还要有 `blocking/non-blocking`、影响和后续时机。
- 标题与摘要中的每项产品能力都能映射到当前需求。
- 未映射需求声明和未经准入的过程残留均为 0。

## Pending 与负向范围

| 类型 | 处理 |
| --- | --- |
| `blocking` pending | 会改变验收、核心旅程、权限/数据契约、安全合规、迁移回滚或可测试性；阻止需求 Ready |
| `non-blocking` pending | 只影响文案、视觉细节或非核心优化，且有负责人或处理时机 |
| 用户确认的本版本 Out/Deferred | 可写入版本边界，不要求证明为永久边界 |
| 长期产品边界 | 仅在用户确认长期有效，且影响验收、兼容、安全或对外承诺时保留 |
| 被拒绝的 Agent 建议 | 移出当前产物，必要时只留在历史或决策记录 |

无法判断 pending 影响时默认 `blocking`。任何负向范围都用产品语言表达，不描述 Agent 曾建议什么或用户后来删了什么。

## 交付文本规则

- 当前正文不保留已解决批注、Answer、划线旧文、被替代方案或 Agent 执行过程。
- 标题按最终交付能力命名，不按删除项或纠错过程命名。
- 注释只解释当前仍成立的意图、约束或非显然原因。
- 用户要求决策历史时，单独提供决策记录或附录，不混入实现与验收正文。

## 失败处理

- 目标 `Scope/Version` 不明确、确认源 split-brain、状态链校验失败或当前状态冲突：停止对应范围定稿，列出冲突与所需决定。
- 权威产物不可读：标记 `unresolved`，不得声称完成一致性整理。
- 用户禁止持久化：不写记忆文件，明确持久化状态，但继续完成获授权的对话交付。

## 回归要求

确认状态的结构回归由 `tests/test_confirmation_state.py` 覆盖。每次修改本交付链后还要人工演练：

| 场景 | 预期结果 |
| --- | --- |
| 当前用户明确替代旧结论 | 本轮立即采用新结论；需长期落盘时追加快照，不重复追问 |
| 模糊的“好，提 PR”对应多个候选 | 只授权动作，需求保持 `unresolved` |
| 旧决策无 `Status` 且无合法 legacy 标记 | 不得视为 active |
