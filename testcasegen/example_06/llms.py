from autogen_ext.models.openai import OpenAIChatCompletionClient
import os
import streamlit as st

model_client = OpenAIChatCompletionClient(
    model="deepseek-chat",
    base_url="https://api.deepseek.com",
    api_key=os.getenv("DEEPSEEK_API_KEY") or st.secrets["api_keys"]["DEEPSEEK_API_KEY"],
    model_info={
        "family": "deepseek",  # 必须包含的字段
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "max_tokens": 4096
    }
)