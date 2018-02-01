#!/bin/bash
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
if [ $aNum -eq 1 ];then
  echo ok is correct
elif [ $aNum -eq 2 ];then
  echo ok is correct2
fi
