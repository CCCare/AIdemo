import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

class LLM(ChatOpenAI):
    def __init__(self,*args,**kwargs):
        belong = os.environ.get("MODEL_BELONG")
        if belong == "DEEPSEEK":
            base_url = "https://api.deepseek.com"
            api_key = os.environ.get("DEEPSEEK_API_KEY")
            model = 'deepseek-chat'
        elif belong == "ZHIPU":
            base_url = "https://open.bigmodel.cn/api/paas/v4/"
            api_key = os.environ.get("ZHIPU_API_KEY")
            model = 'glm-4'
        else:
            raise NotImplementedError(f"{belong} is not supported")
        kwargs["api_key"] = api_key
        kwargs["base_url"] = base_url
        kwargs["model"] = model
        super().__init__(*args, **kwargs)

if __name__ == "__main__":
    llm = LLM(belong="DEEPSEEK")
    print(llm)
