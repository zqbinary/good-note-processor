import json
import re


class WebProcessor:
    origin_file = 'templates/origin.html'
    output_file = 'templates/out.html'
    output_table_file = 'templates/table.html'
    data_file = 'templates/data.json'
    root = ''

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

    def read_html_file(self):
        with open(self.origin_file, 'r', encoding='utf-8') as file:
            return file.read()

    def read_table_file(self):
        with open(self.output_table_file, 'r', encoding='utf-8') as file:
            return file.read()

    def remove_empty_line(self):
        with open(self.output_file, 'r', encoding='utf-8') as file:
            res = file.read()
            with open(self.output_file, 'w', encoding='utf-8') as f2:
                res = re.sub(r'\n\n', r'\n', res)
                res = re.sub(r'\n\n', r'\n', res)
                f2.write(res)


if __name__ == '__main__':
    pass
