# 检查清单

## maintenance-checklist

- CHK-MAINT-001 规则是否有明确适用范围和维护位置？
- CHK-MAINT-002 用户协议是否只保留入口、优先级、任务分类和长期原则？
- CHK-MAINT-003 执行细节是否已下沉到 `routes/`、`playbooks/`、`checks/` 或 `templates/`？
- CHK-MAINT-004 约束是否使用 `CON-*` 编号，并写明适用范围、生效条件、规则正文和验证方式？
- CHK-MAINT-005 工作流是否使用 `WF-*` 编号，并能被任务分类或场景手册引用？
- CHK-MAINT-006 检查项是否使用 `CHK-*` 编号，且同一真值源内唯一？
- CHK-MAINT-007 协议包落盘前是否先给出生成方案预览，并经用户确认？
- CHK-MAINT-008 生成模式是否明确为最小版、项目版或完整版，且默认项目版没有生成无证据语言/框架路由？
- CHK-MAINT-009 `@playbooks`、`@routes`、`@checks` 等抽象入口是否已声明真实路径映射或生成兼容入口？
- CHK-MAINT-010 用户协议是否只列本次实际生成、既有存在或已兼容的场景手册、工程路由和检查入口？
- CHK-MAINT-011 场景手册、工程路由、组合入口和检查入口是否已写成展开后的真实路径，而不是要求执行模型自行解析 `@playbooks`、`@routes` 或 `@checks`？
- CHK-MAINT-012 需要用户确认时是否优先使用当前 Agent App 支持的原生确认/问询机制；不可用时是否退化为普通文本问询？
- CHK-MAINT-013 项目事实、技术栈、命令和目录职责是否都有来源；无来源内容是否标为待确认？
- CHK-MAINT-014 项目级 `必须`、`禁止`、`默认` 或 `仅当` 是否都有目标仓证据支撑？
- CHK-MAINT-015 项目版路由索引是否按 `项目证据支持`、`条件适用`、`通用治理` 标注，并裁剪到文件级粒度？
- CHK-MAINT-016 OpenSpec、风险控制等高频规则是否用锚点式引用压缩，避免结构化约束和详情章节重复展开？
- CHK-MAINT-017 用户协议引用的入口文件是否实际存在？
- CHK-MAINT-018 是否已声明唯一生效入口和各资产真值源，避免根级目录与 `ai-agent-protocols/` 全文双写？
- CHK-MAINT-019 协议正文、协议包 README 和入口说明是否排除了“生成依据”、读取文件清单和事实来源清单？
- CHK-MAINT-020 生效协议、协议包 README 和入口说明是否清除了 `<project>`、`<install-command>`、`<path>` 等模板占位符？
- CHK-MAINT-021 是否单独提供生成报告，并把扫描过程、读取文件清单、置信度和使用者下一步放在报告而不是协议正文？
- CHK-MAINT-022 生成报告是否说明工作区状态，包括未跟踪文件和无关修改？
- CHK-MAINT-023 嵌套目录中的路径引用是否能按当前文件位置或声明的仓库根口径解析？
- CHK-MAINT-024 新增规则是否与更高优先级指令冲突？
- CHK-MAINT-025 若本轮摄入工程实现规则，是否已先评估合理性、适用范围、反例和规范词强度，并写入对应工程路由或检查项？
- CHK-MAINT-026 如新增、移动或删除 reference，`SKILL.md`、局部 index 和总入口是否已同步？
- CHK-MAINT-027 发现的问题是否归类为已解决、延后处理、明确排除或转入后续任务？
- CHK-MAINT-028 创建、升级或审查协议包时，是否已检查任务入口、场景手册、工程路由、项目级约束和检查项之间的触发链路？
- CHK-MAINT-029 条件适用路由是否写明触发条件，且高风险或高频路由能从相关 playbook 短路径触达？
- CHK-MAINT-030 项目级高风险约束是否有生效条件、验证方式和相关工作流短引用，避免只孤立存在于项目协议？
- CHK-MAINT-031 playbook 闭环步骤是否映射到相关检查清单或 `CHK-*` 编号族，且未复制完整检查清单正文？

## security-checklist

- CHK-SEC-001 是否校验信任边界输入？
- CHK-SEC-002 是否保护密钥和敏感日志？
- CHK-SEC-003 是否有认证、授权和资源归属？
- CHK-SEC-004 敏感操作是否具备审计和防滥用？
- CHK-SEC-005 不受信选择器是否经过安全中介？
- CHK-SEC-006 安全整数是否先校验再转换？
- CHK-SEC-007 是否覆盖 OWASP Top 10 相关风险？
- CHK-SEC-008 涉及运行、功能或外部集成配置时，是否已完成配置可发现性评审要求自检？

## frontend-i18n-checklist

- CHK-FE-I18N-001 本次变更是否新增、修改或展示用户可见文案？若否则记录为不适用，并跳过仅由新增文案触发的后续资源同步检查。
- CHK-FE-I18N-002 是否使用项目统一翻译入口、文案资源或等价国际化抽象？
- CHK-FE-I18N-003 是否同步新增或更新语言资源？
- CHK-FE-I18N-004 是否存在硬编码中文？
- CHK-FE-I18N-005 是否存在硬编码英文用户文案？
- CHK-FE-I18N-006 Key 是否符合业务域语义命名？
- CHK-FE-I18N-007 是否同步更新 `zh-CN`？
- CHK-FE-I18N-008 是否同步更新 `en-US`？
- CHK-FE-I18N-009 错误码、异常信息、校验提示和业务提示是否可本地化？
- CHK-FE-I18N-010 是否禁止硬编码用户可见文案？
- CHK-FE-I18N-011 是否禁止中文 Key、整句英文 Key、位置型 Key 和顺序型 Key？
- CHK-FE-I18N-012 是否禁止缺失翻译资源？
- CHK-FE-I18N-013 Key 是否语义化并保持稳定？
- CHK-FE-I18N-014 新页面、新菜单或新业务域是否同步语言资源？
- CHK-FE-I18N-015 Error 信息、业务异常、表单错误和 Notification 是否已国际化？

## frontend-accessibility-checklist

- CHK-FE-A11Y-001 是否使用正确语义元素或等价 ARIA，并避免用无语义容器模拟核心交互？
- CHK-FE-A11Y-002 核心操作、导航、弹窗、菜单、下拉和批量操作是否可键盘访问且焦点可见？
- CHK-FE-A11Y-003 Dialog、Drawer、Popover、Menu、Combobox 等浮层是否处理打开焦点、焦点约束、关闭返回和 Esc 语义？
- CHK-FE-A11Y-004 表单 label、辅助说明、必填状态和错误提示是否与字段建立可感知关联？
- CHK-FE-A11Y-005 成功、警告、危险、选中、禁用或错误状态是否不只依赖颜色表达？
- CHK-FE-A11Y-006 紧凑布局是否保持可读性、可点击目标、触控间距和焦点可见性？

## frontend-testing-checklist

- CHK-FE-TEST-001 测试是否优先验证用户可见行为、业务结果和可访问入口，而不是组件内部实现细节？
- CHK-FE-TEST-002 本次变更是否说明 unit、integration、E2E、visual/story 或人工验证的适用层级？
- CHK-FE-TEST-003 使用 mock server、fixture 或 MSW 时，是否标明数据契约假设且未伪装成真实后端能力？
- CHK-FE-TEST-004 测试选择器是否优先使用 role、label、text、placeholder 或稳定 test id？
- CHK-FE-TEST-005 缺陷修复是否补充失败路径测试，或说明无法补测试的原因和替代验证？

## frontend-performance-checklist

- CHK-FE-PERF-001 前端性能优化是否说明目标指标、关键路径、影响范围和验证方式？
- CHK-FE-PERF-002 是否评估路由级 code splitting、chunk 数量和首屏关键路径影响？
- CHK-FE-PERF-003 新增组件库、图表库、编辑器、地图、polyfill 或运行时样式方案时是否说明体积影响？
- CHK-FE-PERF-004 图片、图标、字体和媒体资源是否有尺寸、格式、懒加载、预加载或响应式策略？
- CHK-FE-PERF-005 高频更新、长列表、复杂图表和全局状态变化是否控制渲染范围或使用虚拟化、节流、防抖、选择器策略？
- CHK-FE-PERF-006 数据或代码预取是否服务明确下一步旅程，且没有全局无界预取或缓存？

## frontend-ui-stability-checklist

- CHK-FE-STABILITY-001 页面完成是否基于实际运行 UI 验收，而不是只依赖静态截图或单一开发设备效果？
- CHK-FE-STABILITY-002 桌面后台页面是否说明最小支持宽度、分辨率和浏览器缩放验证结果；响应式产品是否继承项目断点策略？
- CHK-FE-STABILITY-003 是否验证长中文、长英文、URL、JSON、IP、IPv6、域名等内容不会遮挡、重叠或不可查看？
- CHK-FE-STABILITY-004 表格列宽、长文本列、横向滚动和完整内容查看方式是否明确，且没有无限压缩到不可读？
- CHK-FE-STABILITY-005 卡片、网格、表单 label、输入框和操作按钮是否在缩放和长文本下保持对齐、可读和可操作？
- CHK-FE-STABILITY-006 Dialog、Drawer、Popover 等浮层是否有视口约束、内部滚动和超长内容可达性？
- CHK-FE-STABILITY-007 是否覆盖空数据、少量数据、大量数据、长文本和异常数据；未覆盖项是否说明原因和风险？
- CHK-FE-STABILITY-008 是否避免用固定主体宽高、absolute 拼页面、删除字段、缩小字体或 overflow hidden 掩盖布局问题？

## frontend-enterprise-saas-design-checklist

- CHK-FE-SAAS-001 是否确认任务适用于企业级 SaaS、管理后台、控制台、运维平台、安全平台、云管平台、AI 平台、数据平台或设备管理系统，而不是官网、活动页、品牌宣传页或营销落地页？
- CHK-FE-SAAS-002 是否先完成产品建模，并说明系统类型、核心实体、用户角色、核心流程、辅助流程、关键状态和用户真正管理的对象？
- CHK-FE-SAAS-003 信息架构是否围绕用户目标、业务流程和业务领域组织，而不是数据库表、后端模块、API 分组或配置文件结构？
- CHK-FE-SAAS-004 每个关键页面是否定义页面目标、主要操作、次要操作、管理实体、关键决策、前置条件和后置结果？
- CHK-FE-SAAS-005 页面布局是否由页面职责和业务流程推导，并明确 Dashboard、管理页面、编辑页面、巡检中心或项目特定结构的适用理由？
- CHK-FE-SAAS-006 组件规划是否说明数据规模、关系复杂度、状态语义和批量操作策略，并继承项目组件系统？
- CHK-FE-SAAS-007 是否在线框图之后再输出视觉设计 Prompt、高保真设计稿或前端实现说明？
- CHK-FE-SAAS-008 视觉设计是否保持企业级、高信息密度、可落地、浅色主题、弱阴影和一致 Design Token，并排除营销式、游戏化、科幻风或概念稿模式？
- CHK-FE-SAAS-009 是否说明 500+ 实体、1000+ 资源、500+ 规则和 10000+ 事件等规模下的表格、列表、筛选、分页、虚拟化或横向滚动策略？
- CHK-FE-SAAS-010 是否说明未覆盖的设计阶段、验收项、数据规模、可访问性、运行态 UI 稳定性和剩余风险？

## frontend-component-checklist

- CHK-FE-COMPONENT-001 新共享组件前是否检查已有组件、组合模式、配置扩展、样式 token 和第三方包装层？
- CHK-FE-COMPONENT-002 页面局部组件和共享组件的边界是否清晰，且共享组件具备稳定复用场景？
- CHK-FE-COMPONENT-003 第三方 UI 组件是否通过项目组件层适配主题、i18n、a11y、错误状态和业务默认值？
- CHK-FE-COMPONENT-004 props 过多、状态分支过多或 slot 复杂时，是否采用组合、配置对象、上下文边界或子组件拆分？
- CHK-FE-COMPONENT-005 高复用组件是否覆盖默认、hover、focus、disabled、loading、empty、error、success、长文本和移动端状态？
- CHK-FE-COMPONENT-006 如项目使用 Storybook 或等价组件工坊，是否同步组件示例、状态或文档？

## frontend-structure-checklist

- CHK-FE-STRUCTURE-001 新增或移动文件前是否识别项目既有目录、别名、组件层、路由层和测试布局？
- CHK-FE-STRUCTURE-002 如项目采用 feature-based structure，feature 内代码是否保持业务域内聚并避免默认跨 feature 互引？
- CHK-FE-STRUCTURE-003 共享层、feature 层和 app 层是否保持单向依赖，避免共享层反向依赖业务或应用层？
- CHK-FE-STRUCTURE-004 新增共享 hook、utils、service、types 或组件是否具备明确复用场景和维护边界？
- CHK-FE-STRUCTURE-005 文件名、组件名、Hook 名、store 名和实际职责是否一致？
- CHK-FE-STRUCTURE-006 移动公共能力时是否同步导入、路由注册、测试、文档和类型引用？

## performance-checklist

- CHK-PERF-001 是否存在 N+1 查询？
- CHK-PERF-002 是否存在未释放资源或长期持有对象？
- CHK-PERF-003 是否存在高复杂度算法？
- CHK-PERF-004 是否在循环中重复创建可复用对象？
- CHK-PERF-005 是否存在关键路径同步阻塞？
- CHK-PERF-006 是否说明性能验证方式？
