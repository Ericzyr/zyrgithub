#!/bin/bash -
for ((i=0;i<10;i++));do
	if [ $i -ge 3 ];then echo "超出输入的次数";break;fi
	read -p "输入你的usr：" name
	read -p "输入你的password：" age
	oname=eric
	oage=21
	if [ "$name" == "$oname" -a $age == $oage ];then
	echo "ok";break
	else
	echo '输入不正确'$(($i+1))'次请重新输入'
	echo -e
	fi
done

