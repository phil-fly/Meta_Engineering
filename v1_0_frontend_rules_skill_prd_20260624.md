# PRD: 前端规则技能补强与拆分优化

版本：v1.0
日期：2026-06-24
状态：已完成
目标仓库：Meta_Engineering
目标技能：`skills/maintain-agent-protocols`

## 1. 背景与价值范围

### 1.1 背景

当前 `maintain-agent-protocols` 已经具备较完整的协议工程分层，前端规则集中在 `skills/maintain-agent-protocols/references/engineering/frontend/`。现有前端规则已经覆盖列表查询、表单校验、国际化、Design Token、紧凑 UI、分层规模控制、导航状态、交互权限和 JS/TS 基础边界。

上一轮调研对比了多个高星且仍活跃的前端工程项目和规范项目，包括：

- `airbnb/javascript`：JavaScript 风格、lint 规则、测试和性能章节。
- `alan2207/bulletproof-react`：生产级前端应用结构、API 层、状态管理、测试、安全、性能和部署。
- `shadcn-ui/ui`：可复制、可定制、可扩展的组件库构建思路。
- `storybookjs/storybook`：组件隔离开发、文档、交互测试、a11y 和视觉回归。
- `ant-design/ant-design`：企业级 UI 组件、TypeScript、国际化、主题能力和开发工具链。
- `tailwindlabs/tailwindcss`：utility-first 样式体系和快速 UI 构建。
- `prettier/prettier`、`eslint/eslint`、`typescript-eslint/typescript-eslint`：格式化、静态检查和 TypeScript lint 工具链。
- `testing-library/react-testing-library`：面向用户行为的组件测试原则。
- `radix-ui/primitives`：可访问、可定制的 headless 组件基础能力。

调研结论显示，当前仓库前端规则的优势在于“业务前端场景约束”较强，但在现代前端项目规范的外围工程能力上仍有缺口：项目结构、组件系统、可访问性、测试、性能预算、状态与服务端缓存、工具链和构建发布尚未形成独立入口。

### 1.2 目标用户

- 维护 `maintain-agent-protocols` 技能的协议工程师。
- 使用该技能生成或审查前端工程路由的 AI Agent。
- 需要把前端工程经验沉淀为可路由、可验证规则的开发者。

### 1.3 核心价值

让前端规则技能从“若干前端细则集合”升级为“现代前端工程规则路由体系”，使 Agent 在处理前端任务时能：

- 更快判断该读哪个前端子路由。
- 更少把组件、状态、请求、测试和可访问性规则混在一起。
- 更容易输出可验证的变更说明和验收结果。
- 更好继承高星项目里的成熟经验，但不把具体框架偏好误写成通用强制规则。

### 1.4 MVP 边界

#### MVP 支持

- 新增前端规则子路由，用于补齐项目结构、状态缓存、测试、可访问性、组件系统、性能和工具链。
- 调整前端入口索引，保证新增路由可发现。
- 拆分或改写现有描述中职责混杂的前端规则。
- 补充前端检查清单，支撑审查和验收。
- 保留现有强规则，如 i18n、真实后端筛选、表单错误分层、权限边界和 Design Token。

#### MVP 不支持

- 不直接实现具体业务前端项目代码。
- 不绑定 React、Vue、Angular、Svelte、Next.js、Vite、Tailwind、Ant Design 或 shadcn/ui 为默认强制技术栈。
- 不整段搬运外部项目 README 或文档。
- 不改用户级协议入口，除非后续确认前端规则需要提升为高频用户级入口。
- 不引入外部自动化脚本作为本次必需交付。

## 2. 关键用户旅程

### Journey A: 维护者补充前端工程规则

维护者准备把调研结果沉淀到技能中。他先打开前端入口索引，确认哪些任务应该触发哪些子路由。随后将“项目结构”“状态缓存”“测试”“可访问性”等高价值规则拆成独立文件，并在入口索引中补齐路由说明。完成后，维护者运行现有结构检查脚本，确认新增文件没有悬空引用、占位符或重复编号。

期望结果：新增规则能被 Agent 找到，且每条规则都有明确适用范围、触发条件、输出要求和验证方式。

### Journey B: Agent 处理一个前端开发任务

Agent 收到“优化列表页筛选和状态同步”的任务。它先读 `engineering/index.md`，再进入 `frontend/index.md`。根据任务特征，它读取 `list-query.md`、`api-and-data.md` 和新增的 `state-and-cache.md`。实施或建议时，它说明筛选是否由后端支持、URL 状态和服务端缓存如何同步、loading/error/success/cleanup 是否覆盖。

期望结果：Agent 不再只凭 UI 表面改动处理问题，而是能覆盖数据、状态和验证闭环。

### Journey C: Reviewer 审查前端规则质量

Reviewer 要确认本技能的前端规则是否可执行。他从前端检查清单开始，逐项核对可访问性、测试、性能、组件系统、i18n 和权限边界。发现某些规则只是建议但被写成“必须”，或某些技术栈规则缺少条件前提，则标为 clarification 或 suggestion，并回到对应路由修正。

期望结果：审查结论能定位到具体文件和规则编号，问题不会在后续编辑中消失。

## 3. 路由结构需求

### 3.1 新增路由

| 编号 | 路由文件 | 优先级 | 说明 |
| --- | --- | --- | --- |
| FE-ROUTE-001 | `project-structure.md` | P0 | 前端目录、feature 边界、共享层、导入方向、命名和跨 feature 依赖。 |
| FE-ROUTE-002 | `state-and-cache.md` | P0 | 组件状态、应用状态、服务端缓存、表单状态、URL 状态、状态拥有者。 |
| FE-ROUTE-003 | `testing.md` | P0 | 单元、集成、E2E、MSW、用户行为测试、测试边界和验证输出。 |
| FE-ROUTE-004 | `accessibility.md` | P0 | 键盘、焦点、ARIA、语义、Dialog/Menu/Tooltip 可访问性和 a11y 自检。 |
| FE-ROUTE-005 | `tooling-and-verification.md` | P0 | ESLint、Prettier、TypeScript、typecheck、lint、test、build、CI 和 pre-commit。 |
| FE-ROUTE-006 | `component-system.md` | P1 | 共享组件、页面局部组件、第三方组件包装、Storybook、组件文档和复用边界。 |
| FE-ROUTE-007 | `frontend-performance.md` | P1 | 路由级 code splitting、图片优化、Web Vitals、预取边界、运行时样式成本和 bundle 风险。 |
| FE-ROUTE-008 | `styling-and-tokens.md` | P2 | 从当前 `design-tokens.md` 扩展到颜色、间距、字号、圆角、阴影、motion 和组件 token。 |

### 3.2 现有路由调整

| 编号 | 当前文件 | 调整方式 | 理由 |
| --- | --- | --- | --- |
| FE-SPLIT-001 | `frontend/index.md` | 保留为唯一前端入口索引 | 当前职责清晰，应继续承担前端路由发现。 |
| FE-SPLIT-002 | `ui-development.md` | 改为“前端开发总检查摘要”或删除 | 与 `frontend/index.md` 重复承载入口索引，存在轻度膨胀。 |
| FE-SPLIT-003 | `javascript-typescript.md` | 收窄为 JS/TS 类型和语言边界 | 当前混入状态、依赖、验证、安全输入，适合迁出。 |
| FE-SPLIT-004 | `navigation-and-state.md` | 收窄为导航和路由状态 | 页面状态和异步状态迁入 `state-and-cache.md`。 |
| FE-SPLIT-005 | `interaction-and-permission.md` | 拆成交互模式与权限渲染，或至少分章节 | 当前混入筛选、时间格式、导航、权限和挂载入口。 |
| FE-SPLIT-006 | `design-tokens.md` | 改名或扩展 | 现正文主要是颜色 token，文件名范围更大。 |

## 4. 功能需求明细

### FR-001 前端路由索引可发现

规则：

- `engineering/index.md` 必须补充新增前端子路由的触发词。
- `frontend/index.md` 必须列出所有实际存在的前端子路由。
- 新增路由只能写入已创建或已确认会创建的文件，避免悬空入口。

验收标准：

- 搜索 `frontend/index.md` 可以找到所有新增文件名。
- 搜索 `engineering/index.md` 可以找到高频触发词：项目结构、状态缓存、测试、可访问性、工具链。
- 不存在索引指向未落盘文件。

### FR-002 项目结构规则独立

规则：

- 规则应覆盖 feature 模块边界、共享层职责、app/features/shared 单向依赖、跨 feature 引用限制和文件命名。
- 不强制某个目录名作为所有项目唯一标准；应写成“如项目采用 feature-based structure”或“默认建议”。
- 应说明项目既有结构优先。

验收标准：

- `project-structure.md` 包含适用范围、生效条件、核心规则和输出要求。
- 可以指导 Agent 判断新增文件应放在页面局部、feature 内、shared component、hook、service、utils 还是 store。

### FR-003 状态和缓存规则独立

规则：

- 区分组件状态、应用状态、服务端缓存、表单状态和 URL 状态。
- 服务端数据缓存不应默认塞进全局 store。
- URL query、分页、筛选、排序和列表缓存之间必须有单一状态拥有者。
- 状态同步必须覆盖初始化、刷新、失效、错误和路由切换清理。

验收标准：

- `state-and-cache.md` 能独立回答“状态放哪、谁拥有、何时同步、何时清理”。
- `javascript-typescript.md` 和 `navigation-and-state.md` 不再重复展开同类状态规则。

### FR-004 前端测试规则独立

规则：

- 测试应优先验证用户可见行为和业务结果，避免依赖组件内部实现细节。
- 新增复杂交互、表单、权限、异步数据、路由状态或关键用户旅程时，应说明对应测试层级。
- API 未就绪时，允许使用 MSW 或等价 mock server，但不得把 mock 数据伪装成真实后端能力。
- E2E 适合核心旅程和回归烟测，不要求所有细节都进入 E2E。

验收标准：

- `testing.md` 包含 unit、integration、E2E、mock server 的适用边界。
- 检查清单新增前端测试项，并能在 PRD 或开发验收中引用。

### FR-005 可访问性规则独立

规则：

- 交互组件必须考虑键盘操作、焦点管理、语义角色、可读标签和错误提示关联。
- Dialog、Menu、Tooltip、Popover、Tabs、Combobox 等复杂组件应优先复用项目既有组件库或成熟 headless 基础，不默认手写底层行为。
- 禁止只靠颜色表达状态；重要状态需要文本、图标、aria 或等价辅助信息。
- 紧凑 UI 不得牺牲可点击性、可读性和焦点可见性。

验收标准：

- `accessibility.md` 包含核心组件和页面状态的 a11y 检查点。
- `compact-ui.md` 和 `interaction-and-permission.md` 引用可访问性规则，而不是零散重复。

### FR-006 工具链和验证规则独立

规则：

- 前端交付前应按项目现有入口运行 typecheck、lint、test、build 或等价验证。
- ESLint 负责问题模式和代码质量，Prettier 负责格式化，不应把二者职责混淆。
- TypeScript 项目应优先使用项目 tsconfig、生成类型和 lint 配置，不为了通过检查扩大 `any` 或类型断言。
- 无法运行验证时，必须说明原因和替代验证。

验收标准：

- `tooling-and-verification.md` 包含工具职责边界和输出要求。
- `javascript-typescript.md` 只保留对验证入口的引用，不重复长规则。

### FR-007 组件系统规则补齐

规则：

- 新共享组件前应先确认已有组件、组合模式、配置扩展或第三方组件包装是否可复用。
- 页面局部组件可以存在，但必须有清晰边界。
- 第三方组件应通过项目组件层适配业务默认值、主题、i18n、a11y 和错误状态。
- 如项目使用 Storybook 或等价组件工坊，新增高复用组件应补组件示例或文档。

验收标准：

- `component-system.md` 能指导 Agent 判断“复用、包装、局部组件、新共享组件”四类选择。
- 与 `layering-and-size.md` 的 props、文件规模、复用价值规则不冲突。

### FR-008 前端性能规则补齐

规则：

- 性能规则应与通用 `performance/` 路由互相引用，不重复后端性能内容。
- 前端性能重点覆盖首屏、路由级 code splitting、资源体积、图片、预取、渲染频率、运行时样式成本和 Web Vitals。
- 不做无证据微优化；性能优化必须说明目标指标、影响路径和验证方式。

验收标准：

- `frontend-performance.md` 可单独用于前端页面性能任务。
- `engineering/index.md` 能把前端性能任务路由到 `frontend/frontend-performance.md` 和通用 `performance/index.md`。

### FR-009 检查清单补齐

规则：

- `checks/checklists.md` 新增以下检查组：
  - `frontend-accessibility-checklist`
  - `frontend-testing-checklist`
  - `frontend-performance-checklist`
  - `frontend-component-checklist`
  - `frontend-structure-checklist`
- 检查项必须使用 `CHK-*` 编号，避免与现有编号冲突。
- 检查项只写可判断标准，不写长流程。

验收标准：

- 每组至少包含 4 个可执行检查项。
- 检查项能回链到对应前端路由。

## 5. 非功能需求

### NFR-001 分层一致性

新增内容必须符合本仓协议原则：

- 入口只负责路由选择。
- 工程路由负责执行规则。
- 检查清单负责审查和验收。
- 不把外部调研证据写进生效规则正文。

### NFR-002 规范词强度

- 安全、权限、可访问性、真值源、验证闭环可使用“必须”。
- 框架、库、目录命名和工具选择默认使用“应”“建议”或“如项目采用...”。
- 没有项目证据的技术栈规则不得写成通用强制规则。

### NFR-003 最小修改

- 优先新增独立路由并同步索引。
- 对现有文件只做职责收窄、引用迁移和描述优化。
- 不做无关重命名或全仓格式化。

### NFR-004 可验证性

本需求完成后至少验证：

- `rg` 检查新增路由是否被索引引用。
- `scripts/check-cross-references.ts` 检查交叉引用。
- `scripts/check-rule-ids.ts` 检查编号。
- `scripts/check-placeholders.ts` 检查占位符。

## 6. 信息架构

目标前端目录建议如下：

```text
skills/maintain-agent-protocols/references/engineering/frontend/
├── index.md
├── api-and-data.md
├── list-query.md
├── form-validation.md
├── i18n-governance.md
├── compact-ui.md
├── layering-and-size.md
├── javascript-typescript.md
├── project-structure.md
├── state-and-cache.md
├── testing.md
├── accessibility.md
├── tooling-and-verification.md
├── component-system.md
├── frontend-performance.md
└── styling-and-tokens.md
```

待处理：

- `[待定项-001]` `design-tokens.md` 是改名为 `styling-and-tokens.md`，还是保留文件名并扩展正文。影响：引用同步成本和历史路径兼容。
- `[待定项-002]` `interaction-and-permission.md` 是否拆成两个文件。影响：文件数量与索引复杂度。
- `[待定项-003]` `ui-development.md` 是删除、保留为摘要，还是迁入 `frontend/index.md`。影响：兼容已有引用。

## 7. 实体与状态

### 7.1 核心实体

| 实体 | 定义 | 关键字段 |
| --- | --- | --- |
| FrontendRoute | 前端工程规则路由文件 | path、title、scope、triggers、relatedRoutes、status |
| Rule | 可执行规则 | id、type、scope、condition、body、verification、sourceRoute |
| ChecklistItem | 审查检查项 | id、group、target、passCriteria、evidence |
| ResearchInsight | 调研启发 | source、insight、adoptionDecision、targetRoute |
| OpenQuestion | 待定项 | id、question、impact、owner、status |

### 7.2 状态

| 状态 | 含义 | 可进入条件 | 退出条件 |
| --- | --- | --- | --- |
| 草案 | PRD 已生成，需求仍可调整 | 本文件创建后 | 用户确认进入实施 |
| 待实施 | 需求范围确认，尚未改规则 | 用户确认待定项或接受默认方案 | 开始修改路由文件 |
| 实施中 | 正在新增或调整规则 | 有明确任务范围 | 文件修改完成 |
| 待验证 | 文件已改，等待脚本和人工检查 | 修改完成 | 验证通过或发现问题 |
| 已完成 | 规则、索引、检查项均已闭环 | 验证通过，问题归类完成 | 后续版本变更 |

## 8. 优先级与里程碑

### Milestone 1: MVP 路由补齐

范围：

- 新增 `project-structure.md`
- 新增 `state-and-cache.md`
- 新增 `testing.md`
- 新增 `accessibility.md`
- 新增 `tooling-and-verification.md`
- 更新 `frontend/index.md`
- 更新 `engineering/index.md`
- 更新 `checks/checklists.md`

完成标准：

- 五个 P0 路由均可通过索引发现。
- 检查清单覆盖 a11y、测试、结构、工具链。
- 不破坏现有 i18n、列表查询和表单规则。

### Milestone 2: 规则拆分和描述优化

范围：

- 收窄 `javascript-typescript.md`
- 收窄 `navigation-and-state.md`
- 处理 `ui-development.md`
- 评估 `interaction-and-permission.md` 是否拆分

完成标准：

- 同类规则只有一个主维护位置。
- 其他文件只保留引用或差异。

### Milestone 3: 组件系统与性能补强

范围：

- 新增 `component-system.md`
- 新增 `frontend-performance.md`
- 处理 `design-tokens.md` 改名或扩展

完成标准：

- 前端组件、性能和样式 token 有独立入口。
- 与通用性能路由和 UI 规则不重复。

## 9. 验收清单

- [x] 所有新增路由文件存在。
- [x] `frontend/index.md` 包含所有新增路由。
- [x] `engineering/index.md` 包含新增路由触发词。
- [x] `checks/checklists.md` 包含新增前端检查组。
- [x] `ui-development.md` 重复入口职责已处理。
- [x] `javascript-typescript.md` 不再承载状态、依赖、验证的长规则。
- [x] `navigation-and-state.md` 不再承载通用页面状态规则。
- [x] 所有新增 `CON-*`、`CHK-*` 编号无冲突。
- [x] 无悬空相对路径引用。
- [x] 无 `<project>`、`<path>` 等模板占位符。
- [x] 验证脚本运行并记录结果。

## 10. 待定项

- `[待定项-001]` 是否改名 `design-tokens.md`。建议：若短期需要兼容现有引用，先保留文件名并扩展标题为“Design Token 与样式语义”；后续版本再迁移。
- `[待定项-002]` 是否拆分 `interaction-and-permission.md`。建议：Milestone 2 再根据文件膨胀程度决定。
- `[待定项-003]` 是否删除 `ui-development.md`。建议：先改为总检查摘要，避免破坏已有引用。
- `[待定项-004]` 是否为每个新增路由引入 `CON-FE-*` 编号。建议：P0 强约束编号，普通建议不编号。
- `[待定项-005]` 是否补充外部来源清单到仓库 README。建议：不补；外部调研证据留在 PRD，不写入生效技能规则。

## 11. 不采纳项

- 不采纳“把 React 或 Next.js 写成默认前端规范”。原因：当前技能面向多框架前端工程路由。
- 不采纳“整段复制 Airbnb JavaScript Style Guide”。原因：应优先继承项目 lint 配置，通用技能只维护工具链与验证原则。
- 不采纳“强制使用 Storybook”。原因：Storybook 是高价值条件工具，但不是所有项目必备。
- 不采纳“强制 Tailwind utility-first”。原因：样式技术栈应项目现状优先。
- 不采纳“把所有新增内容写进用户协议”。原因：这些是工程域执行细节，应位于前端工程路由和检查清单。

## 12. 后续任务

- TODO-001：确认三个待定项：`design-tokens.md`、`interaction-and-permission.md`、`ui-development.md` 的处理方式。
- TODO-002：实施 Milestone 1 的五个 P0 路由与索引同步。
- TODO-003：运行并记录 `check-cross-references.ts`、`check-rule-ids.ts`、`check-placeholders.ts` 验证结果。
- TODO-004：实施 Milestone 2 的职责收窄和重复规则清理。
- TODO-005：实施 Milestone 3 的组件系统、前端性能和样式 token 补强。

## 13. 验收记录

验收日期：2026-06-24

### 已解决

- TODO-001：已采用默认决策。保留 `design-tokens.md` 作为颜色 token 兼容入口，新增 `styling-and-tokens.md`；`interaction-and-permission.md` 先分章节不拆文件；`ui-development.md` 改为前端开发总检查摘要。
- TODO-002：已新增 P0 路由并同步 `frontend/index.md`、`engineering/index.md` 和 `checks/checklists.md`。
- TODO-003：已运行并记录验证脚本，结果见下方。
- TODO-004：已收窄 `javascript-typescript.md`、`navigation-and-state.md` 和 `ui-development.md`，并把旧的维护检查清单重复正文收敛到 `checks/checklists.md`。
- TODO-005：已新增 `component-system.md`、`frontend-performance.md` 和 `styling-and-tokens.md`。

### 验证结果

```text
bun skills/maintain-agent-protocols/scripts/check-cross-references.ts
PASS: 检查了 76 个引用，全部有效

bun skills/maintain-agent-protocols/scripts/check-rule-ids.ts
PASS: 发现规则定义编号 175 个，所有规则编号唯一

bun skills/maintain-agent-protocols/scripts/check-placeholders.ts
PASS: 检查了 97 个文件，未发现占位符泄漏

新增前端检查组数量校验
frontend-accessibility-checklist: 6
frontend-testing-checklist: 5
frontend-performance-checklist: 6
frontend-component-checklist: 6
frontend-structure-checklist: 6

裸 .md 引用检查
PASS

git diff --check
PASS
```

### 明确排除

- 不将 React、Next.js、Tailwind、Storybook 或任一组件库写成通用强制技术栈。
- 不把外部调研来源清单写入生效技能规则正文。
- 不将前端工程细则提升到用户级协议入口。

### 剩余风险

- 根目录 `README.md` 在本次实施前已存在未提交修改，本次验收未处理该无关改动。
