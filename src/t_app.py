from service.HtmlProcessor import HtmlProcessor

from service.OutlineProcessor import OutlineProcessor
from service.TableProcessor import TableProcessor


def t_table():
    processor = TableProcessor('file')
    processor.do()


def t_outline():
    processor = OutlineProcessor('file')
    processor.do()


def t_html():
    processor = HtmlProcessor('file')
    processor.do()


if __name__ == '__main__':
    t_html()
    # t_outline()
    # t_table()
