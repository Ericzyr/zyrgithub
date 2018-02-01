#!/bin/bash


t="/mnt/app"
cd $t;ls|cat -n
#ls|cat -n
for i in `seq 10`;do
echo "请选择文件:num; 0:reset"
echo "==============================="
read -p "选择文件:" num
cd `pwd`'/'`ls|cat -n|awk -F' ' '{print$2}'|sed -n $num'p'`'/'
ls|cat -n

if [ $num -eq 0 ];then
echo "==============================="
echo "重新选择文件"
	cd `pwd`
	cd ..
	ls|cat -n
fi

done

