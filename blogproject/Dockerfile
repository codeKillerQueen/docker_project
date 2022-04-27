FROM python:3.8

MAINTAINER Fat Puffer <dcpuffer@outlook.com>

# 设置 python 环境变量
ENV PYTHONUNBUFFERED 1
 
# 在容器内/var/www/html/下创建blogproject文件夹
RUN mkdir -p /var/www/html/blogproject
 
# 设置容器内工作目录
WORKDIR /var/www/html/blogproject
 
# 将当前目录文件加入到容器工作目录中（. 表示当前宿主机目录）
ADD . /var/www/html/blogproject
 
# 更新pip版本/usr/local/bin/python3 -m
RUN pip3 install --upgrade pip

# 利用 pip3 安装依赖
RUN pip3 install -r requirements.txt -i https://pypi.douban.com/simple

# Windows环境下编写的start.sh每行命令结尾有多余的\r字符，需移除。
RUN sed -i 's/\r//' ./start.sh
 
# 设置start.sh文件可执行权限
RUN chmod +x ./start.sh
