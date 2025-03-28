# 接口文档https://bigmodel.cn/dev/api/normal-model/glm-4
import asyncio

from langchain_openai import ChatOpenAI
from browser_use import Agent


# 初始化DeepSeek V3模型
llm = ChatOpenAI(
        model='glm-4-plus',
        base_url="https://open.bigmodel.cn/api/paas/v4/chat/completions",
        api_key='xxxxx'  # 替换为实际API密钥
)

async def main():
    agent = Agent(
        task="""
        1. 查找北京到上海的火车票
        """,
        llm=llm,
        save_conversation_path="logs/conversation",  # Save chat logs
        use_vision=False,  # 禁用视觉模式，依赖DOM解析,
        )
    result = await agent.run(max_steps = 3)
    print(result)
    print(result.urls())
    print(result.final_result())

    agent.stop()
asyncio.run(main())
