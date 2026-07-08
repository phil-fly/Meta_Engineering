# Product Requirements Partner 使用手册

## 定位

`product-requirements-partner` 用于产品需求讨论、价值验证、PRD 编写/评审、竞品调研、UI 相关页面设计需求与线稿、交互设计、实体定义、设计说明和开发交付。

它适合在 AI 协作中承担“产品经理搭档”的角色：把模糊想法拆成可追溯的价值依据、用户旅程、范围决策、需求文档和设计交付资产。

新项目默认把产品产物放入目标仓统一入口 `ai-agent-workspace/product/`；已有项目若采用 `docs/`，可继续作为兼容真值源，但必须声明映射并避免双写。

## 快速入口

| 场景 | 你可以这样提问 | 优先读取 |
| --- | --- | --- |
| 新产品想法 | `帮我梳理这个产品想法是否值得做` | `references/strategy-foundation.md` |
| MVP 范围 | `把这个想法拆成首版 MVP 用户旅程` | `references/prd-protocols.md` |
| PRD 编写 | `写这个功能的 PRD` | `references/prd-protocols.md` |
| PRD 评审 | `评审这个 PRD，找出 blocker 和待确认项` | `references/prd-protocols.md` |
| 竞品调研 | `查一下类似产品，看看我们为什么还值得做` | `references/research-and-competition.md` |
| 页面结构 | `设计这个功能的用户流程和页面结构` | `SKILL.md` Scene 3 |
| 实体模型 | `定义这个模块的实体、状态机和字段行为` | `SKILL.md` Scene 4 |
| 设计交付 | `为这个页面生成设计说明或 mockup` | `references/design-artifacts.md`、`references/design-handoff.md` |
| 技能改造 | `[Meta] 以后需求讨论时先问目标用户` | `SKILL.md` 的 `[Meta]` 改造模式 |

## 目录说明

- `SKILL.md`：技能触发、主流程、行为边界和参考导航。
- `references/strategy-foundation.md`：立项、价值、范围和决策依据。
- `references/prd-protocols.md`：PRD 层级、命名、UI 相关页面设计需求、线稿、写作原则和评审协议。
- `references/memory-system.md`：项目记忆、初始化、TODO、决策记录和写入阈值。
- `references/workflow-contracts.md`：协作强度、Scene 契约、`[Meta]` 层级示例和闭环状态。
- `references/research-and-competition.md`：竞品调研、替代方案矩阵和证据要求。
- `references/design-artifacts.md`：设计指导文档、待定项、线稿和组件 demo。
- `references/design-handoff.md`：设计 token、静态/交互原型分层、HTML mockup 和开发交付说明。
- `LICENSE.upstream-ai-pm`：上游 `ai-pm` 项目的许可文本副本。

## 开源引用

本技能改编自以下开源项目：

| 项目 | 来源 | 引用内容 | 许可证 | 本仓库处理 |
| --- | --- | --- | --- | --- |
| `ai-pm` | `https://github.com/SmileLiuuuu/ai-pm.git`，引入时提交 `bc3ed7c725abaa7c534129f180c01a0d0234e3fc` | 产品经理 Skill 的五阶段方法、项目记忆结构、PRD/设计交付参考文档 | `CC BY-NC 4.0` | 重命名为 `product-requirements-partner`，移除外部安装脚本和宿主路径假设，保留上游许可为 `LICENSE.upstream-ai-pm` |

注意：`CC BY-NC 4.0` 含非商业使用限制。后续分发、改造或复用本技能时，应继续保留来源、许可证和变更说明。

## 维护原则

- 修改触发范围时，同步更新 `SKILL.md` frontmatter description。
- 修改产品工作法时，优先把稳定流程写入 `SKILL.md`，把细节写入 `references/`。
- 修改项目记忆、PRD 或设计产物格式时，同步更新对应 reference。
- 新增场景入口时，同步更新 `SKILL.md` 参考导航、README 快速入口和必要 reference。
- 修改目标仓产物路径时，同步参考仓库根 `references/target-workspace-layout.md`。
- 任何 `[Meta]` 改造都应先说明目标层级、目标文件和影响范围，用户确认后再写入。

## 常用验证

```bash
python3 /Users/phil-fly/Documents/GitHub/skill-craft/scripts/validate-metadata.py --path skills/product-requirements-partner
python3 /Users/phil-fly/Documents/GitHub/skill-craft/scripts/validate-structure.py --path skills/product-requirements-partner
```
