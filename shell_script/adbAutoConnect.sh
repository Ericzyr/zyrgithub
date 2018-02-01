#!/bin/bash
array=(10.75.111.75
10.75.108.140
10.75.109.255
10.75.110.44
10.75.109.177
)
for((i=0;i<`echo ${#array[@]}`;i++));do
ip=${array[i]}
adb connect $ip &>/dev/null
adb connect $ip &>/dev/null
sleep 2
ipconnect=`adb connect ${ip}|awk -F'[ ]' '{print $1}'`
	if [ $ipconnect=='already' -o $ipconnect=='connected' ];then
		echo -e "${ip} connect \033[32m[ok]\033[0m"
	else
        	echo -e "\033[31m no connect IP exit\033[0m" ; exit 1
	fi
done
