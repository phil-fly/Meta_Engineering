# 检查场景入口

审查、验收和维护检查相关请求先读本文件。

## 读取顺序

1. 读取 `checklists.md` 获取维护、安全、前端国际化、前端可访问性、前端测试、前端性能、前端 UI 稳定性、前端组件、前端结构和性能检查项；检查项使用 `CHK-*` 编号。
2. 需要流程时读取 `../scenarios/playbooks.md`。
3. 需要工程规则正文时读取 `../engineering/index.md` 和对应路由。
4. 涉及运行配置、功能配置、外部集成配置或历史配置实现检查时，读取 `../engineering/security/dependency-and-config.md`。

## 适用任务

- `CHK-SEC-*` 安全检查。
- `CHK-FE-I18N-*` 前端国际化与文案治理检查。
- `CHK-FE-A11Y-*` 前端可访问性检查。
- `CHK-FE-TEST-*` 前端测试检查。
- `CHK-FE-PERF-*` 前端性能检查。
- `CHK-FE-STABILITY-*` 前端 UI 稳定性检查。
- `CHK-FE-COMPONENT-*` 前端组件系统检查。
- `CHK-FE-STRUCTURE-*` 前端项目结构检查。
- 配置可发现性检查适用于新开发和历史实现审查，具体检查项以 `checklists.md` 为准。
- `CHK-PERF-*` 性能检查。
- `CHK-MAINT-*` 规则维护检查。
- `CHK-MAINT-*` 协议分层检查。
- `CHK-MAINT-*` 结论范围检查。
