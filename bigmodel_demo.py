# 接口文档https://bigmodel.cn/dev/api/normal-model/glm-4
import asyncio

from langchain_openai import ChatOpenAI
from browser_use import Agent

# from zhipuai import ZhipuAI
# client = ZhipuAI(api_key="e8bb5aaa0caa469f959cb9f073cb12dc.BA5uHVCQUEJtjUS5")  # 请填写您自己的APIKey
# response = client.chat.completions.create(
#     model="glm-4-plus",  # 请填写您要调用的模型名称
#     messages=[
#         {"role": "user", "content": "作为一名营销专家，请为我的产品创作一个吸引人的口号"},
#         {"role": "assistant", "content": "当然，要创作一个吸引人的口号，请告诉我一些关于您产品的信息"},
#         {"role": "user", "content": "智谱AI开放平台"},
#         {"role": "assistant", "content": "点燃未来，智谱AI绘制无限，让创新触手可及！"},
#         {"role": "user", "content": "创作一个更精准且吸引人的口号"}
#     ],
# )
# print(response.choices[0].message)


# 初始化DeepSeek V3模型
llm = ChatOpenAI(
        model='glm-4-plus',
        base_url="https://open.bigmodel.cn/api/paas/v4/chat/completions",
        api_key='e8bb5aaa0caa469f959cb9f073cb12dc.BA5uHVCQUEJtjUS5'  # 替换为实际API密钥
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