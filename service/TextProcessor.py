from collections import Counter
import pyperclip

abs_value = 5


class TextProcessor:
    def merge_lines_with_difference(self, text, line_count):
        lines = text.split('\n')
        merged_lines = [lines[0]]

        for i in range(1, len(lines)):
            flag = (abs(len(lines[i]) - len(lines[i - 1])) <= abs_value
                    and abs(len(lines[i - 1]) - line_count) <= abs_value)
            if i == len(lines) - 1:
                flag = True
            if flag:
                merged_lines[-1] += lines[i]
            else:
                merged_lines.append(lines[i])

        return '\n'.join(merged_lines)

    def count_charater(self, text):
        lines = text.split('\n')
        chinese_counts = []

        for line in lines:
            chinese_count = len(line)  # 使用正则表达式匹配中文字符
            chinese_counts.append(chinese_count)

        return chinese_counts

    def most_common_count(self, chinese_counts):
        count_freq = Counter(chinese_counts)
        most_common = count_freq.most_common(1)

        return most_common[0][0]

    def read_clipboard_content(self):
        clipboard_content = pyperclip.paste()
        return clipboard_content

    def action(self):
        # 示例文本
        example_text = self.read_clipboard_content()
        example_text = example_text.strip()
        chinese_counts = self.count_charater(example_text)
        most_common = self.most_common_count(chinese_counts)
        print("每行中文字数统计：", chinese_counts)
        print("频率最高的字数是：", most_common)
        processed_text = self.merge_lines_with_difference(example_text, most_common)
        print(processed_text)
        pyperclip.copy(processed_text)
