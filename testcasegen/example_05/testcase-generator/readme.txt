命令行执行：streamlit run app.py

结构：
testcase-generator/
├── .streamlit/
│   ├── secrets.toml       # 密钥管理
│   └── config.toml        # 界面配置
├── config/
│   ├── __init__.py
│   ├── settings.py        # 常量与模型配置
│   └── prompts.py         # 提示语模板
├── core/
│   ├── __init__.py
│   ├── parsers.py         # 文档解析
│   └── agents.py          # 智能体系统
├── app.py                 # 主界面
└── requirements.txt