# 前端项目结构

适用前端目录组织、feature 模块边界、共享层、文件命名、导入方向、代码移动和新增文件落点判断。框架可为 React、Vue、Angular、Svelte、Electron 渲染进程或项目自定义前端框架。

## 核心约束

- CON-FE-STRUCTURE-001 既有结构优先：新增或移动前端文件前必须先识别项目既有目录、别名、组件层、路由层和测试布局；没有项目证据时，只能采用条件建议，不得把某个模板目录写成项目事实。
- CON-FE-STRUCTURE-002 模块边界：如项目采用 feature-based structure，feature 内代码应优先收拢在本 feature 的 `api`、`components`、`hooks`、`stores`、`types`、`utils` 或等价目录；跨 feature 复用必须先提升到共享层或应用编排层。
- CON-FE-STRUCTURE-003 单向依赖：共享层可被 feature 和 app 层引用，feature 层不应反向依赖 app 层；feature 之间默认不直接互引，应由 app、route、workflow 或组合层完成编排。
- CON-FE-STRUCTURE-004 共享层准入：新增共享组件、Hook、service、utils 或类型前，应确认至少存在明确复用场景、稳定语义和维护边界；一次性页面逻辑优先留在页面或 feature 内。
- CON-FE-STRUCTURE-005 命名一致：文件名、组件名、Hook 名、store 名和实际职责必须一致；移动公共能力时应同步更新导入、路由注册、测试、文档和类型引用。
- CON-FE-STRUCTURE-006 直接导入优先：如项目构建或 tree shaking 对 barrel file 敏感，默认直接导入目标模块；只有项目已有稳定导出约定时才沿用 barrel file。

## 默认落点判断

```text
只服务单个页面或弹窗        → 页面局部目录或当前 feature 内
服务同一业务域多个页面      → feature 内 components/hooks/stores/api
跨业务域复用且语义稳定      → shared components/hooks/utils/types
承载应用初始化、provider、路由 → app 或 framework 约定目录
封装请求客户端、监控、SDK    → lib、services 或项目既有基础设施目录
测试工具、mock、fixture      → testing、__tests__ 或项目既有测试目录
```

## 关联路由

- 组件复用和第三方组件包装：读取 `component-system.md`。
- 文件规模、函数规模和 props 控制：读取 `layering-and-size.md`。
- 工具链、路径别名和验证入口：读取 `tooling-and-verification.md`。
- 通用命名、注释和悬空引用：读取 `../core/common-quality.md`。

## 输出要求

- 说明本次新增或移动文件的落点、所属层级和复用边界。
- 说明是否存在跨 feature 导入、共享层反向依赖、命名漂移或 barrel file 风险。
- 说明已同步的导入、路由注册、测试、文档或类型引用；无法同步时说明剩余风险。
