from bs4 import BeautifulSoup
import requests
import os

# 读取HTML文件内容
file_path = 'templates/origin.html'
with open(file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# 创建一个BeautifulSoup对象来解析HTML
soup = BeautifulSoup(html_content, 'html.parser')

# 获取所有的图片标签
images = soup.find_all('img')

# 遍历每个图片标签并下载图片
for img in images:
    img_url = img.get('src')  # 获取图片链接

    # 发送 GET 请求获取图片内容
    response = requests.get(img_url)

    # 检查响应状态码
    if response.status_code == 200:
        # 保存图片到本地
        filename = os.path.basename(img_url)  # 获取图片链接中的文件名作为本地文件名
        filename_download = os.path.join('static', filename)
        with open(filename_download, "wb") as file:
            file.write(response.content)
        print(f"图片 {img_url} 已成功下载到本地")

        # 替换原始图片链接为本地图片路径
        img['src'] = 'static/' + filename
    else:
        print(f"下载失败，图片 {img_url}，状态码:", response.status_code)

# 输出替换后的HTML代码
with open('templates/t2.html', 'w', encoding='utf-8') as file:
    file.write(soup.prettify())

print("处理后的 HTML 内容已保存到 t2.html 文件")
