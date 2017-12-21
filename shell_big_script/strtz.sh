#!/bin/bash -
echo tv1=10.75.111.75
echo tv2=10.75.108.140
echo tv3=10.75.109.255
echo tv4=10.75.110.44
read -p 'choic tv Ip number:' ipnumber
case $ipnumber in
	1)  IP='10.75.111.75';;
	2)  IP='10.75.108.140';;
	3)  IP='10.75.109.255';;
	4)  IP='10.75.110.44';;
esac
adb connect $IP
sleep 1
adb connect $IP

