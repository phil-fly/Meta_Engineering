# 协议场景入口

协议生成、协议维护、协议审查和协议转换任务先读本文件。

## 读取顺序

1. 读取 `guide.md` 判断目标层级、目录结构和用户协议入口规则。
2. 如涉及协议工程审查、执行率、Token 成本、协议膨胀或冲突分析，再读取 `protocol-engineer.md`。
3. 如涉及原则、约束、执行流程、模板、检查项或知识摄入，再读取 `rule-ingestion.md`。
4. 如涉及 OpenSpec、Spec-first、规范驱动开发、审查修复闭环或 Epic/Subtask 拆分，再读取 `openspec-workflow.md`。
5. 如涉及完整协议包落盘、模板目录、playbooks 内容来源或目标仓文件生成，再读取 `package-blueprint.md`。
6. 如涉及本技能自身目录结构、`templates/` 目录或结构校验 warning 处理，再读取 `skill-structure.md`。
7. 如创建或补充用户级协议，再读取 `user-protocol-template.md`。
8. 如创建或补充项目级协议，再读取 `project-protocol-template.md`。
9. 如创建或补充路由模板，再读取 `route-card-template.md`。
10. 如涉及用户协作边界、模式切换、确认门槛、证据范围或完成定义，再读取 `collaboration-boundaries.md`。
11. 如涉及工程规则路由，再读取 `../engineering/index.md`。
12. 如涉及任务流程，再读取 `../scenarios/playbooks.md`。
13. 如涉及审查验收，再读取 `../checks/checklists.md`。

## 适用任务

- 创建用户级 AI Agent 协作协议。
- 补充或裁剪用户级协议模板。
- 创建项目级 AI Agent 协作协议。
- 补充或裁剪项目级协议模板。
- 以 Protocol Engineer 视角审查协议体系执行率、复杂度、冲突和 Token 成本。
- 摄入原则、约束、执行流程、模板、检查项或知识，并判断维护位置与触发入口。
- 维护 OpenSpec / Spec-first 工作流，并对齐规范前置、变更闭环、审查闭环和 Epic 拆分。
- 维护 `ai-agent-protocols/` 目录结构。
- 生成或补齐 `templates/`、`playbooks/`、`routes/` 或 `checks/` 文件内容。
- 解释或处理本技能自身结构校验 warning。
- 审查用户协议是否混入执行细节。
- 把零散规则转换为协议入口、工程路由、场景手册或检查清单。
- 维护用户与 Agent 的协作边界、工作模式、确认门槛和完成定义。
