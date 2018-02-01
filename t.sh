#!/bin/sh
echo hello word
var1=myname
echo $var1
echo get pc IP address：


#|cut -c 11-62 这也是一个获取的方法
IpAddress=`ifconfig enp4s0|grep "inet 地址"|cut -d":" -f2|cut -d" " -f1`
echo computer address: $IpAddress
echo $(adb connect ${IpAddress})
