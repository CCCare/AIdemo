from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from common.llm import LLM

template="""
        1. 将操作指令转换为Python selenium代码
        2. 使用chrome驱动，并通过ChromeDriverManager初始化
        3. 注意代码需要编译成功
        {instruction}
        """

class ScriptGenerator:
    """生成测试脚本，并执行"""

    def __init__(self):
        self.llm = LLM()

    def generate(self,instruction):
        prompt = PromptTemplate(
            input_variables=["instruction"],
            template=template.format(instruction=instruction)
        )
        llm_chain = LLMChain(llm=self.llm, prompt=prompt)
        output = llm_chain.invoke({"instruction": instruction})['text']
        print("\n")
        print(output)
        assert output,'测试用例未生成'

        script = self._sanitize_code(output)
        print("\n")
        print(script)
        assert self.compile(script), '代码编译失败'
        exec(script)

    def compile(self,code):
        try:
            compiled_code = compile(code, '<string>', 'exec')
            print("代码编译成功，没有错误。")
            return compiled_code
        except SyntaxError as e:
            print("代码编译失败：", e)
            return False
    def _sanitize_code(self, text):
        return text.split("```python")[1].split("```")[0]


if __name__ == '__main__':
    gen = ScriptGenerator()
    gen.generate("打开百度首页，搜索'LangChain测试'，验证结果包含'教程'")