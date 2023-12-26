#使用的基础镜像
FROM python:3.11
#设置工作目录
WORKDIR /app
#复制requirements.txt
COPY requirements.txt requirements.txt
#安装依赖包
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

#复制当前目录下的内容到docker中
COPY . .
#启动命令
ENTRYPOINT [ "python", "-m" , "flask",  "--app","app.py", "run", "--host=0.0.0.0","--port=7826"]