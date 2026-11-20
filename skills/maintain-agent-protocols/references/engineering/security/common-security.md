# 通用安全总览

适用安全设计、安全实现、安全审查和敏感操作。

本文件只保留安全域总览。需要具体规则时，按 `index.md` 读取同目录下的细分文件。

## 细分入口

- `trust-boundary.md`：信任边界输入校验。
- `secrets-and-audit.md`：密钥保护、敏感日志和审计。
- `unsafe-selectors.md`：危险选择器和安全中介。
- `sensitive-operations.md`：删除、导出、上传、权限变更等敏感操作。
- `safe-integers.md`：安全敏感整数转换前校验。
- `dependency-and-config.md`：依赖漏洞、失败关闭、安全配置和配置可发现性。
- `owasp.md`：OWASP Top 10 检查项。

验证与输出：

- 先列明范围、边界和关键控制点，再给结论。
- 对重复安全发现说明沉淀去向：项目规则、通用规则、工具规则或后续任务。
