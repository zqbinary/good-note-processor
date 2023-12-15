# 介绍
我的笔记工具是印象笔记，这几年想拷贝的内容真的越来越难了。写一个处理工具，用来加强复制。

## 网页图片，内容，格式处理

前端是chrome扩展插件，将选中的html 发送给请求给后端flask 处理  
flask 将图片下载下来，补充格式化html，做一些格式化工作  
localhost:7826/out，就可以看到结果

适配列表：

| 网站   | 域名               | 例子                                                                                                                                                                   | 
|------|------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 博客园  | cnblogs.com      | [https://www.cnblogs.com/acm-bingzi/p/svg.html](https://www.cnblogs.com/acm-bingzi/p/svg.html)                                                                       |
| CSDN | blog.csdn.net    | [https://blog.csdn.net/csdnnews/article/details/134566191?spm=1000.2115.3001.5926](https://blog.csdn.net/csdnnews/article/details/134566191?spm=1000.2115.3001.5926) |
| 思否   | segmentfault.com | https://segmentfault.com/a/1190000044421775                                                                                                                          |
| 掘金   | juejin.cn        | https://juejin.cn/post/6909379124679311368                                                                                                                           |
## 适配问题
https://juejin.cn/post/7294441582983954468  python复制代码

## 支持不同的code preview

| repository    | keyword     | example                                                 |
|---------------|-------------|---------------------------------------------------------|
| hightlight.js | hljs        | https://blog.51cto.com/u_16160587/8658288               |
| prism         | prism-token | 腾讯云 https://cloud.tencent.com/developer/article/2219258 |
其他
* 腾讯云 https://cloud.tencent.com/developer/article/2219258

# 计划

## 处理网页
- [ ] 一键识别主体内容发送
- [ ] 处理md
- [ ] 无头浏览器或者其他方案一键复制
- [ ] 直接生成印象笔记，我特有的笔记模板的样子
- [x] 代码格式化
- [ ] 代码格式化,彩色提示
- [x] 处理后 消息提醒
- [ ] 隔一段就加个br 
- [ ] 如果下一个是h,就先不分tr

