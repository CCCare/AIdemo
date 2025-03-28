import streamlit as st
from autogen import GroupChatManager, GroupChat

from config.settings import llm_config
from config.prompts import PROMPT_TEMPLATE, FORMAT_INSTRUCTION
from core.parsers import parse_pdf
from core.agents import initialize_agents
from core.testcases_tasks import display_testcase_table
import time


def main():
    # 页面基础配置 [4,6](@ref)
    st.set_page_config(
        page_title="AI测试用例生成系统",
        layout="wide",
        page_icon="🧪"
    )

    # 在app.py顶部添加CSS样式
    st.markdown("""
    <style>
        /* 表格行高亮 */
        .ag-row-hover {
            background-color: #f5f5f5 !important;
            cursor: pointer;
        }

        /* 详情面板样式 */
        div[data-testid="stExpander"] details {
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 1rem;
        }

        /* 状态标签颜色 */
        [data-testid="stMetricValue"] {
            color: #1f77b4;  /* 默认蓝色 */
        }
        [data-testid="stMetricValue"].status-failed {
            color: #ff4b4b;  /* 失败红色 */
        }
    </style>
    """, unsafe_allow_html=True)

    # 侧边栏参数配置
    with st.sidebar:
        case_num = st.slider("生成用例数量", 1, 100, 1)
        test_level = st.selectbox("测试级别", ["单元","功能", "集成", "系统"])

    # 双模式输入
    input_tab, doc_tab = st.tabs(["📝 文本输入", "📁 文档上传"])
    with input_tab:
        input_text = st.text_area("输入需求描述", height=200)
    with doc_tab:
        if uploaded_file := st.file_uploader("上传PRD文档", type=["pdf"]):
            if parsed := parse_pdf(uploaded_file):
                input_text = parsed["text"]

    # 生成逻辑
    if input_text and st.button("🚀 生成用例"):
        with st.spinner("智能体协作中..."):
            start_time = time.time()

            # 测试类型映射
            test_type_map = {
                "单元": ["函数验证", "边界值", "异常处理"],
                "集成": ["功能验证", "接口兼容性", "数据一致性"],
                "系统": ["业务流程", "性能基线", "监控告警"]
            }

            # 动态更新模板（网页6的提示词工程）
            dynamic_template = PROMPT_TEMPLATE.format(
                requirement=input_text,
                test_level=test_level,
                case_num=case_num,
                test_type_condition="\n   ".join(test_type_map[test_level]),
                format_instruction=FORMAT_INSTRUCTION
            )

            # 获取智能体列表和转换规则
            agents, transition_rules = initialize_agents(llm_config,test_level)
            # 查看代理角色配置
            for agent in agents:
                print(f"Agent: {agent.name}\nSystem Message: {agent.system_message}\n")

            group_chat = GroupChat(
                agents=agents,
                messages=[],
                allowed_or_disallowed_speaker_transitions=transition_rules,
                speaker_transitions_type="allowed",  # 明确指定类型
                max_round=30,  # 限制最大对话轮次，默认值为12，建议扩展至20-30
            )

            manager = GroupChatManager(groupchat=group_chat,
                                       llm_config=llm_config,  # ✅ 必须传递有效 LLM 配置
                                       system_message=f"生成至少{case_num}个测试用例后自动终止，其中必须包含{test_level}测试类型",
                                       )

            response = manager.run(dynamic_template)

            print(response)

            # # 结果后处理 [2](@ref)
            # processed_cases = filter_testcases(
            #     parse_response(response),  # 解析原始响应
            #     case_num=case_num,
            #     test_level=test_level
            # )
            #
            # # 存储到会话状态
            # st.session_state.test_cases = processed_cases
            #
            # # 结果展示
            st.subheader("生成结果")
            st.markdown(response)
            st.success(f"生成完成！耗时 {time.time() - start_time:.2f}s")

    # 展示结果
    if 'test_cases' in st.session_state:
        display_testcase_table(st.session_state.test_cases)

    # # 添加导出按钮
    # if st.button("📥 导出测试用例"):
    #     export_data = convert_to_excel(st.session_state.test_cases)
    #     st.download_button(
    #         label="下载Excel文件",
    #         data=export_data,
    #         file_name=f"测试用例_{test_level}_{case_num}条.xlsx",
    #         mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    #     )
if __name__ == "__main__":
    main()