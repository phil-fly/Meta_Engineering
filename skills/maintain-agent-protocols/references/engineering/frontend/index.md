# 前端工程入口

前端、UI、页面、组件、交互、表单、Design Token、紧凑布局、国际化、文案治理、JavaScript、TypeScript、导航、权限渲染和前端请求任务先读本文件。

## 文件

- `ui-development.md`：UI 开发总览。
- `javascript-typescript.md`：JavaScript/TypeScript 类型边界、异步生命周期、状态、依赖和验证规则。
- `api-and-data.md`：前端请求、真实筛选、按需加载。
- `list-query.md`：列表查询接口组合路由与查询类型分类策略。
- `form-validation.md`：提交型表单、字段校验、错误展示和服务端业务错误保留。
- `i18n-governance.md`：国际化、文案资源、翻译 Key、硬编码文案和错误信息本地化。
- `design-tokens.md`：颜色 token、语义色、状态色和局部视觉范围控制。
- `compact-ui.md`：首屏核心任务可见、布局密度、文案压缩、图表高度和留白节奏。
- `layering-and-size.md`：分层、文件规模、函数规模、props 控制。
- `navigation-and-state.md`：导航、路由状态、命名和页面状态。
- `interaction-and-permission.md`：交互、格式化、小眉标、高影响操作和权限渲染。

## 关联

- 列表、表格、选择器、枚举、远程搜索：先读取 `list-query.md`。
- 提交型表单、弹窗表单、配置表单和表单错误展示：先读取 `form-validation.md`。
- 页面、弹窗、表单、表格、菜单、Tooltip、Notification、Empty 状态、Error 状态或任何用户可见文案：读取 `i18n-governance.md`。
- 颜色、主题、品牌色、状态色、中性色和视觉 token：先读取 `design-tokens.md`。
- 首屏核心任务、紧凑布局、图表高度、重复文案和容器层级压缩：先读取 `compact-ui.md`。
- JavaScript、TypeScript、JSX、TSX、Electron 渲染进程和前端构建脚本：读取 `javascript-typescript.md`。
- 列表查询、响应契约：读取 `../core/api-design.md`。
- 前端权限和后端权限边界：读取 `../core/auth-and-permission.md`。
- 通用质量、命名和注释规范：读取 `../core/common-quality.md`。
- 高影响操作：读取 `../security/index.md`。
