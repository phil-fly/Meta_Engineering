# 前端工程入口

前端、UI、页面、组件、交互、表单、Design Token、紧凑布局、UI 稳定性、国际化、文案治理、JavaScript、TypeScript、导航、权限渲染、前端请求、项目结构、状态缓存、测试、可访问性、工具链和前端性能任务先读本文件。

## 文件

- `ui-development.md`：前端开发总检查摘要，不作为路由索引。
- `project-structure.md`：前端目录、feature 边界、共享层、导入方向和命名。
- `component-system.md`：共享组件、页面局部组件、第三方组件包装、组件工坊和复用边界。
- `javascript-typescript.md`：JavaScript/TypeScript 类型边界、异步生命周期和安全输入规则。
- `api-and-data.md`：前端请求、真实筛选、按需加载。
- `state-and-cache.md`：组件状态、应用状态、服务端缓存、表单状态、URL 状态和缓存失效。
- `list-query.md`：列表查询接口组合路由与查询类型分类策略。
- `form-validation.md`：提交型表单、字段校验、错误展示和服务端业务错误保留。
- `i18n-governance.md`：国际化、文案资源、翻译 Key、硬编码文案和错误信息本地化。
- `styling-and-tokens.md`：颜色、间距、字号、圆角、阴影、motion 和组件 token。
- `design-tokens.md`：颜色 token 兼容入口。
- `compact-ui.md`：首屏核心任务可见、布局密度、文案压缩、图表高度和留白节奏。
- `ui-stability.md`：运行态 UI 稳定性、多分辨率、浏览器缩放、长文本、表格列宽、浮层溢出和极限数据验收。
- `layering-and-size.md`：分层、文件规模、函数规模、props 控制。
- `navigation-and-state.md`：导航、路由状态、命名和页面状态。
- `interaction-and-permission.md`：交互、格式化、小眉标、高影响操作和权限渲染。
- `accessibility.md`：键盘、焦点、ARIA、语义、复杂组件可访问性和 a11y 自检。
- `testing.md`：单元、集成、E2E、MSW、用户行为测试和验证边界。
- `tooling-and-verification.md`：ESLint、Prettier、TypeScript、typecheck、lint、test、build、CI 和依赖验证。
- `frontend-performance.md`：首屏、code splitting、bundle、资源、预取、渲染频率和 Web Vitals。

## 关联

- 列表、表格、选择器、枚举、远程搜索：先读取 `list-query.md`。
- 提交型表单、弹窗表单、配置表单和表单错误展示：先读取 `form-validation.md`。
- 页面、弹窗、表单、表格、菜单、Tooltip、Notification、Empty 状态、Error 状态或任何用户可见文案：读取 `i18n-governance.md`。
- 前端目录、新文件落点、feature 边界、共享层、路径别名和导入方向：读取 `project-structure.md`。
- 共享组件、页面局部组件、第三方组件包装和 Storybook：读取 `component-system.md`。
- 状态拥有者、服务端缓存、URL 状态、缓存失效和本地持久化：读取 `state-and-cache.md`。
- 颜色、主题、品牌色、状态色、中性色、间距、字号、圆角、阴影、motion 和视觉 token：读取 `styling-and-tokens.md`；只涉及历史颜色 token 时可读取 `design-tokens.md`。
- 首屏核心任务、紧凑布局、图表高度、重复文案和容器层级压缩：先读取 `compact-ui.md`。
- UI 稳定性、分辨率、浏览器缩放、长文本、表格列宽、Dialog/Drawer 溢出、极限数据或运行态 UI Review：读取 `ui-stability.md`。
- JavaScript、TypeScript、JSX、TSX、Electron 渲染进程和前端构建脚本：读取 `javascript-typescript.md`。
- 键盘、焦点、ARIA、复杂组件、只靠颜色表达状态或紧凑布局可访问性：读取 `accessibility.md`。
- 单元、集成、E2E、mock server、用户行为测试和回归验证：读取 `testing.md`。
- ESLint、Prettier、TypeScript、typecheck、lint、test、build、CI、依赖和路径别名：读取 `tooling-and-verification.md`。
- 首屏、路由级 code splitting、bundle、图片字体、预取、渲染频率或 Web Vitals：读取 `frontend-performance.md`。
- 列表查询、响应契约：读取 `../core/api-design.md`。
- 前端权限和后端权限边界：读取 `../core/auth-and-permission.md`。
- 通用质量、命名和注释规范：读取 `../core/common-quality.md`。
- 高影响操作：读取 `../security/index.md`。
