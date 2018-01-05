#!/bin/bash -
echo list TV connect IP address:
echo tv1=10.58.81.215
echo tv3=10.75.109.255
echo tv4=10.75.110.44
echo tv5=10.75.111.117
read -p 'choic tv Ip number:' ipnumber
case $ipnumber in
	1)  IP='10.75.111.75';;
	2)  IP='10.75.108.140';;
	3)  IP='10.75.109.255';;
	4)  IP='10.75.110.44';;
	5)  IP='10.75.111.117';;
esac
adb connect $IP
sleep 1
adb connect $IP
echo -e
adb devices
echo "1：选择进行电视的root权限"
echo "2：选择进行exit"
read -p 'choic tv Ip number:' inputNumber
if [ $inputNumber -eq 1 ];then
	adb -s $IP:5555 shell
elif [ $inputNumber -eq 2 ];then
	exit
else 
	echo 'you choice is error exit' `exit`
fi

