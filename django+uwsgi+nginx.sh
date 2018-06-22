#!/bin bash
pig=`netstat -tunlp|grep :8000|awk -F'[ :]+' '{print $9}'|sed 's/\/python.*//g'`
`netstat -tunlp|grep :8000|kill $pig` 2>&1>/dev/null

#ps -ef | grep nginx

#netstat -tunlp|grep :80



#测试一个项目启动uwsgi
uwsgi --http :8000 --wsgi-file test.py

#执行下面一定在项目目录中执行
#测试django项目下启动uwsgi
uwsgi --http 10.58.81.227:8000 --file djweb/wsgi.py --static-map=/static=static


#1、启动
uwsgi --ini uwsgi.ini
#2、停止
uwsgi --stop uwsgi.pid
#3、加载
uwsgi --reload uwsgi.pid


# 启动Nginx通过Nginx访问

# 这里有个命令configtest,Nginx配置是重启生效的，如果你修改完了，不知道对    不对又担心影响其他人可以使用它测试
/etc/init.d/nginx configtest
# 如果是生产环境的话Nginx正在运行，就不要直接stop start 或者 restart  直接reload就行了
#1、启动
/etc/init.d/nginx start

#2、停止
/etc/init.d/nginx stop

#3、重启
/etc/init.d/nginx restart

# 对线上影响最低 加载
/etc/init.d/nginx reload


[uwsgi]
# 项目目录
chdir=/myjack/djweb/
# 启动uwsgi的用户名和用户组
uid=root
gid=root
# 指定项目的application
module=djweb.wsgi:application
# 指定sock的文件路径       
socket=/myjack/script/uwsgi.sock
# 启用主进程
master=true
# 进程个数       
workers=5
pidfile=/myjack/script/uwsgi.pid
# 自动移除unix Socket和pid文件当服务停止的时候
vacuum=true
# 序列化接受的内容，如果可能的话
thunder-lock=true
# 启用线程
enable-threads=true
# 设置自中断时间
harakiri=30
# 设置缓冲
post-buffering=1028
# 指定IP端口       
#http=10.58.81.227:8080
# 指定静态文件
static-map=/static=/myjack/djweb/static
# 设置日志目录
daemonize=/myjack/script/uwsgi.log





server {
        listen 8099 default_server;
        listen [::]:8099 default_server;


        root /usr/share/nginx/html;

        index index.html index.htm index.nginx-debian.html;

        server_name 10.58.81.227;
        location / {
                include uwsgi_params;
                uwsgi_connect_timeout 30;
                uwsgi_pass unix:/myjack/script/uwsgi.sock;
        }
        location /static/ {
                alias /myjack/djweb/static/;
                index index.html index.htm;
        }
}



就跟踪日志
tailf /var/log/nginx/access.log
