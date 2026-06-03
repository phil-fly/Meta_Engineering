# Meta_Engineering
协作体系工程，AI 帮你设计 AI 的工作方式

## 主目录

- `skills/`：Codex 技能 hub 主目录。
- `skills/<skill-name>/SKILL.md`：每个技能的根入口文件。
- `skills/<skill-name>/agents/`：技能的 UI 元数据。
- `skills/<skill-name>/references/`：按需加载的技能参考资料。
- `skills/<skill-name>/scripts/`：技能维护或执行脚本。
- `skills/<skill-name>/templates/`：技能可复制模板资产。
- `references/`：跨技能共享参考资料，例如目标仓统一产物布局。

## 共享参考

- [`target-workspace-layout`](references/target-workspace-layout.md)：用户目标仓 AI 协作产物的统一入口目录、兼容路径和新技能接入规则。

## 技能说明索引

- [`maintain-agent-protocols`](skills/maintain-agent-protocols/README.md)：AI Agent 协作协议与规则路由的创建、审查、维护和快速使用手册。
- [`product-requirements-partner`](skills/product-requirements-partner/README.md)：产品需求讨论、价值验证、PRD、交互设计、实体定义、设计说明和开发交付协作技能。

## 开源引用

| 项目 | 来源 | 引用位置 | 许可证 | 说明 |
| --- | --- | --- | --- | --- |
| `ai-pm` | `https://github.com/SmileLiuuuu/ai-pm.git`，引入时提交 `bc3ed7c725abaa7c534129f180c01a0d0234e3fc` | `skills/product-requirements-partner/` | `CC BY-NC 4.0` | 本仓库将其改名并改造为仓库内产品需求协作技能；上游许可文本保存在 `skills/product-requirements-partner/LICENSE.upstream-ai-pm`。 |
