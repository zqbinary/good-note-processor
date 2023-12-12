import json
import re
import time

from bs4 import BeautifulSoup
import requests
import os
from service.Notification import notify


class HtmlProcessor:
    origin_file = 'templates/origin.html'
    output_file = 'templates/out.html'
    data_file = 'templates/data.json'
    root = ''

    def __init__(self, type='file', origin_html=''):
        if type == 'file':
            self.html_content = self.read_html_file()
        if type == 'html':
            self.html_content = self.gen_html(origin_html)
            self.save_origin_html()
        self.location = self.load_location()

    @classmethod
    def set_root(cls, f):
        cls.root = f

    @classmethod
    def set_file_dir(cls, data_file, origin_file, output_file):
        cls.data_file = data_file
        cls.origin_file = origin_file
        cls.output_file = output_file

    @classmethod
    def load_location(cls):
        with open(cls.data_file, 'r') as file:
            return json.load(file)

    @classmethod
    def dump_location_from_str(cls, string):
        with open(cls.data_file, 'w', encoding='utf-8') as file:
            file.write(string)
        pass

    def do(self, is_download_img=True):
        self.soup = BeautifulSoup(self.html_content, 'html.parser')
        self.format_html()
        if is_download_img:
            self.download_images()
            self.save_origin_html()

        self.save_out_html()
        notify()

    def read_html_file(self):
        with open(self.origin_file, 'r', encoding='utf-8') as file:
            return file.read()

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
                <title>Copy page</title>
                <link rel="icon" type="image/x-icon" href="/static/zq-static/favicon.ico" />
                <link href="/static/zq-static/zq-main.css?t={}" rel="stylesheet" />
            </head>
            <body>
            <div class="zq-main">
        """.format(time.time())
        html += origin_html
        html += "</div></body></html>"
        return html

    def format_origin_html(self, origin_html):
        pass

    def save_origin_html(self):
        with open(self.origin_file, 'w', encoding='utf-8') as file:
            file.write(self.html_content)
        pass

    def save_out_html(self):
        with open(self.output_file, 'w', encoding='utf-8') as file:
            res = str(self.soup)
            file.write(res)
        # 去掉空行

        self.remove_empty_line()
        print("处理后的 HTML 内容已保存到 {} 文件".format(self.output_file))

    def remove_empty_line(self):
        with open(self.output_file, 'r', encoding='utf-8') as file:
            res = file.read()
            with open(self.output_file, 'w', encoding='utf-8') as f2:
                res = re.sub(r'\n\n', r'\n', res)
                res = re.sub(r'\n\n', r'\n', res)
                f2.write(res)

    def download_images(self):
        images = self.soup.find_all('img')

        for idx, img in enumerate(images):
            img_url = img.get('src')

            response = requests.get(img_url)
            if response.status_code > 400:
                print(f"下载失败，图片 {img_url}，状态码:", response.status_code)
            filename = self.get_img_filename(idx, img_url, response.headers.get('Content-Type'))
            filename_download = os.path.join(self.root, 'static', filename)
            with open(filename_download, "wb") as file:
                file.write(response.content)
            print(f"图片 {img_url} 已成功下载到本地")

            img['src'] = '/static/' + filename

    def get_img_filename(self, idx, image_url, content_type):
        # 获取 Content-Type 头部信息
        image_format = 'png'
        if content_type:
            image_format = content_type.split('/')[-1]  # 获取 Content-Type 中的格式部分
        image_extension = image_format
        return os.path.join('p' + str(idx) + '.' + image_extension)

    def format_html(self):
        self.format_imgs()
        self.format_code_pres()

    def format_imgs(self):
        images = self.soup.find_all('img')
        for img in images:
            img_url = img.get('src')
            if img_url.startswith('/'):
                img['src'] = self.location['origin'] + img_url
                print(img)

    def format_code_pres(self):
        pres = self.soup.find_all('pre')
        for pre_tag in pres:
            # 获取pre标签的文本内容
            pre_text = pre_tag.get_text()
            pre_text_with_nbsp = re.sub(r'^( +)'
                                        , lambda match: '\u00A0' * len(match.group(1))
                                        , pre_text
                                        , flags=re.MULTILINE)
            pre_text = pre_text_with_nbsp
            # 按行分割文本内容
            lines = pre_text.splitlines()

            # 创建一个新的div标签用于替换pre标签
            new_div = self.soup.new_tag('pre')

            new_div['class'] = pre_tag.get('class')
            # 将每行文本放入一个单独的div中，并添加到新的div标签中
            for line in lines:
                line_div = self.soup.new_tag('div')
                line_div.string = line
                new_div.append(line_div)
            pre_tag.replace_with(new_div)

            new_div.insert_before(self.soup.new_tag('br'))
            new_div.insert_after(self.soup.new_tag('br'))
            # pre_tag.string = new_div.get_text()
