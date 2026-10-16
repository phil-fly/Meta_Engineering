# Meta_Engineering
协作体系工程，AI 帮你设计 AI 的工作方式

## 主目录

- `skills/`：Codex 技能 hub 主目录。
- `skills/<skill-name>/SKILL.md`：每个技能的根入口文件。
- `skills/<skill-name>/agents/`：技能的 UI 元数据。
- `skills/<skill-name>/references/`：按需加载的技能参考资料。
- `skills/<skill-name>/scripts/`：技能维护或执行脚本。
- `skills/<skill-name>/assets/`：可复制模板、前后端代码资产和其他输出资源。
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

## 版本与许可

- 技能 frontmatter 遵循宿主技能 schema，只包含 `name` 和 `description`，不含 `version` 字段；技能版本以 git 提交历史为准。
- 本仓库自身的许可尚未声明。`skills/product-requirements-partner/` 中改编自上游的部分继续受 `CC BY-NC 4.0` 约束，该许可证含非商业使用限制；对外分发前需要先确定仓库级许可。

## 本地开发

- 运行校验脚本时以**技能根目录**为工作目录，脚本从自身位置解析路径，不依赖调用时的 cwd。各技能可用命令见对应技能 README 的“常用验证”章节。
- 生成物、缓存与工具临时目录由 `.gitignore` 排除（`__pycache__/`、`.wbtmp/`、`node_modules/` 等）。
