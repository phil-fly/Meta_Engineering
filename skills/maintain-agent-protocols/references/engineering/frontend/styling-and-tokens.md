# 样式语义与 Design Token

适用颜色、间距、字号、行高、圆角、阴影、边框、背景、motion、组件 token、主题变量和局部视觉改动。

## 核心约束

- CON-FE-STYLE-001 Token 优先：产品 UI 样式应优先通过 Design Token、主题变量、组件变量或项目既有语义变量表达；避免在页面和组件内扩散硬编码视觉值。
- CON-FE-STYLE-002 语义明确：颜色、间距、字号、圆角、阴影、motion 和组件 token 必须具备明确语义和适用场景；不得新增与现有 token 同义或冲突的值。
- CON-FE-STYLE-003 状态一致：success、warning、danger、info、disabled、selected、muted、background、border 和 text 等状态语义应全项目一致；同一状态不得在不同页面表达相反含义。
- CON-FE-STYLE-004 局部控制：修改页面时默认只处理本次范围内的样式问题；全局 token、主题或组件默认值变更必须说明影响范围和回归验证。
- CON-FE-STYLE-005 可访问视觉：颜色对比、焦点样式、错误态、禁用态和高影响操作必须满足可读、可辨、可键盘感知的最低要求；禁止只靠颜色表达重要状态。
- CON-FE-STYLE-006 例外隔离：图表色板、品牌插画、第三方嵌入、截图复刻、临时调试色和一次性营销视觉可以作为例外，但不得污染通用 UI token。
- CON-FE-STYLE-007 技术栈条件：Tailwind、CSS Modules、CSS-in-JS、vanilla-extract、Sass 或组件库主题均为条件实现；应继承项目现状，不把某个方案写成通用强制规则。

## 关联路由

- 历史颜色 token 规则兼容：读取 `design-tokens.md`。
- 可访问性：读取 `accessibility.md`。
- 组件系统：读取 `component-system.md`。
- 紧凑布局：读取 `compact-ui.md`。
- 前端性能和运行时样式成本：读取 `frontend-performance.md`。

## 输出要求

- 说明本次样式来自哪个 token、主题变量、组件变量或项目语义变量。
- 说明是否新增或修改 token；若是，说明语义、适用场景、影响范围和回归验证。
- 说明状态色、焦点、禁用、错误和对比度是否保持一致与可访问。
