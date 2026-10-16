# 陈星 week10 作业

作业一：多 Agent 语种识别与互译（`task1.py`），输出固定 JSON：`query_input` / `language` / `result`。
作业二：FastMCP 服务端新增 3 个工具（`task2_server.py`：calculator / tokenize / get_time）+ Agents SDK 客户端调用（`task2_client.py`）。

## 环境

```bash
pip install openai-agents fastmcp jieba pydantic
export OPENAI_API_KEY=你的密钥
export OPENAI_BASE_URL=https://api.deepseek.com   # 可选
export OPENAI_MODEL=deepseek-chat                 # 可选
```

## 运行

```bash
# 作业一
python task1.py "今天天气不错"
python task1.py "Hello, nice to meet you"

# 作业二（两个终端）
python task2_server.py
python task2_client.py
```

运行截图请自行补到本目录后提交。
