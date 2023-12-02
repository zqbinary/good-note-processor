# 介绍

我的笔记工具是印象笔记，这几年想拷贝的内容真的越来越难了。写一个处理工具，用来加强复制。

# 功能

## ocr识别再处理

ocr识别结果，且不说准确性，换行总是处理不好，如果选择取出换行，就会误伤一些，如果不去掉换行，又看了难受。所以想了一个方案，算出行的字数，在这个字数左右的行就去掉换行符号。

使用： 我使用的是utools, 截图ocr并复制，接下来是py的事。py监听快捷键 alt+b,监听到，就取出处理再放入剪贴板。

## 网页图片，内容，格式处理

前端是chrome扩展插件，将选中的html 发送给请求 post localhost:7826/html 给后端flask 处理，flask 将图片下载下来，补充格式化html，浏览器
get localhost:7826/out,就可以看到结果，该结果图片已经下到本地可以自由复制

适配列表：

| 网站   | 域名               | 例子                                                                                                                                                                   | 
|------|------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 博客园  | cnblogs.com      | [https://www.cnblogs.com/acm-bingzi/p/svg.html](https://www.cnblogs.com/acm-bingzi/p/svg.html)                                                                       |
| CSDN | blog.csdn.net    | [https://blog.csdn.net/csdnnews/article/details/134566191?spm=1000.2115.3001.5926](https://blog.csdn.net/csdnnews/article/details/134566191?spm=1000.2115.3001.5926) |
| 思否   | segmentfault.com | https://segmentfault.com/a/1190000044421775                                                                                                                          |
| 掘金   | juejin.cn        | https://juejin.cn/post/6909379124679311368                                                                                                                           |
其他
* 腾讯云 https://cloud.tencent.com/developer/article/2219258
# 计划

* 一键识别主体内容发送
* 单元测试，保证ocr格式，各个demo正确
* 单元测试，保证图片识别，各个demo正确
* 定期去掉图片
* ？写个引擎，不同网站不同规则
* 处理md
* 无头浏览器或者其他方案一键复制
* 直接生成印象笔记，我特有的笔记模板的样子
* 代码格式化