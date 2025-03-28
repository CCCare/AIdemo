import re
from io import StringIO

import pandas as pd
from langchain.chains import TransformChain
from common.llm import LLM

template = """分析以下错误日志，找出根本原因：
                {logs}
                按以下格式输出：        
                1. 主要异常类型        
                2. 高频错误关键词        
                3. 修复建议"""

class LogAnalyzer:
    """
    通过LangChain处理日志文件，利用DeepSeek的NLP能力提取关键错误信息，生成分析报告。
    """

    def __init__(self):
        self.llm = LLM()

    def generate(self,log_path,pattern):
        buffer = self._read_buffer(log_path, pattern)
        df = pd.read_csv(buffer, names=['timestamp', 'level', 'message'])
        critical_logs = df[df['level'].str.contains('ERROR') | df['level'].str.contains('error')]

        analysis_chain = TransformChain(transform=self._analyze_logs, input_variables=["logs"],
                                        output_variables=["report"])
        result = analysis_chain.invoke({"logs": critical_logs.to_dict()})
        assert result['report']
        print(result['report'].content)

    @staticmethod
    def _read_buffer(log_path, pattern):
        buffer = StringIO()
        with open(log_path) as f:
            for line in f:
                match = re.match(pattern, line.strip())
                if match:
                    buffer.write(','.join([  # 生成CSV格式数据
                        match.group(1).replace(',', '.'),  # 时间戳数据逗号替换为英文句号
                        match.group(2),
                        match.group(3).replace(',', ';')  # 处理消息中的逗号
                    ]) + '\n')

        buffer.seek(0)
        return buffer

    def _analyze_logs(self, inputs):
        return {"report": self.llm.invoke(template.format(logs=inputs["logs"]))}


if __name__ == '__main__':
    gen = LogAnalyzer()
    gen.generate("caselogs/app.log","^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})\s+([A-Z]+)\s+(.*)")
    gen.generate("caselogs/jmeter.log",'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})\s+([A-Z]+)\s+(.*)')