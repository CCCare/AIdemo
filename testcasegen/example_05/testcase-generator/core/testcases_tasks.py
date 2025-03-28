import json

import pandas as pd

import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder

def parse_response(raw_response):
    try:
        cases = json.loads(raw_response)
        return [validate_case(c) for c in cases]
    except json.JSONDecodeError:
        print("Invalid JSON format")
        # logger.error("Invalid JSON format")
        return []


def validate_case(case):
    # 校验必填字段
    assert "id" in case, "Missing case ID"
    return case


def filter_testcases(raw_cases, case_num=20, test_level="单元"):
    """
    根据用例数量和测试级别筛选测试用例

    :param raw_cases: 原始用例列表，每个元素为字典格式
    :param case_num: 需要返回的用例数量（默认20）
    :param test_level: 测试级别（单元/集成/系统）
    :return: 筛选后的用例列表
    """
    # 条件过滤（网页7多条件筛选逻辑）
    filtered = [
        case for case in raw_cases
        if case["type"] == test_level
           and case["status"] == "valid"  # 有效用例
    ]

    # 数量控制（网页8动态返回逻辑）
    return filtered[:min(case_num, len(filtered))]


def display_testcase_table(cases):
    """使用streamlit-aggrid展示增强型表格"""
    gb = GridOptionsBuilder.from_dataframe(
        pd.DataFrame(cases)[['id', 'name', 'priority', 'type', 'status']]
    )

    # 配置表格功能 [2](@ref)
    gb.configure_pagination(paginationPageSize=10)  # 分页显示
    gb.configure_default_column(
        filterable=True,  # 启用筛选
        sortable=True,  # 启用排序
        editable=False,
        groupable=True
    )

    # 配置行点击事件 [5](@ref)
    gb.configure_selection(selection_mode='single', use_checkbox=False)
    grid_options = gb.build()

    # 渲染表格
    grid_response = AgGrid(
        pd.DataFrame(cases),
        gridOptions=grid_options,
        height=400,
        width='100%',
        theme='streamlit',
        update_mode='MODEL_CHANGED'
    )

    # 处理行点击事件
    selected_rows = grid_response['selected_rows']
    if selected_rows:
        show_case_detail(selected_rows[0])


def show_case_detail(case):
    """展示用例详细信息"""
    with st.expander(f"📑 用例详情 - {case['id']} {case['name']}", expanded=True):
        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown("**基础信息**")
            st.metric("优先级", ["低", "中", "高"][case['priority'] - 1])
            st.metric("测试类型", case['type'])
            st.metric("执行状态", ["未执行", "通过", "失败", "阻塞"][case['status']])

        with col2:
            st.markdown("**测试步骤**")
            for i, step in enumerate(case['steps'], 1):
                st.markdown(f"{i}. {step['action']}")
                if step.get('data'):
                    st.caption(f"输入数据：{step['data']}")

            st.divider()
            st.markdown("**预期结果**")
            for expect in case['expectations']:
                st.markdown(f"- ✅ {expect}")
