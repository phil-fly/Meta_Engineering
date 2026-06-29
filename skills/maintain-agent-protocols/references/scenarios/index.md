# 场景流程入口

任务执行流程相关请求先读本文件。

## 读取顺序

1. 读取 `playbooks.md` 判断任务流程、`WF-*` 工作流编号和约束门禁节点。
2. 按任务类型读取 `../engineering/index.md` 和对应工程规则。
3. 审查类任务补读 `../checks/checklists.md`。

## 适用任务

- `WF-CODING` 开发任务。
- `WF-ARCHITECTURE` 架构设计。
- `WF-ENTERPRISE-SAAS-DESIGN` 企业级 SaaS、管理后台、控制台、运维平台、安全平台、云管平台、AI 平台、数据平台或设备管理系统的产品与页面设计。
- `WF-SECURITY-REVIEW` 安全审查。
- `WF-PERFORMANCE-REVIEW` 性能审查。
- `WF-TROUBLESHOOTING` 故障排查。
- `WF-RESEARCH` 技术调研。
