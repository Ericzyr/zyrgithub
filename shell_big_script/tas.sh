#!/bin/bash -

array=(10.75.111.75
10.75.108.140)
# 10.75.109.255 10.75.110.44 10.75.109.177
#)
for((i=0;i<`echo ${#array[@]}`;i++));do
ip=${array[i]}
adb connect $ip >/dev/null 2>&1
sleep 2
ipconnect=`adb connect $ip|awk -F'[ ]' '{print $1}'` &>/dev/null
echo $ipconnect is nm

done
