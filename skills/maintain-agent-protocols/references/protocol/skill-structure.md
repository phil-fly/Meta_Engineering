# 技能自身结构说明

本文件说明 `maintain-agent-protocols` 技能自身为何采用多层 `references/` 和独立 `templates/` 目录，以及结构校验 warning 的处理方式。

## 结构决策

本技能是协议治理类技能，规则覆盖协议生成、规则摄入、工程路由、场景手册、检查清单和模板落盘。为降低常驻上下文成本，技能自身采用按场景加载的目录结构：

```text
references/protocol/
references/engineering/
references/scenarios/
references/checks/
references/shared/
templates/
scripts/
```

## 结构校验反证

`skill-craft` 的通用结构脚本可能提示：

- `templates/` 是 deprecated directory。
- `references/` 下存在多层目录。

这些提示对本技能不直接构成缺陷，原因是：

- `templates/` 是目标仓协议模板目录的可复制资产，新项目默认落到 `ai-agent-workspace/protocols/templates/`，旧项目可兼容 `ai-agent-protocols/templates/`；它不是执行流程引用目录。
- 多层 `references/` 是本技能按需加载的核心设计，用于避免一次性读取全部工程规则。
- `references/shared/` 保存随 Skill 安装的精确副本或当前 Skill 专用投影，避免独立安装后依赖源码仓根目录或其他 Skill。
- `SKILL.md` 已明确要求先读 `references/index.md`，再按任务场景进入对应目录。

处理规则：

- 不因通用 warning 删除 `templates/` 或压平 `references/`。
- 若模板正文变化，必须同步 `templates/` 与 `references/protocol/` 下对应模板参考文件。
- 若新增目录，必须同时更新 `SKILL.md` 的技能内部分层和 `references/index.md`。
- 若新增目标仓落盘资产，必须同时更新 `references/protocol/package-blueprint.md` 和 `scripts/protocol-package-manifest.json`。
- 若修改源码仓根级共享参考，必须同步 `references/shared/`；`scripts/check-template-sync.py` 会检查精确副本一致性，并确认专用投影具备必要章节且不依赖其他 Skill。

## 验证方式

优先运行：

```bash
python3 scripts/check-template-sync.py
node scripts/check-cross-references.ts
node scripts/check-rule-ids.ts
node scripts/check-placeholders.ts
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts -p 'test_*.py' -v
python3 scripts/protocol-package.py plan . --mode project
```

脚本不可用时，手动检查：

```bash
cmp -s templates/user-protocol.md references/protocol/user-protocol-template.md
cmp -s templates/project-protocol.md references/protocol/project-protocol-template.md
cmp -s templates/route-card.md references/protocol/route-card-template.md
```

验证通过后，仍需接受通用结构脚本对 `templates/` 和多层 `references/` 的 warning，但应在最终结果中说明这些 warning 属于本技能的显式结构例外。
