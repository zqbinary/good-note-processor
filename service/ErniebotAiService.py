import os

import erniebot
from dotenv import load_dotenv
from langchain.chains import AnalyzeDocumentChain
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.chat_models import ErnieBotChat

load_dotenv()


class ErniebotAiService:

    def get_summary_with_map_reduce(self, content, title):
        CHAIN_TYPE = "map_reduce"
        llm = ErnieBotChat()
        # 定义文本分割器 每块文本大小为500，不重叠
        text_splitter = CharacterTextSplitter(
            chunk_size=3000,
            chunk_overlap=100,
            length_function=len,
        )

        # 生成摘要
        summary_chain = load_summarize_chain(llm, chain_type=CHAIN_TYPE)
        summarize_document_chain = AnalyzeDocumentChain(combine_docs_chain=summary_chain, text_splitter=text_splitter)
        res = summarize_document_chain.run(contents=content)
        print("re", res)

        #####

    def get_summary_from_content(self, title, content):
        template = """
            你是善于总结归纳的文本助理。我将提供文档内容，你需要提取要点整理文章大纲。
            要求返回文本格式，要点前面带*，不要用数字。
            如果无法整理就说你无法整理。如果文档标题无意义,比如是一串数字或字母，就忽略标题。
            文档标题：{name}
            文档内容：{ctx}
            """
        template1 = """
            你是善于总结归纳的文本助理。我将提供文档内容，你整理出目录，生成格式md。
            如果无法整理就说你无法整理。如果文档标题无意义,比如是一串数字或字母，就忽略标题。
            文档标题：{name}
            文档内容：{ctx}
            """

        prompt = PromptTemplate.from_template(template)
        message = prompt.format(name=title, ctx=content)
        erniebot.api_type = "aistudio"
        erniebot.access_token = os.getenv('AISTUDIO_TOKEN')
        erniebot.proxy = "http://127.0.0.1:7890"
        # erniebot.ChatCompletion.temperature = 0.5
        response = erniebot.ChatCompletion.create(model="ernie-3.5",
                                                  messages=[{"role": "user", "content": message}],
                                                  temperature=0.1,
                                                  )

        print(response)
        return response.get_result()
