import json
from langchain.output_parsers import StructuredOutputParser, ResponseSchema

from common.llm import LLM


class AssertionGenerator:
    """
    智能断言生成‌：用DeepSeek理解测试输出，生成动态断言条件，代替硬编码的断言。五、智能断言生成器
    """
    def __init__(self):
        self.llm = LLM()
        self.parser = StructuredOutputParser.from_response_schemas([
            ResponseSchema(
                name="assert_type",
                type="string",
                description="断言类型，例如：相等、包含等"  # 必填
            ),
            ResponseSchema(
                name="expected_value",
                type="string",
                description="期望的对比值，例如：200、'success'等"
            ),
            ResponseSchema(
                name="condition",
                type="string",
                description="断言条件，例如：大于、不等于等"
            )
        ])

    def generate(self,response_data):
        prompt = f"""根据API响应生成验证断言：
        {json.dumps(response_data)}
        输出格式：        
        {self.parser.get_format_instructions()}"""

        output = self.llm.invoke(prompt)
        # self.parser.parse(output.content)
        return output.content



if __name__ == '__main__':
    generator = AssertionGenerator()
    print(generator.generate({"status": "success", "data": {"user_id": 123, "balance": 150.5}}))