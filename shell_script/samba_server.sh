https://jingyan.baidu.com/article/db55b609e041584ba30a2f01.html
https://blog.csdn.net/qiangwei1212/article/details/68923558



1、安装samba ：一共有两个应用

安装samba：sudo apt-get install samba
安装smbclient：sudo apt-get install smbclient
  

3. 重启samba服务：

sudo service restart smbd

sudo service restart nmbd


2、修改samba 的配置文件

打开配置文件：vim /etc/samba/smb.conf



在文件后面加下面一段话
在home下新建一下文件share 并设置权限 chmod + 777
[share]
comment = Share Folder require password
browseable = yes
path = /home/share
create mask = 0777
directory mask = 0777
valid users = share
force user = nobody
force group = nogroup
public = yes
writable = yes
available = yes

