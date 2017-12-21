#!/bin/bash -
a=(`seq 10`)
echo $a
echo ${#a[@]} #获取数组的长度;
echo ${a[2]} #获取数组下标并读取;
echo ${a[*]} #获取数组所有的;

a[1]=100 #数组的赋值;
echo ${a[*]}

unset a[1] #数组删除;
echo ${a[*]}

echo ${a[@]:0:5} #数组中分片;
echo ${a[*]}

echo ${a[@]/5/25} #数组中的替换;
