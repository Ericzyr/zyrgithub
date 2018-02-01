#!/bin/bash -
cd /home/pc7/TV_Stress/TV_938
ls -l|grep ^dr|awk -F' ' '{print $8"\t"$9}'|sort|cat -n
num1=`ls -l|grep ^dr|awk -F' ' '{print $8"\t"$9}'|cat -n|wc -l`
echo $num1
read -p "input test file:" num

