from autogen import AssistantAgent, UserProxyAgent


def initialize_agents(llm_config, test_level="单元"):
    """根据测试级别初始化不同角色的智能体"""

    # 角色配置模板（网页3的SRE工程师案例启发）
    agent_profiles = {
        "单元": {
            "analyst": {
                "name": "单元测试分析师",
                "system_message": "专注函数级测试，识别边界值和异常流场景。\n"
                                  "输出格式要求：每个用例必须包含输入参数、预期输出、异常捕获逻辑"
            },
            "designer": {
                "name": "白盒测试设计师",
                "system_message": "根据代码逻辑生成路径覆盖用例，需包含：\n"
                                  "- 语句覆盖\n- 条件覆盖\n- 路径覆盖矩阵"
            }
        },
        "集成": {
            "analyst": {
                "name": "集成测试分析师",
                "system_message": "专注功能模块的可用性、完整性、正确性测试，识别边界值，要求包含：\n"
                                  "1. 数据流验证用例\n2. 接口兼容性矩阵\n3. 异常传递场景"
            },
            "designer": {
                "name": "集成测试设计员",
                "system_message": "根据需求功能的测试点和影响点生成集成测试用例，严格遵循以下规则：\n"
                                  "1. 仅生成功能测试用例，禁止包含自动化代码\n"
                                  "2. 测试用例元素必须包含：\n"
                                  "   - 用例ID\n   - 标题\n   - 优先级\n   - 前提条件\n   - 步骤\n   - 期望结果\n"
                                  "3. 设计方法必须使用：\n"
                                  "   - 等价类划分\n   - 边界值分析\n   - 错误推断法等\n"
                                  "4. 只需要生成自然语言的功能测试用例"
            }
        },
        "系统": {
            "analyst": {
                "name": "端到端架构师",
                "system_message": "设计业务流程测试，要求：\n"
                                  "1. 用户旅程图（CJM）驱动\n2. 跨系统数据一致性检查\n3. 性能基线指标"
            },
            "designer": {
                "name": "系统测试工程师",
                "system_message": "生成生产环境验证用例，包含：\n"
                                  "- 监控指标阈值（如CPU>90%持续5分钟）\n"
                                  "- 日志模式检测规则\n- 告警触发条件"
            }
        }
    }

    # 动态选择角色配置（网页3的graph_dict思路）
    role_config = agent_profiles[test_level]

    # 初始化核心代理（参考网页2的UserProxyAgent配置）
    analyst = AssistantAgent(
        name=role_config["analyst"]["name"],
        llm_config=llm_config,
        system_message=role_config["analyst"]["system_message"]
    )

    designer = AssistantAgent(
        name=role_config["designer"]["name"],
        llm_config=llm_config,
        system_message=role_config["designer"]["system_message"]
    )

    # 用户代理配置
    user_proxy = UserProxyAgent(
        name="质量保障主管",
        human_input_mode="TERMINATE",
        max_consecutive_auto_reply=3,  # 减少自动回复次数
        is_termination_msg=lambda x: "用例生成完成" in x.get("content", "") or x.get("content", "").endswith(
            "TERMINATE"),
        code_execution_config={"work_dir": "groupchat", "use_docker": False},
        system_message="当检测到完整用例且数量达标时，回复『用例生成完成』并附加TERMINATE"
    )

    # 定义代理间交互规则（网页3的graph_dict实现）
    transition_rules = {
        user_proxy: [analyst],
        analyst: [designer],
        designer: [user_proxy]  # 形成闭环验证流程
    }

    return [user_proxy, analyst, designer], transition_rules