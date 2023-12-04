from unittest import TestCase

from service.TextProcessor import TextProcessor


class TestTextProcessor(TestCase):
    def test_action(self):
        text = """
        抓包
停止抓包
清除清求
要跨页面加载保存请求：Preserve log
屏幕截图：Capture screenshots■
重新执行XHR请求：右键点击请求选择Replay XHR
停用浏览器缓存
手动清除浏览器缓存：右键点击请求选择Clear Browser Cache
离线模拟：Oine
模拟慢速网络连接：Network Throttling,可自定义网速
手动清除刘览器Cookie：右键点击请求选择Clear Browser Cookies
隐藏Filters窗格
隐藏Overview窗格
        """
        print(text)
        print("============")
        processor = TextProcessor('input', text)
        processor.action()
        self.assertTrue(True)

    def test_action1(self):
        text = """
        domain:仅显示来自指定域的资源。您可以使用通配符()来包括多个域。例如，.com显示
以.com结尾的所有域名中的资源。DevTools会在自动完成下拉菜单中自动填充它遇到的所有域。
has-response-header:显示包含指定HTTP响应头信息的资源。DevTools会在自动完成下拉菜单
中自动填充它遇到的所有响应头。
is:通过is:running找出WebSocket请求。
larger-than(大于)：显示大于指定大小的资源（以字节为单位）。设置值1000等效于设置值1k。
method(方法)：显示通过指定的HTTP方法类型检索的资源。DevTools使用它遇到的所有HTTP方
法填充下拉列表。
mime-type(mime类型：显示指定MIME类型的资源。DevTools使用它遇到的所有MIME类型填
充下拉列表。
mixed-content(混合内容：显示所有混合内容资源(mixed-content:all)或仅显示当前显示的内
(mixed-content:displayed).
         """
        print(text)
        processor = TextProcessor('input', text)
        processor.action()
        self.assertTrue(True)

    def test_action2(self):
        text = """
        什么是Base64
定义：
Base64是一种基于64个可打印字符来表示二进制数据的表示方法。由于2^6=64，所以每6个比特为一个单元，
对应某个可打印字符.3个字节(8位)有24个比特，对应于4个Base64单元，即3个字节可由4个可打印字符来表示.
它可用来作为电子邮件的传输编码。在Base64中的可打印字符包括字母A-Z、a-z、数字0-9，这样共有62个字
符，此外两个可打印符号在不同的系统中而不同。
场景
BaSe64常用于在通常处理文本数据的场合，表示、传输、存储一些二进制数据，包括MME的电子邮件及XML的
一些复杂数据。
        """

        print(text)
        processor = TextProcessor('input', text)
        processor.action()
        self.assertTrue(True)
    def test_action3(self):
        text = """
解读
高级加密标准（英语：Advanced Encryption Standard,缩写：AES),在密码学中又称Rijndael加密
法，是美国联邦政府采用的一种区块加密标准。这个标准用来替代原先的DES,已经被多方分析且广
为全世界所使用。经过五年的甄选流程，高级加密标准由美国国家标准与技术研究院(NIST)于2001
年11月26日发布于F1 PS PUB197,并在2002年5月26日成为有效的标准。2006年，高级加密标准已
然成为对称密钥加密中最流行的算法之一。
该算法为比利时密码学家Joan Daemen和Vincent Rijmen.所设计，结合两位作者的名字，以Rijndael为
名投稿高级加密标准的甄选流程。(Riindaeli的发音近于"Rhine doll")
        """
        print(text)
        processor = TextProcessor('input', text)
        processor.action()
        self.assertTrue(True)