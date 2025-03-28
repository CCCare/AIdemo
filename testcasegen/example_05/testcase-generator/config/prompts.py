PROMPT_TEMPLATE= """作为资深测试专家，请根据以下需求生成{test_level}测试用例：
{requirement}

要求：
1. 生成{case_num}个用例，包含以下类型：
   {test_type_condition}
2. 格式遵循：
{format_instruction}
"""

FORMAT_INSTRUCTION = """- 优先级分类(P0-P3)
- 包含正向/异常场景
- 边界值标注数值范围"""