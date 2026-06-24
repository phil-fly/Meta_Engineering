# JavaScript / TypeScript

适用前端 JavaScript、TypeScript、JSX、TSX、浏览器运行时代码、Electron 渲染进程代码和前端构建脚本。框架可为 React、Vue、Angular、Svelte 或项目自定义框架。

## 核心规则

- 默认继承 `../core/common-quality.md`、`api-and-data.md`、`interaction-and-permission.md`、`state-and-cache.md`、`tooling-and-verification.md` 和相关前端细分路由。
- TypeScript 项目应优先表达真实类型边界，避免用 `any`、类型断言或宽泛对象绕过契约；确需使用时，应说明来源边界和收敛计划。
- 共享类型应从接口契约、schema、生成类型或稳定领域模型派生，避免前后端平行手写漂移。
- 异步流程必须覆盖 loading、error、success、cleanup 和过期响应；组件卸载、请求取消或路由切换时不得留下悬挂更新。
- DOM、URL、HTML、样式选择器、排序字段和本地存储输入属于不受信输入时，必须经过安全映射、白名单或转义处理。
- 状态拥有者、服务端缓存、URL 状态和本地持久化规则以 `state-and-cache.md` 为准；本文件只要求类型边界不得掩盖状态契约。
- 前端包依赖、构建插件、运行时 polyfill 和验证入口以 `tooling-and-verification.md` 为准；本文件只要求依赖暴露的类型契约清晰。
- 浏览器端和 Electron 渲染进程不得保存生产密钥、长期令牌或服务端权限判断；隐藏 UI 不是最终权限边界。
- 交付前应按 `tooling-and-verification.md` 运行与变更范围匹配的类型检查、lint、测试或构建入口；若不可用，应说明原因和替代验证。

## 输出要求

- 说明本次任务涉及类型边界、异步生命周期、安全输入或浏览器端权限中的哪些子域。
- 说明是否存在 `any`、类型断言、平行手写类型、悬挂异步或浏览器端权限误用；状态、依赖和验证结论分别引用 `state-and-cache.md` 与 `tooling-and-verification.md`。
