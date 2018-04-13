

-- 一、 启动方式
-- 1、使用 service 启动：service mysql start
-- 2、使用 mysqld 脚本启动：/etc/inint.d/mysql start
-- 3、使用 safe_mysqld 启动：safe_mysql&
-- 二、停止
-- 1、使用 service 启动：service mysql stop
-- 2、使用 mysqld 脚本启动：/etc/inint.d/mysql stop
-- 3、mysqladmin shutdown
-- 三、重启
-- 1、使用 service 启动：service mysql restart
-- 2、使用 mysqld 脚本启动：/etc/inint.d/mysql restart

-- 新建一下表格
--  create table命令格式：create table <表名> (<字段名1> <类型1> [,..<字段名n> <类型n>]);
-- create table 表名(
--     > id int(4) not null primary key auto_increment,  设置主键名 id
--     > name varchar(20) not null,
--     > sex int(4) not null default '0',
--     > degree double(16,2)); double 又精度 小数点后有两位数 00.00
--         

-- //重命名列
-- alter table 表名 change a b integer;   某列名a 改为 b
-- select * from cmdb_*;
use pydata;
show tables;
-- 把表格转换中UTF8的格式
-- alter table cmdb_userinfo CONVERT TO CHARACTER SET utf8; 
insert into cmdb_userinfo (`user`, `pwd`) VALUES ('张三', 'admin');
-- 
-- delete from cmdb_userinfo where id >64;
-- delete from cmdb_userinfo where id =64;
select * from cmdb_userinfo;
