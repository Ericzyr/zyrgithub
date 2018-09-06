

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


-- 在命令打 mysql -u root -p
-- 用户 root 密码 new_pass

1、查看当前的数据库：show databases; 

创建数据库：create database + gohome;
删除数据库  drop database + RUNOOB;

2、使用use + 数据库名; 
3、显示当前数据库的表单：show tables; 结构
　　(1)show tables from book;　查看一个database 有几个sheet;
  (2)show tables;　查看一个database 有几个sheet;
4 desc + 表名; 查看表的结构;
4 drop table + 表名; 对表的删除

-- 新建一下表格
--  create table命令格式：create table <表名> (<字段名1> <类型1> [,..<字段名n> <类型n>]);
-- create table 表名(
--     > id int(4) not null primary key auto_increment,  设置主键名 id 
--     > name varchar(20) not null,
--     > sex int(4) not null default '0',
-- sex enum('男','女') default '男'   设置默认值
--     > degree double(16,2)); double 又精度 小数点后有两位数 00.00
--    
-- 
-- 


alter table readerinfo addd email varchar(30); 增加一个列表add
alter table readerinfo add email2 varchar(15) after tel; 指定增加那下列后；
alter table readerinfo change email2 email_bak varchar(20);更改一列名；
alter table readerinfo modify email char(2); 更改一列数据类型；
alter table readerinfo modify balance decimal(7,3) after email;把一个列表某一列放在某一列后面，排序；
alter table readerinfo  drop email_bak;删除某一列；
alter table readerinfo rename reader; 表的重新命名；
drop table t1,t2; 删除表格一个或者多个；



alter table bookinfo modify book_name varchar(22) not null; 更改一列数据类型不能为空；非空约束
alter table bookinfo modify book_name varchar(22) not null; 更改一列数据类型为空；非空约束；

 (1)book_id int(10) primary key 在创建时候设置主键；
 (2)alter table bookinfo modify book_id int primary key;　修改表中定义主键
 (3)alter table bookinfo drop primary key; 删除主键；


 (1)alter table bookinfo drop key book_name; 删除唯一性约束；
 (2)alter table bookinfo add unique(book_name); 添加唯一性约束；



(1)alter table bookinfo alter column book_name set default 'jack';在列中添加设置默认值
(2)alter table bookinfo alter column book_name drop default;在列中删除设置默认值



create table bookinfo( book_id int primary key, book_category_id int, foreign key(book_category_id) references bookcategory(category_id) );创建表中添加外键；


insert into aa select*from bb;插入数据从别的表格中
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

从表格中添加数据
-- insert into cmdb_userinfo (user, pwd) VALUES ('张三', 'admin');
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

