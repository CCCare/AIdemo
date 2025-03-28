import asyncio
import os
import logging
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.controller.service import Controller
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from browser_use import Agent
from browser_use import logging_config

# Validate required environment variables
load_dotenv()
# full screen mode
# controller = Controller()

logging.basicConfig(level=logging.DEBUG)
logging_config.setup_logging()

# # 确保日志目录存在
# log_dir = "logs/conversation"
# if not os.path.exists(log_dir):
#     os.makedirs(log_dir)


# 初始化智谱GLM-4模型
llm = ChatOpenAI(
    temperature=0.95,
    model='glm-4',
    # base_url="https://open.bigmodel.cn/api/paas/v4/chat/completions",
    # api_key='e8bb5aaa0caa469f959cb9f073cb12dc.BA5uHVCQUEJtjUS5'  # 替换为实际API密钥
    openai_api_key="e8bb5aaa0caa469f959cb9f073cb12dc.BA5uHVCQUEJtjUS5",
    # openai_api_base="https://open.bigmodel.cn/api/paas/v4/chat/completions"
    openai_api_base="https://open.bigmodel.cn/api/paas/v4/"
)

config = BrowserConfig(
    headless=False,  # 非headless模式
    disable_security=True,  # 关闭安全模式
    extra_chromium_args=[
        "--disable-gpu",
        "--disable-dev-shm-usage",
        "--disable-blink-features=AutomationControlled",
    ],  # 关闭 GPU和devshm
    chrome_instance_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",  # 本地Chrome路径
    # proxy={"server": "proxy.example.com:8080", "username": "username", "password": "password"},  # 代理设置
)
browser = Browser(config=config)



async def main():
    agent = Agent(
        # message_context="",# 提示词
        task="""
        1. 打开必应首页( https://cn.bing.com/)
        2. 等待页面加载完成
        3. 在搜索框输入'目前最流行的编程语言'
        4. 点击搜索按钮，进入搜索结果页面
        """,
        llm=llm,
        save_conversation_path='logs/conversation',  # Save chat logs
        use_vision=True,  # 禁用视觉模式，依赖DOM解析,
        browser=browser,
        # controller=controller
    )
    try:
        result = await agent.run(max_steps=10)
        print(result)
        print(result.urls())
        print(result.final_result())
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        agent.stop()


if __name__ == "__main__":
    asyncio.run(main())