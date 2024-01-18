from abc import abstractmethod, ABCMeta
import re

from flask import json


class BaseProcessor(metaclass=ABCMeta):
    origin_file = 'templates/origin.html'
    output_file = 'templates/out.html'
    outline_file = 'templates/outline.html'
    output_table_file = 'templates/table.html'
    data_file = 'templates/data.json'
    root = ''

    @abstractmethod
    def do(self):
        pass

    @abstractmethod
    def save_to_html(self):
        pass

    @abstractmethod
    def read_output_from_file(self):
        pass

    @staticmethod
    def remove_eles_by_selectors(selector_list, soup):
        for selector in selector_list:
            for element in soup.select(selector):
                element.decompose()

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
        with open(cls.data_file, 'r', encoding='utf-8') as file:
            return json.load(file)

    @classmethod
    def dump_location_from_str(cls, string):
        with open(cls.data_file, 'w', encoding='utf-8') as file:
            file.write(string)
        pass

    def read_origin_file(self):
        with open(self.origin_file, 'r', encoding='utf-8') as file:
            return file.read()

    def remove_empty_line(self):
        with open(self.output_file, 'r', encoding='utf-8') as file:
            res = file.read()
            with open(self.output_file, 'w', encoding='utf-8') as f2:
                res = re.sub(r'\n+', r'\n', res)
                f2.write(res)
