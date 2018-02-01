#!/bin/bash -
echo "=======python tools/pars.py======"
echo -e
echo "1) 938平台"
echo -e
echo "2) 648平台"
echo -e
echo -e "\033[31m3)退出平台\033[0m"
echo -e "\n"
read -p "请选择你测试的平台的文件:" Num
case $Num in
1) 	echo "you choice is 938 CIBN"
	echo 'path=/home/pc7/TV_Stress/TV_938'
	cd /home/adminpc/TV_Stress/938_TV
	ls -l|grep ^dr|awk -F' ' '{print $8"\t"$9}'|cat -n
	num1=`ls -l|grep ^dr|awk -F' ' '{print $8"\t"$9}'|cat -n|wc -l`
	read -p "input up choice test file:" num
	[ $num -gt $num1 ]&& echo "input number is error exit $0" && exit 1
	cd /home/adminpc/TV_Stress/938_TV
	file=`ls -l|grep ^dr|awk -F' ' '{print $9}'|cat -n|sed -n $num'p'|awk -F' ' '{print $2}'`
	echo $file
	cd /home/adminpc/TV_Stress/938_TV
	`python tools/parse.py $file/`
	cd /home/adminpc/TV_Stress/938_TV/$file/
	pat=`ls -t|cat -n|grep .html$|awk -F' ' '{print $2}'|head -1`
	xdg-open $pat

	cd /home/adminpc/TV_Stress/938_TV

	#file:///home/adminpc/TV_Stress/938_TV/file/pat
	echo `date +%Y-%d-%m`'---result---'
	#xdg-open $file &>/dev/null
	echo `date +%Y-%d-%m`'---result---'
	echo "============================"
	cd 
	pathhtml='file:///home/adminpc/TV_Stress/938_TV/'$file/$pat

	python3 web16.py $pathhtml
	;;
2) echo echo "you choice is 648 CIBN"
echo "you choice is 648 CIBN"
	echo 'path=/home/adminpc/TV_Stress/648_TV'
	cd /home/adminpc/TV_Stress/648_TV
	ls -l|grep ^dr|awk -F' ' '{print $8"\t"$9}'|cat -n
	num1=`ls -l|grep ^dr|awk -F' ' '{print $8"\t"$9}'|cat -n|wc -l`
	read -p "input up choice test file:" num
	[ $num -gt $num1 ]&& echo "input number is error exit $0" && exit 1
	cd /home/adminpc/TV_Stress/648_TV
	file=`ls -l|grep ^dr|awk -F' ' '{print $9}'|cat -n|sed -n $num'p'|awk -F' ' '{print $2}'`
	echo $file
	cd /home/adminpc/TV_Stress/648_TV
	`python tools/parse.py $file/`
	cd /home/adminpc/TV_Stress/648_TV/$file/
	pat=`ls -t|cat -n|grep .html$|awk -F' ' '{print $2}'|head -1`
	xdg-open $pat
	
	cd /home/adminpc/TV_Stress/648_TV
	#xdg-open $file &>/dev/null
	
	echo "============================"
	cd 
	pathhtml='file:///home/adminpc/TV_Stress/648_TV/'$file/$pat

	python3 web16.py $pathhtml
	;;
3)echo 'you choice exit';exit
	;;
*) echo "你选择错误退出";exit 1
esac
