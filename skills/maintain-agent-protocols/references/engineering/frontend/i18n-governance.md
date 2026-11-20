# 国际化与文案治理

适用前端页面、组件、弹窗、表单、表格、菜单、Tooltip、Notification、Empty 状态、Error 状态、路由配置和其他用户可见文案。目标不是规定某个国际化库，而是约束 Agent 和开发者不得产生不可国际化的代码。

## 原则

- 用户可见文本均视为可翻译资源；业务代码中禁止直接写入展示文案。
- 国际化 Key 是稳定契约；文案允许修改，Key 不得随意变更。
- Key 必须表达业务语义，禁止使用页面位置、组件顺序或中文原文命名。
- 国际化能力必须在功能生成、修改和重构时同步维护，禁止留下需要后期整体重构才能支持多语言的实现。

## 强制约束

- CON-FE-I18N-001 硬编码文案：React/Vue/Angular/Svelte 组件、弹窗、Notification、Table、Form、路由菜单、Tooltip、Empty 状态和 Error 状态中，禁止直接出现用户可见文案；必须通过项目统一翻译入口、文案资源或等价国际化抽象获取。
- CON-FE-I18N-002 稳定 Key：国际化 Key 必须使用稳定、语义化、非展示文案的标识；禁止使用中文 Key、整句英文 Key、`page1_title`、`btn1` 等位置或顺序命名。
- CON-FE-I18N-003 业务语义命名：Key 应按业务域、对象、动作和状态组织，例如 `asset.create.submit`、`user.management.title`、`common.save_success`；不得只表达视觉位置或组件类型。
- CON-FE-I18N-004 错误信息国际化：面向用户的异常、业务错误和校验提示必须使用稳定错误码或翻译 Key；禁止直接抛出或展示硬编码用户文案。UI 层应把错误码映射为本地化文案，日志仍保留诊断上下文。
- CON-FE-I18N-005 资源同步：Agent 新增或修改页面、弹窗、表单、表格、菜单、Tooltip、Notification、Empty 状态或 Error 状态时，必须同步新增或更新 `zh-CN` 与 `en-US` 语言资源；不得只生成组件代码。
- CON-FE-I18N-006 新页面资源：新增页面或业务域入口时，必须同步新增对应业务域语言资源文件或在项目既有资源结构中补充对应命名空间；不得遗漏中文或英文任一语言。
- CON-FE-I18N-007 既有结构优先：若项目已有国际化库、目录、命名空间、加载方式或类型生成流程，必须沿用既有模式；只有缺少项目模式时，才可按业务域拆分 `locales/zh-CN/*.json` 与 `locales/en-US/*.json` 作为默认建议。
- CON-FE-I18N-008 例外边界：仅开发者日志、测试夹具、协议说明、内部注释、不可见诊断字段和明确不会进入用户界面的枚举值可不走用户文案国际化；若同一值会展示给用户，展示层仍必须国际化。

## 资源结构

优先继承项目现有目录。没有既有约定时，默认按业务域拆分：

```text
src/
└── locales/
    ├── zh-CN/
    │   ├── common.json
    │   ├── auth.json
    │   ├── dashboard.json
    │   ├── asset.json
    │   ├── gateway.json
    │   ├── honeypot.json
    │   ├── event.json
    │   ├── alert.json
    │   └── setting.json
    └── en-US/
        ├── common.json
        ├── auth.json
        ├── dashboard.json
        ├── asset.json
        ├── gateway.json
        ├── honeypot.json
        ├── event.json
        ├── alert.json
        └── setting.json
```

## Agent 执行规则

- 生成或修改 UI 代码前，先判断是否新增用户可见文案；若新增，必须同时规划 Key 和语言资源。
- 发现组件文本、弹窗标题、表格列名、表单 label、菜单名、toast、tooltip、空态或错误态硬编码时，必须自动改为国际化入口。
- 发现翻译调用缺少资源时，必须同步补齐 `zh-CN` 和 `en-US` 对应资源。
- 发现中文 Key、整句英文 Key、位置型 Key 或顺序型 Key 时，必须拒绝该命名并改为业务语义 Key。
- 生成异常、校验或业务错误时，必须优先生成稳定错误码或翻译 Key，并在 UI 层通过本地化入口展示。

## 检查与审查

执行前端国际化自检和 Code Review 时，使用 [frontend-i18n-checklist](../../checks/checklists.md)。`CHK-FE-I18N-001` 用于判断本次变更是否触发后续国际化检查；若触发后存在任一适用的合规检查项不满足，禁止提交或声明前端开发任务完成。

## 输出要求

- 说明本次是否新增用户可见文案、是否同步 `zh-CN` 和 `en-US` 资源，以及是否存在硬编码文本例外。
- 涉及新增页面、菜单、表单、表格、弹窗、Tooltip、Notification、Empty 状态或 Error 状态时，说明使用的业务域 Key 命名策略。
- 若项目尚无国际化基础设施，说明当前改动如何避免不可国际化代码，并把基础设施建设列为后续任务。
