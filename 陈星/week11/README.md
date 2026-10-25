# 陈星 week11 作业

## 作业1：SQL Agent
路径：`task1/00-sql-agent`

基于 `openai-agents` 的只读 SQL Agent：库表解析 → 选表 → 生成 SQL → 校验 → 改写/修复 → 执行 → 结果摘要。

- 运行：`PYTHONPATH=src python3 -m sql_agent "总共有多少张专辑？"`（需 `OPENAI_API_KEY`）
- 测试：`pytest -q`（21 passed，无需 API Key）
- 设计说明：`docs/agent-design.md`

## 作业2：企业级 Data Agent 平台设计
路径：`task2`

- 企业级DataAgent平台功能设计说明.docx
- 企业级DataAgent平台技术设计说明.docx
- 企业级DataAgent平台项目设计说明.docx
