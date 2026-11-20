# 前端组件系统

适用共享组件、页面局部组件、第三方组件包装、组件库、headless 组件、Storybook 或等价组件工坊、组件文档和组件状态示例。

## 核心约束

- CON-FE-COMPONENT-001 复用先查：新增共享组件前必须先检查项目已有组件、组合模式、配置扩展、样式 token 和第三方包装层；能复用或扩展时不应创建同义组件。
- CON-FE-COMPONENT-002 局部优先：只服务单页、单弹窗或单流程的 UI 应优先作为页面局部组件；只有语义稳定且跨场景复用时才提升为共享组件。
- CON-FE-COMPONENT-003 第三方包装：第三方 UI 组件应通过项目组件层适配业务默认值、主题、i18n、a11y、错误状态和埋点；业务页面不应到处散落第三方库细节。
- CON-FE-COMPONENT-004 组合优先：组件 props 过多、状态分支过多或 slot 语义复杂时，应优先用组合组件、配置对象、上下文边界或子组件拆分，而不是继续追加参数。
- CON-FE-COMPONENT-005 状态覆盖：共享组件应覆盖默认、hover、focus、disabled、loading、empty、error、success、长文本、移动端和权限不可见等关键状态。
- CON-FE-COMPONENT-006 组件工坊：如项目使用 Storybook、文档站、playground 或等价组件工坊，高复用组件新增或显著改动时应同步示例、状态和使用说明；未使用时说明替代验证方式。

## 关联路由

- 文件规模、函数规模和 props 控制：读取 `layering-and-size.md`。
- 可访问性：读取 `accessibility.md`。
- 样式 token 和视觉语义：读取 `styling-and-tokens.md`。
- 国际化和用户文案：读取 `i18n-governance.md`。
- 长文本、卡片高度、运行态 UI 稳定性和极限数据：读取 `ui-stability.md`。
- 前端测试和视觉状态：读取 `testing.md`。

## 输出要求

- 说明本次选择复用、扩展、包装、局部组件还是新共享组件。
- 说明共享组件的复用场景、状态覆盖、a11y、i18n 和 token 关系。
- 涉及卡片、表格、表单、浮层或长文本组件时，说明 UI 稳定性和极限内容状态。
- 说明是否同步组件工坊、文档、示例或替代验证。
