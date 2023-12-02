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
