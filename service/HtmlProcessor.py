from bs4 import BeautifulSoup
import requests
import os

output_file = 'out.html'
origin_file = 'origin.html'


class HtmlProcessor:
    def __init__(self, html_origin):
        self.origin = html_origin
        self.html_content = self.gen_html()
        self.save_origin_html()
        self.soup = BeautifulSoup(self.html_content, 'html.parser')
        self.format_html()
        self.download_images()

    def read_html_file(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def gen_html(self):
        html = ""
        html += """
        <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>Title</title>
                <style>div img {width:80%;}</style>
            </head>
            <body>
            <div style="width:500px;">
        """
        html += self.origin
        html += "</div></body></html>"
        return html

    def save_origin_html(self):
        with open('templates/' + origin_file, 'w', encoding='utf-8') as file:
            file.write(self.html_content)
        pass

    def download_images(self):
        images = self.soup.find_all('img')

        for img in images:
            img_url = img.get('src')

            response = requests.get(img_url)

            if response.status_code == 200:
                filename = os.path.basename(img_url)
                filename_download = os.path.join('static', filename)
                with open(filename_download, "wb") as file:
                    file.write(response.content)
                print(f"图片 {img_url} 已成功下载到本地")

                img['src'] = 'static/' + filename
            else:
                print(f"下载失败，图片 {img_url}，状态码:", response.status_code)

        with open('templates/' + output_file, 'w', encoding='utf-8') as file:
            file.write(self.soup.prettify())
        print("处理后的 HTML 内容已保存到 {}.html 文件".format(output_file))

    def format_html(self):
        # for p_tag in self.soup.find_all('p'):
        #     new_tag = self.soup.new_tag('div')  # 创建一个新的 <div> 标签
        #     new_tag.string = p_tag.string  # 将 <div> 的内容设置为 <p> 的内容
        #     p_tag.replace_with(new_tag)  # 用 <div> 标签替换 <p> 标签
        pass
