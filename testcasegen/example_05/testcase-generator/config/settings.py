from autogen_ext.models.openai import OpenAIChatCompletionClient
import os
import streamlit as st

# 模型客户端配置 [1,2](@ref)
DEEPSEEK_CLIENT = OpenAIChatCompletionClient(
    model= "deepseek-chat",
    base_url= "https://api.deepseek.com",
    api_key=os.getenv("DEEPSEEK_API_KEY") or st.secrets["api_keys"]["DEEPSEEK_API_KEY"],
    model_info={
        "family": "deepseek",  # 必须包含的字段
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "max_tokens": 4096
    }
)

llm_config = {
    "config_list": [{
        "model": "deepseek-chat",  # 必填字段
        # "api_type": "open_ai",     # 本地模型需指定为 open_ai
        "api_key": os.getenv("DEEPSEEK_API_KEY") or st.secrets["api_keys"]["DEEPSEEK_API_KEY"],         # 本地模型可为空
        "base_url": "https://api.deepseek.com"
    }],
    "temperature": 0.3,
    "max_tokens": 2000
}


# 运行环境配置
CACHE_CONFIG = {
    "ttl": 3600,
    "show_spinner": False
}