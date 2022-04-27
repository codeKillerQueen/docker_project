 #!/bin/bash
 # 从第一行到最后一行分别表示：
 # 1. 收集静态文件到根目录，
 # 2. 生成数据库可执行文件，
 # 3. 根据数据库可执行文件来修改数据库
 # 4. 用 uwsgi启动 django 服务
 python3 manage.py collectstatic --noinput && 
 python3 manage.py makemigrations &&
 python3 manage.py migrate &&
 uwsgi --ini /var/www/html/blogproject/uwsgi.ini