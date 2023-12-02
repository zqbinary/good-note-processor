import os
from unittest import TestCase

from service.HtmlProcessor import HtmlProcessor


class TestHtmlProcessor(TestCase):
    current_directory = ''

    @classmethod
    def setUpClass(cls) -> None:
        cnt_dir = os.path.dirname(__file__)
        cls.current_directory = os.path.abspath(os.path.join(cnt_dir, '..', '..'))

    def gen_test_file_path(self, case_name, filename):
        return os.path.join(self.current_directory, 'templates', 'tests', case_name, filename)

    def test_segment(self):
        data_file = self.gen_test_file_path('sg', 'data.json')
        origin_file = self.gen_test_file_path('sg', 'origin.html')
        out_file = self.gen_test_file_path('sg', 'out.html')
        HtmlProcessor.set_root(self.current_directory)
        HtmlProcessor.set_file_dir(data_file, origin_file, out_file)
        processor = HtmlProcessor('file')
        processor.do()
        self.assertTrue(True)

    def test_csdn(self):
        case_name = 'csdn'
        data_file = self.gen_test_file_path(case_name, 'data.json')
        origin_file = self.gen_test_file_path(case_name, 'origin.html')
        out_file = self.gen_test_file_path(case_name, 'out.html')
        HtmlProcessor.set_root(self.current_directory)
        HtmlProcessor.set_file_dir(data_file, origin_file, out_file)
        processor = HtmlProcessor('file')
        processor.do()
        self.assertTrue(True)

    def test_juejin(self):
        case_name = 'juejin'
        data_file = self.gen_test_file_path(case_name, 'data.json')
        origin_file = self.gen_test_file_path(case_name, 'origin.html')
        out_file = self.gen_test_file_path(case_name, 'out.html')
        HtmlProcessor.set_root(self.current_directory)
        HtmlProcessor.set_file_dir(data_file, origin_file, out_file)
        processor = HtmlProcessor('file')
        processor.do()
        self.assertTrue(True)
