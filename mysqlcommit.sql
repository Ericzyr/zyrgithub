

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


-- 
-- desc 表名 查看表的结构;
-- drop table 表名 对表的删除

-- 新建一下表格
--  create table命令格式：create table <表名> (<字段名1> <类型1> [,..<字段名n> <类型n>]);
-- create table 表名(
--     > id int(4) not null primary key auto_increment,  设置主键名 id 
--     > name varchar(20) not null,
--     > sex int(4) not null default '0',
-- sex enum('男','女') default '男'   设置默认值
--     > degree double(16,2)); double 又精度 小数点后有两位数 00.00
--    
-- insert into aa select*from bb;插入数据从别的表格中
-- 
-- select count(*) from aa; 查看一个数中有多少行;

-- mysql> create table aa(
--     -> id int,
--     -> name varchar(10),
--     -> mail varchar(15) unique); unique 不允许有重复值
-- truncate  table aa; 清空表格中的数据


-- django_migrationsstudentApp_studentsheet-- //重命名列
-- -- alter table 表名 change a b integer;   某列名a 改为 b
-- -- select * from cmdb_*;
-- select *from a2 where id>=2 and id<=5; 查找id 大于多少小于多范围
-- use pydata;
-- show tables;
-- -- 把表格转换中UTF8的格式
-- -- alter table cmdb_userinfo CONVERT TO CHARACTER SET utf8; 
-- insert into cmdb_userinfo (`user`, `pwd`) VALUES ('张三', 'admin');
-- -- 
-- -- delete from cmdb_userinfo where id >64;
-- -- delete from cmdb_userinfo where id =64;
-- select * from cmdb_userinfo;
-- use studentlogin;
-- select*from studentApp_studentsheet;
-- 
 -- id int primary key auto_increment,

-- 
-- create table cc select *from aa;  这是复制表的结构
-- create table cc like aa;   这是对表所有的结构和数据的复制 （所有）

