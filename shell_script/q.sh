#!/bin/bash
#shell中的if循环 注意：里面的必须有空格。
read name
#echo $name
if [ $name == java ]||[ $name == Java ];then
echo input correct
elif [ $name == javac ];then
echo input also correct
else
echo input no
fi

a=20
b=30
if [ $a -eq $b ];then
echo a与b是相等
elif [ $a -gt $b ];then
echo a大于b
elif [ $a -lt $b ];then
echo a小于b
else 没有符合要求的
fi
#shell中的for循环 
for loop in 1 3 5;do
echo the value is: $loop
done

for st in 'his is a string';do
echo $st
done


#shell中的while循环 
int=1
while(( $int<=5 ));do
echo $int
let int++
done

#echo -n '输入你最喜欢的电影'
#while read FILM;do
#echo 是的$FILM是一部好电影
#done

echo 输入1到10的数字，输入的是为
read aNum
case $aNum in
	1) echo 选择了1
	;;
	2) echo 选择了2
	;;
	3) echo 选择了3
	;;
	4) echo 选择了4
	;;
	*) echo 你没有输入1到10的数字
	;;
esac
