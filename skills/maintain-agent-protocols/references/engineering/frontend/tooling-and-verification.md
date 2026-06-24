# 前端工具链与验证

适用 ESLint、Prettier、TypeScript、typecheck、lint、test、build、pre-commit、CI、路径别名、依赖和交付验证。

## 工具职责

```text
ESLint / framework lint → 问题模式、质量规则、导入边界、安全和框架语义
Prettier / formatter    → 格式化一致性，不承担业务质量判断
TypeScript / typecheck  → 类型边界、重构安全、契约漂移和编译期反馈
Test runner             → 单元、集成、组件和 E2E 行为验证
Build                   → 打包、类型输出、资源、路径别名和生产模式验证
CI / hook               → 提交或合并前的自动质量门
```

## 核心约束

- CON-FE-TOOL-001 项目配置优先：前端验证必须优先使用目标项目已有 package manager、脚本、tsconfig、lint、format、test、build 和 CI 入口；不得凭通用模板替换项目真值源。
- CON-FE-TOOL-002 职责分离：ESLint 负责问题模式和代码质量，Prettier 负责格式化；二者冲突时应调整配置或执行顺序，不用手工风格争论替代工具链。
- CON-FE-TOOL-003 类型收敛：TypeScript 项目应优先通过真实类型、schema、生成类型或契约修正解决错误；不得为了通过检查扩大 `any`、类型断言或宽泛对象。
- CON-FE-TOOL-004 导入边界验证：如项目使用路径别名、模块边界、feature 限制或单向依赖，应通过 lint、tsconfig、构建或等价检查验证导入是否可解析且无反向依赖。
- CON-FE-TOOL-005 依赖准入：新增前端依赖、构建插件、polyfill 或组件库时，应说明复用价值、体积影响、安全风险、维护状态和替代方案；低价值一次性依赖不应引入。
- CON-FE-TOOL-006 交付验证：前端交付前应运行与变更范围匹配的 typecheck、lint、test、build、storybook、E2E 或等价验证；无法运行时必须说明原因、替代验证和剩余风险。

## 关联路由

- JS/TS 类型边界：读取 `javascript-typescript.md`。
- 项目结构和导入方向：读取 `project-structure.md`。
- 前端测试：读取 `testing.md`。
- 运行态 UI 稳定性、多分辨率、浏览器缩放和极限数据验收：读取 `ui-stability.md`。
- 前端性能和 bundle 风险：读取 `frontend-performance.md`。
- 依赖安全：读取 `../security/dependency-and-config.md`。

## 输出要求

- 说明项目已有的验证入口和本次实际运行或无法运行的命令。
- 说明是否涉及 lint、format、typecheck、test、build、依赖或路径别名。
- 涉及页面或复杂组件时，说明是否运行或人工完成 UI 稳定性验证；无法验证时说明替代证据和剩余风险。
- 说明新增依赖、插件或 polyfill 的价值、体积、安全和维护风险。
