from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from common.llm import LLM

template="""将以下需求转换为Gherkin格式测试用例：
{requirement}
输出格式：
功能: [功能名称]
场景: [场景描述]
当[条件]
且[条件]
那么[结果]"""

class CaseGenerator:
    """生成测试用例"""

    def __init__(self):
        self.prompt = PromptTemplate(
            input_variables=["requirement"],
            template=template
        )
        self.llm = LLM()
        self.llm_chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def generate(self,requirement):
        output = self.llm_chain.invoke({"requirement": requirement})['text']
        print("\n")
        print(output)
        assert output,'测试用例未生成'


if __name__ == '__main__':
    gen = CaseGenerator()
    gen.generate(requirement="用户登录功能需验证手机号格式和验证码有效期")