import json
import time
from urllib.parse import urlparse

from bs4 import BeautifulSoup
import requests
import os


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

    def read_html_file(self):
        with open(self.origin_file, 'r', encoding='utf-8') as file:
            return file.read()

    def gen_html(self, origin_html):
        html = ""
        html += """
        <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>Copy Copy</title>
                <link rel="stylesheet" href="/static/zq-css/zq-main.css?t={}">
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
            file.write(self.soup.prettify())
        print("处理后的 HTML 内容已保存到 {} 文件".format(self.output_file))

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
        # filename = os.path.basename(image_url)

        # image_name_without_extension, image_extension = os.path.splitext(filename)
        # if not image_extension:
        image_extension = image_format
        # if image_extension.startswith('.'):
        #     image_extension = image_format[1:]
        return os.path.join('p' + str(idx) + '.' + image_extension)

    def format_html(self):
        images = self.soup.find_all('img')
        for img in images:
            img_url = img.get('src')
            if img_url.startswith('/'):
                img['src'] = self.location['origin'] + img_url
                print(img)
