# Frontend Design System Review Prompt

用于对目标仓库执行独立、只读、可复用的前端设计系统基线调查或变更审查。

本提示语必须保持自包含：设计和开发流程可以把高频审查项前移为短门禁，但不得因此删除本提示语中的完整调查维度、逐项问题和报告契约。日常设计与开发不应重复加载本提示语全文，而应使用前端设计系统维护路由和 `CHK-FE-DS-*` 门禁。

---

# 任务：调查目标仓库的前端协议与设计规范维护体系

本阶段只允许阅读、搜索、运行非写入检查和输出报告。禁止修改、删除、新建、重命名项目文件，禁止安装依赖、调整 Token、修改 CSS、重构组件或写入审计历史。

本任务是 Reverse Engineering 当前体系，不是设计新协议。先理解目标仓库，再形成完整的现状报告。

## 0. 执行边界与证据规则

开始前先声明：

```text
审查模式：仓库级基线调查 / 指定目录审查 / 变更集审查
检查范围：
未检查范围：
结论适用范围：
```

执行期间遵守以下规则：

- 仓库级结论必须覆盖前端实现和所有已发现的规范入口；局部证据只能形成局部结论。
- 文件名、目录名、关键词、单个硬编码值和常见项目结构只能作为调查信号，不能直接升级为结论。
- 强结论必须读取真实定义、消费者、覆盖顺序和例外，并检查可能推翻或限制结论的反证。
- 实际参数必须来自代码、配置、设计资产或运行结果；示例值、模板值和通用经验不得写成项目事实。
- 未读取生产实现时，不得把设计模板断言为生产实际值；未运行页面时，不得断言响应式、交互或可访问性已经通过。
- 没有找到定义时写“未发现统一定义”或“未发现”，不要自行补值或补齐想象中的组件。

每个参数域、组件域和规则域必须标记状态：

```text
已有实际值 / 仅语义规则 / 模板占位 / 分散实现 / 未发现 / 不适用
```

## 1. 调查目标

基于目标仓库实际内容，逐项回答：

1. 前端设计规范在哪里维护；
2. UI 参数在哪里维护；
3. Design Token 在哪里维护；
4. Color 在哪里维护；
5. Typography 在哪里维护；
6. Spacing 在哪里维护；
7. Radius 在哪里维护；
8. Border 在哪里维护；
9. Shadow 在哪里维护；
10. Grid / Layout / 栅格在哪里维护；
11. Breakpoint / Responsive 在哪里维护；
12. Component 规范在哪里维护；
13. Page Layout / Page Pattern 在哪里维护；
14. Interaction / State 规范在哪里维护；
15. Accessibility 规范在哪里维护；
16. Theme 在哪里维护；
17. 前端工程规范在哪里维护；
18. AI Coding / Vibe Coding 相关规则在哪里维护；
19. Agent 通过什么机制发现和读取这些规范；
20. 规范之间是否存在继承、覆盖、扩展、优先级和例外机制。

## 2. 扫描项目结构与真实来源

不要假设目录结构。从目标仓根目录开始，检查实际存在的入口和文件。候选范围包括但不限于：

```text
AGENTS.md
CLAUDE.md
CODEX.md
README*
docs/
openspec/
spec/
specs/
.cursor/
.claude/
.codex/
.github/
frontend/
web/
ui/
app/
pages/
src/
components/
styles/
theme/
tokens/
design/
config/
package.json
tailwind.config.*
postcss.config.*
vite.config.*
next.config.*
tsconfig.*
CSS / SCSS / Less
CSS Variables
TypeScript / JavaScript Token
CSS-in-JS Theme
UI Framework 配置
Storybook 或等价组件工坊
视觉回归与 E2E 配置
Figma 或其他设计工具导出物
```

同时搜索以下实际内容：

```text
design, design system, token, color, typography, font, spacing,
radius, border, shadow, grid, layout, breakpoint, responsive,
component, ui, theme, style, visual, accessibility, frontend,
agent, vibe coding, coding rules, protocol, specification,
guideline, hardcode, deprecated, override, extend, exception
```

不要只列搜索命中。对每个候选来源继续确认：

- 它是可编辑真值源、生成文件、兼容入口、说明文档还是历史遗留；
- 它由谁读取、作用于哪些页面或组件；
- 它是否被更高优先级主题、配置或局部样式覆盖；
- 它是否仍被生产代码消费；
- 是否存在同义、重复、冲突或已废弃来源。

## 3. 建立规范来源地图

根据项目实际结构绘制来源关系，不要套用示例。至少覆盖：

```text
Agent 入口
  -> 项目协议 / Spec / ADR / 设计文档
  -> Token / Theme / 样式配置真值源
  -> 组件库 / 布局原语 / 页面模式
  -> 页面与业务组件实现
  -> Storybook / 测试 / 视觉与运行态验证
```

对每一层记录：

```text
文件或目录 | 职责 | 作用范围 | 被谁读取 | 优先级 | 派生/覆盖关系 | 例外 | 验证入口
```

同时建立参数域映射：

```text
Color -> ?
Typography -> ?
Spacing -> ?
Radius -> ?
Border -> ?
Shadow -> ?
Layout / Grid -> ?
Breakpoint / Responsive -> ?
Component -> ?
Page Pattern -> ?
Interaction / State -> ?
Accessibility -> ?
Theme -> ?
AI / Vibe Coding Rules -> ?
```

## 4. Design Token 与视觉参数

逐类记录以下字段：

```text
参数域 | Token/实际值 | 语义 | 定义位置 | 消费者 | 状态/主题 | 覆盖关系 | 结论
```

### 4.1 Color

检查是否定义及实际使用：

```text
primary
secondary
success
warning
danger
info
background
surface
text
border
disabled
hover
active
focus
selected
```

逐项回答：

1. 是语义 Token、基础 Palette、组件 Token、CSS 变量还是直接颜色值；
2. 实际值是什么，在哪个主题或作用域生效；
3. 是否存在完整 Palette 以及语义层与 Palette 的映射；
4. 是否存在 Light、Dark、高对比度或品牌主题；
5. 组件是否允许直接写 Hex、RGB、HSL 或框架颜色名；
6. Agent 是否被明确要求禁止或限制硬编码颜色；
7. hover、active、focus、selected、disabled 是否有独立语义；
8. 是否存在近似色、重复色、失效 Token 或局部覆盖。

不要把 Token 定义文件中的直接颜色值自动判为违规；必须区分 Palette 真值源与消费者硬编码。

### 4.2 Typography

调查并列出实际值：

```text
font family
font size
font weight
line height
letter spacing
heading
body
caption
label
code
数字与表格文本
fallback 与字体加载
```

检查语义样式是否集中维护，组件或页面是否绕过语义样式，以及不同视口、语言、长文本和浏览器缩放下是否有特殊规则。

### 4.3 Spacing

调查是否存在统一的基础刻度和语义间距：

```text
base scale
margin
padding
gap
page padding
section spacing
component spacing
form spacing
table/list density
```

列出实际 scale，例如项目真实存在的 `4 / 8 / 12 / ...`；不要把示例刻度当成项目事实。检查是否存在任意值、近似值、负间距、局部密度覆盖和响应式 spacing。

### 4.4 Radius

调查以下对象是否使用统一或语义化 Radius：

```text
button
input
card
modal / dialog / drawer
badge / tag
avatar
popover / tooltip
```

列出实际值、Token 映射、组件覆盖和例外。检查是否存在无语义的近似圆角或同类组件不一致。

### 4.5 Border 与 Shadow

调查 Border 的颜色、宽度、样式、状态和主题映射；调查以下对象是否存在统一 Shadow 或 elevation：

```text
card
dropdown
modal
popover
tooltip
drawer
focus ring
```

列出实际值和语义，区分边框、焦点环、分隔线、浮层层级与纯装饰阴影。

### 4.6 其他视觉参数

检查并记录实际定义、消费者和状态：

```text
motion / duration / easing
icon size / stroke / fill
z-index / elevation
density
opacity
high contrast
reduced motion
```

## 5. Layout / Grid

这是独立审查的必查项。明确项目是否集中维护以下参数及实际值：

```text
Container
Max Width
Page Padding
Grid Columns
Gutter
Header Height
Sidebar Width
Content Width
Section Gap
Form Grid
Card/List/Table Grid
Content Min/Max Width
```

同时调查 Mobile、Tablet、Desktop、Wide 或项目实际命名的 Breakpoint：

```text
名称 | 实际值 | 定义位置 | 消费者 | 布局变化 | 组件变化 | 例外
```

如果参数分散在 CSS、组件、页面或框架配置中，必须指出分散位置、重复值、覆盖关系和是否存在事实上的隐式规范。

## 6. Component 规范与状态

先从实际代码识别核心 UI Component。以下名称只能作为搜索候选，不代表项目一定存在：

```text
Button, Input, Select, Form, Table, Card, Modal, Dialog, Drawer,
Tabs, Menu, Pagination, Alert, Toast, Badge, Tag, Tooltip,
Popover, Skeleton, Empty, Date/Time Picker, Search, Filter
```

对每一个实际核心组件记录：

```text
组件 | 统一实现 | 重复实现 | 参数规范 | Variant | Size | State |
Responsive | Token 映射 | 第三方包装层 | Story/测试 | 消费者
```

重点检查以下状态是否定义并在实际实现中一致：

```text
default
hover
active
focus
selected
disabled
readonly
loading
empty
error
success
warning
权限不足
长文本
```

还要回答：

- 共享组件、页面局部组件和第三方组件包装层的边界是否清晰；
- 是否存在多个重复组件或无依据的平行组件；
- 组件默认值、Variant、Size 和 State 是否可追溯到 Token 或主题；
- 是否存在第二套 UI Framework 或绕过项目组件层的使用方式；
- 修改共享组件或默认值时是否有消费者影响和迁移机制。

## 7. Page Pattern

从实际页面中识别是否存在统一页面模式。以下仅为调查候选：

```text
List Page
Detail Page
Dashboard
Form Page
Settings Page
Wizard / Onboarding
```

对每种实际模式检查：

```text
Page Header
Breadcrumb
Title
Description
Toolbar
Search
Filter
Primary / Secondary Action
Content
Pagination
Empty State
Loading State
Error State
Permission State
```

记录页面模式的真值源、布局组件、复用方式、差异和例外，不要根据常见后台结构补齐不存在的模式。

## 8. Responsive 与真实运行行为

不要只查 Breakpoint 定义，还要检查真实组件和页面行为。至少按实际适用范围调查：

```text
Sidebar：展开 / 折叠 / Drawer / 隐藏
Table：固定列 / 横向滚动 / 卡片化 / 列裁剪
Toolbar：横向 / 换行 / 堆叠 / 溢出菜单
Grid：列数、Gutter 和密度变化
Dialog / Drawer：宽度、全屏、内部滚动
Navigation：顶部、侧边、底部或折叠行为
Form：列数、Label、操作区和错误信息变化
```

示例行为只能作为调查问题，不能作为预期设计。必须根据源码、Story、测试或实际运行页面总结。

如运行环境可用，还应验证项目要求的目标视口、最小宽度、Wide 视口、100%/125%/150% 缩放、长中文、长英文、URL、JSON、大数据量和异常状态。无法运行时说明证据限制。

## 9. Accessibility、Theme 与工程验证

调查是否存在并实际执行：

- 语义 HTML、ARIA、键盘访问、焦点顺序和焦点返回；
- focus ring、对比度、非颜色状态表达、触控目标和 reduced motion；
- Light、Dark、品牌、高对比度主题的定义、切换、持久化和组件覆盖；
- lint、typecheck、unit、integration、E2E、Storybook、视觉回归、构建和运行态检查；
- 设计文档、handoff、Storybook、Token 和生产实现之间的同步机制。

只记录目标仓实际存在或明确要求的工具与命令；未运行的验证不得写成“已通过”。

## 10. AI / Vibe Coding 机制

这是核心调查项。查清楚 Agent 如何知道项目规范，例如实际存在的：

```text
AGENTS.md
CLAUDE.md
OpenSpec / Spec
skills
rules / instructions
playbooks / routes / checks
```

查清楚 Agent 如何知道前端设计参数，例如实际存在的：

```text
frontend protocol
design-system.*
tokens.*
tailwind.config.*
theme.*
CSS Variables
component stories / docs
```

逐项判断是否存在以下约束，并给出准确来源、规范词强度和触发入口：

- 禁止或限制硬编码颜色；
- 禁止或限制硬编码 spacing 与其他视觉值；
- 优先复用 Design Token、组件和布局原语；
- 禁止重复组件；
- 禁止无依据新增 UI Framework；
- 修改全局 Token、主题、断点、布局原语和组件默认值前必须做影响分析；
- 必须执行 lint、typecheck、test、build、Storybook、视觉检查或运行态验证；
- 设计和开发流程是否能稳定读到这些规则与检查项。

区分“必须”“应”“建议”和实际没有约束。只有写在文档中但没有任务入口、流程门禁或验证方式的规则，应标为不可稳定执行，而不是自动视为已生效。

## 11. 协议优先级、继承与演进

不要假设固定层级。根据目标仓实际内容绘制协议关系，并回答：

1. 当前有哪些层级和入口；
2. 当前有没有 Inherit、Override、Extend 和 Exception；
3. 多个协议、Token、主题或组件规则冲突时谁优先；
4. Agent 是否有明确的冲突处理规则；
5. 每类参数的唯一可编辑真值源是什么；
6. 是否存在生成文件、兼容入口、设计稿或两套平行正文；
7. 新增 Token、废弃旧 Token、迁移消费者和记录例外的流程是什么；
8. 全局 Token、断点、主题和组件默认值变更如何评估消费者；
9. 设计稿、handoff、Storybook 和生产代码如何同步；
10. 历史硬编码和局部例外是否有退出条件。

可以检查类似 Global、Base、Product、Project、Frontend、Page、Component、Task 的候选层级，但最终关系图必须来自项目证据。

## 12. 问题分析

在完成来源地图、参数矩阵、组件与页面调查后再判断问题。分类包括：

### A. 缺失

相关规范、参数或机制完全没有维护。

### B. 分散

已经存在，但分散在多个位置且没有明确真值源或派生关系。

### C. 重复

多个位置重复维护同一个参数、组件或规则。

### D. 冲突

不同来源存在不一致定义，且无法从优先级或覆盖规则解释。

### E. 不可执行

只有“保持美观”“保持一致”等原则，Agent 无法据此采取确定动作。

### F. 不可验证

存在规则，但没有检查入口、验证方式或可观察结果。

### G. 粒度不足

只有基础值或名称，没有状态、主题、响应式、组件或页面级语义。

### H. Agent 风险

重点识别 AI 自行发明颜色、spacing、radius、字体、Grid、断点、组件、页面密度和 UI Framework 的风险。

每个问题必须包含：

```text
优先级：P0 / P1 / P2
类型：缺失 / 分散 / 重复 / 冲突 / 不可执行 / 不可验证 / 粒度不足 / Agent 风险
信号：触发调查的文件、关键词或现象
证据：文件、行号、配置、消费者或运行结果
影响：
反证检查：none / mitigated / contradicted / scope_limited / unknown
证据完整性：complete / partial / unresolved
结论：accepted / tentative / unresolved / rejected
建议维护位置：
```

证据不足或未检查反证时，结论最高只能是 `tentative`；证据被推翻时必须标为 `rejected`，不得继续列入已确认问题。

## 13. 最终报告

报告至少包含：

1. 检查范围、未检查范围和结论适用范围；
2. 当前协议体系：文件/目录、职责、作用范围、读取者和优先级；
3. Agent 发现与触发机制；
4. 前端规范来源地图和实际继承/覆盖关系图；
5. Color、Typography、Spacing、Radius、Border、Shadow、Layout/Grid、Breakpoint、Theme 等实际参数矩阵；
6. 组件、状态、页面模式和真实响应式行为；
7. Accessibility、工程验证和设计到生产的同步现状；
8. P0/P1/P2 问题、证据、反证、结论和建议维护位置；
9. Vibe Coding 风险：视觉不一致、参数漂移、重复组件、Layout 漂移、UI Framework 污染和 Responsive 不一致；
10. 按“设计阶段、开发预检、变更实施、验证交付、独立审查”分组的优化建议。

实际参数应尽可能列出真实值，而不是只写“存在”。如果没有统一定义，明确写：

```text
未发现统一定义
```

优化建议只给建议，不执行修改。不得在报告中把候选值、通用最佳实践或模板参数包装成项目标准。

## 14. 完成门

输出报告前检查：

```text
已分类参数域数 == 本次适用参数域总数
已确认真值源数 + 待确认真值源数 == 本次适用参数域总数
已调查核心组件数 == 本次识别的核心组件总数
已归类问题数 == 候选问题总数
P0 数 + P1 数 + P2 数 == 已确认问题总数
```

无法完成的项目必须进入“未检查范围”或“证据缺口”，不得静默省略。

报告完成后停止，等待用户决定是否进入修复阶段。
