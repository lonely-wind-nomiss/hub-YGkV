import os

# https://bailian.console.aliyun.com/?tab=model#/api-key
os.environ["OPENAI_API_KEY"] = "sk-67042ea1c6c342c0974f00b6ee886b33"
os.environ["OPENAI_BASE_URL"] = "https://api.deepseek.com"

import asyncio
from pydantic import BaseModel
from typing import Optional
from agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner
from agents.exceptions import InputGuardrailTripwireTriggered
# from agents.extensions.visualization import draw_graph

# 大模型调用调用协议
# openai： Chat Completions / Responses
# a/ ：

from agents import set_default_openai_api, set_tracing_disabled
set_default_openai_api("chat_completions") # 强制 SDK 使用 Chat Completions API，而非默认的 Responses API。
set_tracing_disabled(True) # 彻底关闭 SDK 的链路追踪（Tracing） 功能

class HomeworkOutput(BaseModel):
    """用于判断用户请求是否属于功课或学习类问题的结构"""
    is_Chinese: bool


# 守卫检查代理 - 》 本质也是通过大模型调用完成的
guardrail_agent = Agent(
    name="Guardrail Check Agent",
    model="deepseek-v4-flash",
    instructions=(
        "判断用户的是否为中文。"
        "请严格以 JSON 格式返回，且只返回 JSON，不要有 markdown 代码块包裹。"
        "格式示例：{\"is_Chinese\": true} 或 {\"is_Chinese\": false}"
    ),
)

async def homework_guardrail(ctx, agent, input_data):
    """
    运行检查代理来判断输入是否为功课。
    如果不是功课 ('is_homework' 为 False)，则触发阻断 (tripwire)。
    """
    print(f"\n[Guardrail Check] 正在检查输入: '{input_data}'...")
    
    # 运行检查代理
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    
    # 解析输出
    raw = result.final_output.strip()
    if raw.startswith("```"):  # 防御模型加 ```json 代码块
        raw = raw.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    final_output = HomeworkOutput.model_validate_json(raw)
    
    tripwire_triggered = not final_output.is_Chinese
        
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=tripwire_triggered,
    )


translate_agent = Agent(
    name="Triage Agent",
    model="deepseek-v4-flash",
    instructions="""您的任务是根据用户输入的文本进行判断翻译，如果是中文，就翻译成英文，否则就翻译成中文。
    请严格以 JSON 格式返回，且只返回 JSON，不要有 markdown 代码块包裹。
    示例1：
    用户输入：你好。
    输出：{"query":"你好","language":"中文","result":"hello"}
    示例1：
    用户输入：Hello。
    输出：{"query":"Hello","language":"英文","result":"你好"}
    """,
)


async def main():
    print("--- 启动文本翻译代理系统示例 ---")
    
    print("\n" + "="*50)
    print("="*50)
    try:
        query = "请问人工智能发展前景怎么样？"
        print(f"**用户提问:** {query}")
        result = await Runner.run(translate_agent, query) # 异步运行  guardrail agent -》 triage agent -》 math agent
        print("\n**✅ 流程通过，最终输出:**")
        print(result.final_output)
    except InputGuardrailTripwireTriggered as e:
        print("\n**❌ 守卫阻断触发:**", e)
        
    
    print("\n" + "="*50)
    print("="*50)
    try:
        query = "I will go to Beijing for working。"
        print(f"**用户提问:** {query}")
        result = await Runner.run(translate_agent, query)
        print("\n**✅ 流程通过，最终输出:**")
        print(result.final_output)
    except InputGuardrailTripwireTriggered as e:
        print("\n**❌ 守卫阻断触发:**", e)
        
    
    print("\n" + "="*50)
    print("="*50)
    try:
        query = "베이징은 중국의 수도입니다."
        print(f"**用户提问:** {query}")
        result = await Runner.run(translate_agent, query)
        print("\n**✅ 流程通过，最终输出:**")
        print(result.final_output) # 这行应该不会被执行
    except InputGuardrailTripwireTriggered as e:
        print("\n**❌ 守卫阻断触发:** 输入被阻断，因为它不是功课。")
        print(e)

if __name__ == "__main__":
    asyncio.run(main())


