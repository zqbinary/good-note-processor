from bs4 import BeautifulSoup

from service.BaseProcessor import BaseProcessor
from service.ErniebotAiService import ErniebotAiService


class OutlineProcessor(BaseProcessor):
    def __init__(self, kind='file', origin_html=''):
        self.soup = None
        self.location = self.load_location()
        self.html_content = ''
        self.summary = ''

    def do(self):
        html_content = self.read_origin_file()
        self.soup = BeautifulSoup(html_content, 'html.parser')
        self.html_content = self.soup.get_text()
        self.summary = self.ai_summary(self.html_content)
        self.save_to_html()

    def save_to_html(self):
        with open(self.outline_file, 'w', encoding='utf-8') as file:
            # todo sse
            # res = f"<pre>{self.summary}</pr>"
            res = (f'<div style = "white-space: pre-wrap">{self.summary}</div>')
            file.write(res)

    def read_output_from_file(self):
        with open(self.outline_file, 'r', encoding='utf-8') as file:
            return file.read()

    def ai_summary(self, content):
        service = ErniebotAiService()
        title = self.location['title']
        return service.get_summary_from_content(title, content)
