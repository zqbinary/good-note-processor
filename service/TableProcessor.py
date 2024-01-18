from bs4 import BeautifulSoup

from service.BaseProcessor import BaseProcessor

BR = '<div><br></div>'
BLOCK_START = '<table style="border-collapse: collapse; min-width: 100%"><colgroup><col style="width: 839px"><col style="width: 413px"></colgroup>'
TR_START = '<tr><td style="width: 839px; padding: 8px; border: 1px solid">'
TR_END = '</td><td style="width: 413px; padding: 8px; border: 1px solid;"><div><br /></div></td>'
BLOCK_END = '</tr></tbody></table>'
SEPERATOR = 'q-hr'


class TableProcessor(BaseProcessor):
    def __init__(self, kind='file', origin_html=''):
        self.soup = None
        if kind == 'file':
            self.html_content = self.read_origin_file()
        self.location = self.load_location()
        self.seperator_hn = 'h2'

    def __format_table_html(self):
        hn_tags = self.soup.find_all('h2')
        self.__process_head()
        # return
        # 将每个 h2 标签和其后的内容合并为一块
        zi = 0
        ZI_COUNT_SEPERATOR = 300
        ZI_COUNT_SEPERATOR_LIMIT = 10
        ZI_LINE_SEPERATOR = 10
        for tag in hn_tags:
            contents = []
            ele = tag.find_next_sibling()
            while ele and ele.name != 'h2':
                seperator_flag = True
                seperator_next_h_flag = False
                if ele.name:
                    zi_cnt = len(str(ele.get_text()))
                    zi += zi_cnt
                    ele_next = ele.find_next_sibling()
                    if ele_next and 'name' in ele_next and ele_next.name == 'br':
                        ele_next = ele_next.find_next_sibling()
                    # 如果下一段是h,就换换行
                    if ele_next and ele_next.name and ele_next.name.startswith('h'):
                        seperator_next_h_flag = True
                    # 如果当行字少，就不换行
                    if zi_cnt < ZI_COUNT_SEPERATOR_LIMIT:
                        seperator_flag = False
                    contents.append(ele)
                    if (zi > ZI_COUNT_SEPERATOR or seperator_next_h_flag) and seperator_flag:
                        contents.append(self.soup.new_tag(SEPERATOR))
                        zi = 0
                ele = ele.find_next_sibling()
            self.__block_to_table(contents, tag)

    def __process_head(self):
        contents = []
        tag = self.soup.body.div.find()
        contents = self.__get_pre_contents(tag, contents)
        self.__pre_to_table(contents, tag)

    def __get_pre_contents(self, tag, contents):
        tag_cnt = tag
        if not tag_cnt or not tag_cnt.name:
            return contents
        while tag_cnt and tag_cnt.name and tag_cnt.name != 'h2':
            if tag_cnt.find('h2'):
                return self.__get_pre_contents(tag_cnt.find(), contents)
            else:
                contents.append(tag_cnt)
                tag_cnt = tag_cnt.find_next_sibling()
        return contents

    def __pre_to_table(self, contents, tag):
        # meta
        table_meta = self.__gen_container()
        a = self.soup.new_tag('a', href=self.location['href'], target='_blank')
        a.string = self.location['title']
        table_meta.find('td').find_next_sibling().insert(0, a)
        self.soup.div.insert(0, table_meta)
        # header
        table = self.__gen_container()
        td = table.find('td')
        for child in contents:
            if child.name == SEPERATOR:
                td.append(self.soup.new_tag('br'))
                tr_str = TR_START + TR_END + '</tr>'
                td.parent.parent.append(BeautifulSoup(tr_str, 'html.parser'))
                td = td.parent.find_next_sibling().find('td')
                continue
            else:
                td.append(child)
        self.soup.div.insert(1, table)

    def __block_to_table(self, contents, tag):
        table = self.__gen_container()
        td = table.find('td')
        for child in contents:
            if child.name == SEPERATOR:
                td.append(self.soup.new_tag('br'))
                tr_str = TR_START + '<br>' + TR_END + '</tr>'
                td.parent.parent.append(BeautifulSoup(tr_str, 'html.parser'))
                td = td.parent.find_next_sibling().find('td')
                continue
            else:
                td.append(child)
        tag.insert_after(table)
        # self.soup.div.append(table)
        table.find('td').insert(0, tag)
        table2 = self.__gen_container()
        table.insert_before(table2)
        table.unwrap()

    def __gen_container(self):
        html_content = '<br>' + BLOCK_START + TR_START + TR_END + BLOCK_END
        div_tag = self.soup.new_tag('div')
        div_tag.append(BeautifulSoup(html_content, 'html.parser'))
        return div_tag

    def do(self):
        with open(self.output_file, 'r', encoding='utf-8') as file:
            out_file = file.read()
        self.soup = BeautifulSoup(out_file, 'html.parser')
        self.__prepare_to_format()
        self.__format_table_html()
        self.save_to_html()

    def save_to_html(self):
        with open(self.output_table_file, 'w', encoding='utf-8') as file:
            res = str(self.soup)
            file.write(res)
        self.remove_empty_line()
        print("处理后的 HTML 内容已保存到 {} 文件".format(self.output_table_file))

    def __prepare_to_format(self):
        for doc in self.soup.find_all('h2'):
            if doc.parent and doc.parent.name and doc.parent.name != '':
                pass
        for tbl in self.soup.find_all('table'):
            table_div = self.soup.new_tag("div", attrs={"class": "q-table"})

            # 获取原始表格中的行数据并创建相应的<div>元素
            for row in tbl.find_all('tr'):
                row_div = self.soup.new_tag("div", attrs={"class": "q-table-row"})
                for cell in row.find_all(['td', 'th']):
                    cell_div = self.soup.new_tag("div", attrs={"class": "q-table-cell"})
                    cell_div.string = cell.get_text(strip=True)
                    row_div.append(cell_div)
                table_div.append(row_div)

            tbl.replace_with(table_div)
    def read_output_from_file(self):
        with open(self.output_table_file, 'r', encoding='utf-8') as file:
            return file.read()


if __name__ == '__main__':
    processor = TableProcessor('file')
    processor.do()
