import os
import statistics

import pyperclip
import zhipuai
from dotenv import load_dotenv

from service.Notification import notify

load_dotenv()


class TextProcessor:
    # 频率最高的偏差
    abs_value = 10
    line_min_count = 20

    def __init__(self, typ='clipboard', text=''):
        self.typ = typ
        if 'clipboard' == typ:
            text = self.read_clipboard_content()
        if 'input' == typ:
            text = text
        self.text = text.strip()

    def action(self, mode='man'):
        processed_text = ''
        if mode == 'man':
            processed_text = self.man_process()
        if mode == 'ai':
            processed_text = self.ai_process()
        if not processed_text:
            return
        return self.out(processed_text)

    def out(self, processed_text):
        if 'clipboard' == self.typ:
            print('copy!')
            pyperclip.copy(processed_text)
        print("<------output------------")
        print(processed_text)
        print("------output------------>")
        notify('clipboard process success')

    def man_process(self):
        chinese_counts = self.count_char()
        print("每行中文字数统计：", chinese_counts)
        most_common = self.most_common_count(chinese_counts)
        print("频率最高的字数是：", most_common)
        processed_text = self.merge_lines_with_difference(most_common)
        print("<------------------")
        print(processed_text)
        return processed_text

    def ai_process(self):
        content_pre = """
              这里是一段ocr识别的内容，我需要你帮我修正其中的错别字，去掉多余的换行，增加可阅读性。
              仅仅输出处理结果即可。文本如下：
               """
        zhipuai.api_key = os.getenv('zhipuai_api_key')
        try:
            response = zhipuai.model_api.sse_invoke(
                model="chatglm_turbo",
                prompt=[{
                    "role": "user",
                    "content": content_pre + self.text
                }],
                temperature=0,
                incremental=False
            )
        except Exception as e:
            print('ai connected error:', str(e))
            exit('500')
        res = ''
        try:
            for event in response.events():
                if event.event == "finish":
                    res = event.data
        except Exception as e:
            print(e)
        return res

    def merge_lines_with_difference(self, line_count_computed):
        # 频率最高的不足10
        if line_count_computed < TextProcessor.line_min_count:
            return self.text

        lines = self.text.split('\n')
        merged_lines = [lines[0]]

        for i in range(1, len(lines)):
            # abs(0，-1) <
            flag = ((abs(len(lines[i]) - len(lines[i - 1])) < TextProcessor.abs_value)
                    and (abs(len(lines[i - 1]) - line_count_computed) < TextProcessor.abs_value))
            # 最后一条合并
            if i == len(lines) - 1:
                flag = True

            if flag:
                merged_lines[-1] += lines[i]
            else:
                merged_lines.append(lines[i])

        return '\n'.join(merged_lines)

    def count_char(self):
        lines = self.text.split('\n')
        char_count = []

        for line in lines:
            if line:
                chinese_count = len(line.strip())  # 使用正则表达式匹配中文字符
            else:
                chinese_count = 0
            char_count.append(chinese_count)

        return char_count

    def most_common_count(self, line_counts):
        line_counts = [num for num in line_counts if num > self.line_min_count]
        if not len(line_counts):
            return self.line_min_count
        print("行字数：", line_counts)
        c1 = sum(line_counts) / len(line_counts)
        c2 = statistics.median(line_counts)
        print("平均数：", c1)
        print("中位数：", c2)
        return (c1 + c2) / 2

    def read_clipboard_content(self):
        clipboard_content = pyperclip.paste()
        return clipboard_content
