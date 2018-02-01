#!/bin/bash -
cd /mnt/app/SuperTV
ls|cat -n

function file(){
	echo "文件进入路径:和 0:退出"
	read -p "进入选择的文件夹:" num
	echo " "
	if [ $num -eq 0 ];then
	echo 'exit file'
	break
	fi
	path1=`ls|cat -n|awk -F' ' '{print$2}'|sed -n $num'p'`
	if [ $path1 == *userdebug ];then
	echo 'exit file'
	pwdth=`pwd`
	break
	fi
	cd $path1;ls|cat -n|tail -10
	echo " "
}

function file1(){
	echo "文件进入路径:和 0:退出"
	read -p "进入选择的文件夹:" num
	echo " "
	if [ $num -eq 0 ];then
	echo 'exit file'
	break
	fi
	path1=`ls|cat -n|awk -F' ' '{print$2}'|sed -n $num'p'`

	cd $path1;ls|cat -n
	filepath=`pwd`
	echo " "
}

for i in `seq 10`;do
	file
done

echo '--------------------------------------------------------------'

cd $pwdth
ls|cat -n
for i in `seq 2`;do
	file1
done

echo $filepath

filname=`cd $filepath;ls -l *.zip|sort -nrk3|head -1|awk -F'[:]' '{print $2}'|awk -F'[ ]' '{print $2}'`
echo $filname




