# 前端测试

适用前端组件、页面、表单、权限、异步数据、路由状态、关键用户旅程、mock server 和回归验证。

## 测试层级

```text
Unit        → 纯函数、格式化、schema、复杂局部逻辑和稳定共享组件
Integration → 页面片段、表单、数据加载、权限展示和多个组件协作
E2E         → 登录、核心业务流、跨页面旅程、回归烟测和高风险操作
Visual/Story → 高复用组件、视觉状态、主题、响应式和组件文档
```

## 核心约束

- CON-FE-TEST-001 用户行为优先：前端测试应优先验证用户可见行为、业务结果、可访问入口和错误反馈，避免依赖组件内部实现细节、私有 state 或不稳定 DOM 结构。
- CON-FE-TEST-002 风险匹配：新增复杂交互、表单校验、权限展示、异步数据、URL 状态或关键用户旅程时，必须说明采用 unit、integration、E2E、visual/story 或人工验证中的哪些层级。
- CON-FE-TEST-003 Mock 边界：API 未就绪时可用 MSW、mock server 或等价工具 unblock 前端开发，但 mock 结果必须标明数据契约假设，不得伪装成真实后端能力。
- CON-FE-TEST-004 稳定选择器：测试选择器应优先使用用户可感知语义，例如 role、label、text、placeholder 或稳定 test id；不得依赖易变 class、样式层级或生成 ID。
- CON-FE-TEST-005 E2E 范围：E2E 用于核心旅程、跨页面状态和高风险回归，不要求覆盖所有字段分支；大量边界条件应下沉到 integration、unit 或契约测试。
- CON-FE-TEST-006 变更验证：修复缺陷时应优先补能复现失败路径的测试；无法补测试时必须说明原因、替代验证和剩余风险。

## 关联路由

- 工具链和验证入口：读取 `tooling-and-verification.md`。
- 组件系统和 Storybook：读取 `component-system.md`。
- 表单校验和错误展示：读取 `form-validation.md`。
- 多分辨率、浏览器缩放、长文本、极限数据和运行态 UI Review：读取 `ui-stability.md`。
- 权限展示和高影响操作：读取 `interaction-and-permission.md`。

## 输出要求

- 说明本次变更对应的测试层级和未覆盖原因。
- 说明是否使用 mock server、fixture 或真实后端；若使用 mock，说明契约假设。
- 说明验证关注用户行为、业务结果、可访问入口、UI 稳定性还是内部逻辑，并说明执行结果或无法执行原因。
