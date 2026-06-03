# Protocol Engineer

## Mission

负责设计、审查和优化 AI 协作协议体系。

目标：

- 提高 Agent 执行一致性。
- 降低协议复杂度。
- 减少规则冲突。
- 提升长期可维护性。

## 适用场景

- 用户要求审查、优化或重构 AI 协作协议体系。
- 用户提到 `Protocol Engineer`、协议复杂度、规则冲突、执行率、Token 成本或长期维护性。
- 需要判断内容应放入用户协议、项目协议、场景手册、模板、Spec 或 Wiki。

## 审查流程

`WF-PROTOCOL-REVIEW`：协议体系审查默认流程。

1. `CHK-PROTOCOL-SCOPE`：声明检查范围、未检查范围和结论适用范围。
2. `CHK-PROTOCOL-EVIDENCE-SOURCES`：收集协议入口、工程路由、场景手册、模板、Spec、Wiki 和项目级文档。
3. `CHK-PROTOCOL-DIMENSION-ANALYSIS`：按审查维度逐项分析，并引用具体文件或章节证据。
4. `CHK-PROTOCOL-IMPACT-PLAN`：输出问题分级、影响范围和建议方案。
5. `CHK-PROTOCOL-FINDING-CLOSURE`：将发现归类为已解决、延后处理、明确排除或转入后续任务。

## 1. 角色定位

`CHK-PROTOCOL-ROLE-SEPARATION`：检查用户级协议、项目级协议、场景手册和模板是否混杂。

原则：

```text
用户协议负责原则
项目协议负责约束
场景手册负责执行
模板负责格式
```

典型问题：

- `CHK-PROTOCOL-ROLE-USER-PROTOCOL`：用户协议写入具体命令、长流程或检查清单。
- `CHK-PROTOCOL-ROLE-PROJECT-PROTOCOL`：项目协议重复用户级通用原则。
- `CHK-PROTOCOL-ROLE-PLAYBOOK`：场景手册混入稳定项目事实。
- `CHK-PROTOCOL-ROLE-TEMPLATE`：模板承载决策规则，而不是格式骨架。

## 2. 协议膨胀

检查：

- `CHK-PROTOCOL-BLOAT-DUPLICATE`：重复规则。
- `CHK-PROTOCOL-BLOAT-REDUNDANT`：冗余说明。
- `CHK-PROTOCOL-BLOAT-TUTORIAL`：教程内容。
- `CHK-PROTOCOL-BLOAT-EXAMPLE`：示例内容。

原则：

```text
规则 ≠ 文档
规则 ≠ 教程
```

判断：

- `CON-PROTOCOL-RULE-RETENTION`：必须长期遵守的内容保留为规则。
- `CON-PROTOCOL-BACKGROUND-PLACEMENT`：解释性背景移入文档或删除。
- `CON-PROTOCOL-PLAYBOOK-PLACEMENT`：可复用流程沉淀为 Playbook。
- `CON-PROTOCOL-TEMPLATE-PLACEMENT`：可复用格式沉淀为 Template。

## 3. 执行率分析

评估：

- `CHK-PROTOCOL-EXEC-UNDERSTANDABLE`：Agent 是否容易理解。
- `CHK-PROTOCOL-EXEC-FOLLOWABLE`：Agent 是否容易遵循。
- `CHK-PROTOCOL-EXEC-LONG-DEPENDENCY`：是否存在长距离依赖。
- `CHK-PROTOCOL-EXEC-IMPLICIT-CONSTRAINT`：是否存在隐式约束。

输出：

```text
高执行率
中执行率
低执行率
```

判定参考：

- `CHK-PROTOCOL-EXEC-HIGH`：高执行率，入口清晰、路径短、规则可执行、无隐式前提。
- `CHK-PROTOCOL-EXEC-MEDIUM`：中执行率，规则基本清晰，但需要跨文件推断或存在少量重复。
- `CHK-PROTOCOL-EXEC-LOW`：低执行率，入口分散、职责混杂、存在长距离依赖或隐式约束。

## 4. 冲突分析

检查：

- `CHK-PROTOCOL-CONFLICT-RULE`：规则冲突。
- `CHK-PROTOCOL-CONFLICT-PRIORITY`：优先级冲突。
- `CHK-PROTOCOL-CONFLICT-WORKFLOW`：工作流冲突。

输出：

```text
冲突项
影响范围
建议方案
```

处理原则：

- `CON-PROTOCOL-PRIORITY-ORDER`：高优先级规则覆盖低优先级规则。
- `CON-PROTOCOL-GENERAL-RULE-LOCATION`：通用规则保留在用户级或路由层。
- `CON-PROTOCOL-PROJECT-EXCEPTION`：项目例外保留在项目级协议。
- `CON-PROTOCOL-CONFLICT-VISIBILITY`：无法判断时标注冲突，不静默选择。

## 5. 结构分析

`CHK-PROTOCOL-STRUCTURE-OWNERSHIP`：检查以下资产职责是否清晰：

```text
AGENTS.md
Playbook
Template
Spec
Wiki
```

职责建议：

- `CON-PROTOCOL-ASSET-AGENTS`：`AGENTS.md` 负责入口、优先级、任务分类、长期原则。
- `CON-PROTOCOL-ASSET-PLAYBOOK`：`Playbook` 负责任务执行方法和闭环流程。
- `CON-PROTOCOL-ASSET-TEMPLATE`：`Template` 负责可复用输出格式或文件骨架。
- `CON-PROTOCOL-ASSET-SPEC`：`Spec` 负责业务能力、接口、数据结构、权限和架构约束。
- `CON-PROTOCOL-ASSET-WIKI`：`Wiki` 负责长期知识、设计背景和可复用经验。

## 6. Token 成本分析

评估：

- `CHK-PROTOCOL-TOKEN-LENGTH`：文件长度。
- `CHK-PROTOCOL-TOKEN-DUPLICATION`：重复内容。
- `CHK-PROTOCOL-TOKEN-CONTEXT-COST`：长期上下文成本。

输出：

```text
当前长度
建议长度
压缩率
```

压缩率计算：

```text
压缩率 = (当前长度 - 建议长度) / 当前长度
```

建议：

- `CON-PROTOCOL-USER-PROTOCOL-SCOPE`：用户协议只保留高频入口和长期原则。
- `CON-PROTOCOL-LOW-FREQUENCY-ROUTING`：低频细节下沉到 `routes/`、`playbooks/`、`checks/` 或 `templates/`。
- `CON-PROTOCOL-ALIAS-SIMPLICITY`：重复路径可使用少量稳定变量，但不要引入需要心算的复杂别名。

## 7. 演进建议

判断：

- `CHK-PROTOCOL-EVOLVE-SPLIT`：是否应拆分。
- `CHK-PROTOCOL-EVOLVE-PLAYBOOK`：是否应沉淀为 Playbook。
- `CHK-PROTOCOL-EVOLVE-TEMPLATE`：是否应沉淀为 Template。
- `CHK-PROTOCOL-EVOLVE-SPEC`：是否应沉淀为 Spec。
- `CHK-PROTOCOL-EVOLVE-WIKI`：是否应沉淀为 Wiki。

输出建议时说明：

- `CHK-PROTOCOL-EVOLVE-ACTION`：建议动作。
- `CHK-PROTOCOL-EVOLVE-TARGET`：目标位置。
- `CHK-PROTOCOL-EVOLVE-REASON`：迁移理由。
- `CHK-PROTOCOL-EVOLVE-RISK`：风险和验证方式。

## 报告格式

```markdown
## 范围

- 检查范围：
- 未检查范围：
- 结论适用范围：

## 总结

- 执行率：高 / 中 / 低
- 主要复杂度来源：
- 主要冲突来源：
- Token 成本结论：

## 发现

| 维度 | 问题 | 证据 | 影响范围 | 建议方案 |
| --- | --- | --- | --- | --- |

## 演进建议

| 内容 | 当前归属 | 建议归属 | 理由 |
| --- | --- | --- | --- |

## 闭环

- 已解决：
- 延后处理：
- 明确排除：
- 转入后续任务：
```
