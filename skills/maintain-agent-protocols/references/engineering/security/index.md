# 安全工程入口

安全设计、安全实现、安全审查和敏感操作任务先读本文件。

## 文件

- `common-security.md`：安全总览和输出要求。
- `trust-boundary.md`：信任边界输入校验。
- `secrets-and-audit.md`：密钥保护、敏感日志和审计。
- `unsafe-selectors.md`：危险选择器和安全中介。
- `sensitive-operations.md`：敏感操作控制。
- `safe-integers.md`：安全敏感整数。
- `dependency-and-config.md`：依赖与安全配置。
- `owasp.md`：OWASP Top 10 检查项。

## 读取顺序

1. 先读 `common-security.md` 判断安全范围和输出要求。
2. 按任务控制点读取对应细分文件。
3. 安全审查或高风险变更补读 `owasp.md`。
4. 涉及权限边界时补读 `../core/auth-and-permission.md`。
5. 涉及审计日志时补读 `../core/error-and-logging.md`。

## 关联

- 鉴权授权：读取 `../core/auth-and-permission.md`。
- 错误与日志：读取 `../core/error-and-logging.md`。
- 安全审查流程：读取 `../../scenarios/playbooks.md`。
- 安全检查清单：读取 `../../checks/checklists.md`。
