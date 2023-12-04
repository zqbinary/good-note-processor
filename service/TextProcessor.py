from collections import Counter
import pyperclip
import statistics


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

    def action(self):
        # 示例文本
        chinese_counts = self.count_char()
        print("每行中文字数统计：", chinese_counts)
        most_common = self.most_common_count(chinese_counts)
        print("频率最高的字数是：", most_common)
        processed_text = self.merge_lines_with_difference(most_common)
        print("<------------------")
        print(processed_text)
        print("------------------>")
        if 'clipboard' == self.typ:
            print('copy!')
            pyperclip.copy(processed_text)

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
