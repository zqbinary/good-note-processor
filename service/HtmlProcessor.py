import os
import re
import time
from concurrent.futures import ThreadPoolExecutor

import requests
from bs4 import BeautifulSoup

from service.HtmlRuleStrategy import StrategyFactory
from service.WebProcessor import WebProcessor


class HtmlProcessor(WebProcessor):

    def __init__(self, kind='file', origin_html=''):
        self.soup = None
        if kind == 'file':
            self.html_content = self.read_origin_file()
        if kind == 'html':
            self.html_content = self.gen_html(origin_html)
            self.save_origin_html()
        self.location = self.load_location()

    def do(self, is_download_img=True):
        self.soup = BeautifulSoup(self.html_content, 'html.parser')
        self.format_html()
        if is_download_img:
            self.download_images()
            self.save_origin_html()

        self.save_out_html()
        # notify('生成out.html')

    def gen_html(self, origin_html):
        html = ""
        prism = """
                <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.25.0/themes/prism.min.css" rel="stylesheet" />
                <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.25.0/prism.min.js"></script>
                <!-- 这里可以添加其他语言的扩展，比如对应语言的 JavaScript 文件 -->
                <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.25.0/components/prism-javascript.min.js"></script>
        """
        html += r"""
        <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>Copy Page</title>
                <link rel="icon" type="image/x-icon" href="/static/zq-static/favicon.ico" />
                <link href="/static/zq-static/zq-main.css?t={}" rel="stylesheet" />
            </head>
            <body>
            <div class="zq-main">
        """.format(time.time())
        html += origin_html
        html += "</div></body></html>"
        return html

    def save_origin_html(self):
        with open(self.origin_file, 'w', encoding='utf-8') as file:
            file.write(self.html_content)
        pass

    def save_out_html(self):
        with open(self.output_file, 'w', encoding='utf-8') as file:
            res = str(self.soup)
            file.write(res)
        self.remove_empty_line()
        print("处理后的 HTML 内容已保存到 {} 文件".format(self.output_file))

    def save_html_html(self):
        with open(self.output_table_file, 'w', encoding='utf-8') as file:
            res = str(self.soup)
            file.write(res)
        self.remove_empty_line()
        print("处理后的 HTML 内容已保存到 {} 文件".format(self.output_table_file))

    def download_image(self, idx, img):
        img_url = img.get('src')

        try:
            response = requests.get(img_url)
        except Exception as e:
            print('download img error', str(e))
            return

        if response.status_code > 400:
            print(f"下载失败，图片 {img_url}，状态码:", response.status_code)
            return
            # todo image类型
        filename = self.get_img_filename(idx, img_url, response.headers.get('Content-Type'))
        filename_download = os.path.join(self.root, 'static', filename)
        with open(filename_download, "wb") as file:
            file.write(response.content)
        print(f"图片 {img_url} 已成功下载到本地")

        img['src'] = '/static/' + filename

    def download_images(self):
        images = self.soup.find_all('img')
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(self.download_image, idx, img) for idx, img in enumerate(images)]
            for future in futures:
                future.result()

    @classmethod
    def get_img_filename(cls, idx, image_url, content_type):
        # 获取 Content-Type 头部信息
        ['gif', 'jpeg', 'png', 'webp']
        image_format = 'png'
        if content_type:
            image_format = content_type.split('/')[-1]  # 获取 Content-Type 中的格式部分
        image_extension = image_format
        return os.path.join('p' + str(idx) + '.' + image_extension)

    def format_html(self):
        self.format_imgs()
        self.format_code_pres()
        self.rule_format()

    def format_imgs(self):
        images = self.soup.find_all('img')
        for img in images:
            img_url = img.get('src')
            if img_url.startswith('/'):
                img['src'] = self.location['origin'] + img_url

    def format_code_pres(self):
        remove_selector = [
            '.pre-numbering',
            'button'
        ]
        WebProcessor.remove_eles_by_selectors(remove_selector, self.soup)
        for li in self.soup.find_all('li'):
            d = self.soup.new_tag('div')
            li.wrap(d)
            # if li 下只有一个tag
            if len(li.contents) == 1 and li.find():
                li.find().insert(0, " * ")
            else:
                li.insert(0, " * ")
            li.unwrap()
        pres = self.soup.find_all('pre')
        for pre_tag in pres:
            pre_text = pre_tag.get_text()
            pre_text = pre_text.replace(' ', '\u00A0')
            pre_text = pre_text.replace('\t', '\u00A0\u00A0\u00A0\u00A0')
            """
            pre_text = re.sub(r'^( +)'
                              , lambda match: '\u00A0' * len(match.group(1))
                              , pre_text
                              , flags=re.MULTILINE)
"""
            # 按行分割文本内容
            lines = pre_text.splitlines()

            pre_new = self.soup.new_tag('div')

            # new_div['class'] = pre_tag.get('class')
            pre_new['class'] = 'q-code'
            # 将每行文本放入一个单独的div中，并添加到新的div标签中
            for line in lines:
                line_div = self.soup.new_tag('div')
                line_div.string = line
                pre_new.append(line_div)
            pre_tag.replace_with(pre_new)

            pre_new.insert_before(self.soup.new_tag('br'))
            pre_new.insert_after(self.soup.new_tag('br'))
            # pre_tag.string = new_div.get_text()

    def rule_format(self):
        strategy = StrategyFactory().get_strategy(self.location['host'], self.soup)
        if strategy:
            strategy.apply_rule(self.location)
