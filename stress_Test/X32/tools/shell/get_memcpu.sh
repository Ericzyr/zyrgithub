#!/system/bin/sh

#检测su
check_su=`ls /system/xbin/|busybox grep -c -w su`
if [ $check_su -eq 0 ];then
	su=""
else
	su="su -k"
fi

if [ $# -ne 2 ];then
    echo "No avg!!!"
    exit
fi

if [ -a $EXTERNAL_STORAGE/Pss_Cpu/State.txt ];then
	pid=`busybox awk -F "," '{print $1}' $EXTERNAL_STORAGE/Pss_Cpu/State.txt`
	name=`ps $((pid))|busybox awk 'END{print $9}'`
	if [ $name"a" == "sha" ];then
		kill $((pid))
		echo "Killed the running script."
	fi
fi

#结果保存文件夹根据需求调整
testresult="$EXTERNAL_STORAGE/Pss_Cpu"
if [ ! -d $testresult ];then
	mkdir $testresult
else
    rm -r $testresult
	mkdir $testresult
fi

echo "$$,0,0,0,0,0" >$testresult/State.txt

#系统时间+16输出当前时间，输出$day——日期;$time——时间;$time_name——用于文件名时间戳。
#用法
#date_now
#直接使用输出变量
date_now(){
local y=`date +%Y|busybox sed 's/^0*//'`
local m=`date +%m|busybox sed 's/^0*//'`
local d=`date +%d|busybox sed 's/^0*//'`
local h=$((`date +%H|busybox sed 's/^0*//'`+16))
if [ $h -ge 24 ];then
	local h=$((h-24))
	#日期+1
	case $m in
		1|3|5|7|8|10|12)
				local l=31
		;;
		4|6|9|11)
				local l=30
		;;
		2)
				if [ $(($y%4)) = 0 ];then
					local l=29
				else
					local l=28
				fi
		;;
	esac
	if [ $((d+1)) -gt $l ];then
		local day=1
		if [ $m -eq 12 ];then
			local m=1
			local y=$((y+1))
		else
			local m=$((m+1))
		fi
	else
		local d=$((d+1))
	fi
fi
day=$y"/"$m"/"$d
if [ $m -lt 10 ];then
		local m="0"$m
fi
if [ $d -lt 10 ];then
		local d="0"$d
fi
if [ $h -lt 10 ];then
		local h="0"$h
fi
time="$h:`date +%M:%S`"
time_name="$m$d"-"$h`date +%M%S`"
}

#需要一个参数，second：第一列序列时间
get_meminfo(){
date_now
fg=`$su dumpsys activity|grep "Recent #0"|busybox awk '{print $7}'|busybox tr -d "}"`
tmp=`procrank`
local a=1
while [ $a -ne 0 ];do
	local w=`echo "$tmp"|grep -c "warning"`
	if [ $w -ne 0 ];then
		local w_pid=`echo "$tmp"|grep "warning"|busybox awk '{print $7";"}'`
		local w_pid=`echo $w_pid`
		date_now
		fg=`$su dumpsys activity|grep "Recent #0"|busybox awk '{print $7}'|busybox tr -d "}"`
		tmp=`procrank`
		local a=$((a+1))
		echo "$day $time procrank获取结果中有warning(进程：$w_pid时间点：$1;当前前台进程：$fg)" >>$testresult/procrank_error.log
		if [ $a -eq 3 ];then
			echo "$day $time 重试3次仍旧存在warning，停止重试)" >>$testresult/procrank_error.log
			local a=0
		fi
	else
		local a=0
	fi
done
if [ ! -a $testresult/procrank.csv ];then
	echo "Second,PID,Pss,cmdline,Process_state" >$testresult/procrank.csv
fi
if [ ! -a $testresult/freemem.csv ];then
	echo "Second,Time,free,buffers,cached,freemem" >$testresult/freemem.csv
fi
echo "$tmp"|busybox awk -v s=$1 -v t="$day $time" -v f=$fg -v csv1="$testresult/procrank.csv" -v csv2="$testresult/freemem.csv" -v txt="$testresult/cmdline.txt" '{if(NF==6&&$1!="PID"){l=l+1;if(l<6){print $6>>txt};if($6==f){c="fp"}else{c="bp"};print s","$1","substr($4,1,length($4)-1)","$6","c >>csv1}else{if(NF==13){print s","t","substr($4,1,length($4)-1)","substr($6,1,length($6)-1)","substr($8,1,length($8)-1)","substr($4,1,length($4)-1)+substr($6,1,length($6)-1)+substr($8,1,length($8)-1)+0 >>csv2}}}' 
local txt=`cat $testresult/cmdline.txt|busybox sort|busybox uniq`
echo "$txt" >$testresult/cmdline.txt
}

#需要一个参数，second：第一列序列时间
get_cpuinfo(){
if [ ! -a $testresult/cpu.csv ];then
	echo "Second,User,System,IOW,IRQ" >$testresult/cpu.csv
fi
if [ ! -a $testresult/top.csv ];then
	echo "Second,PID,CPU%,cmdline" >$testresult/top.csv
fi
top -m 5 -n 1|busybox awk -v s=$1 -v csv1="$testresult/cpu.csv" -v csv2="$testresult/top.csv" -v txt="$testresult/name.txt" '{if(NF==8){print s","$2$4$6$8 >>csv1}else{if(NF!=0&&NF!=22&&$1!="PID"){print s","$1","$3","$NF >>csv2;print $NF >>txt}}}'
local txt=`cat $testresult/name.txt|busybox sort|busybox uniq`
echo "$txt" >$testresult/name.txt
}

a=0
date_now
monitor_start_time="$day $time"
start_s=`date +%s`
while [ a -lt $2 ];do
	start_second=`date +%s`
	Second=$(($1*$a))
	date_now
	get_meminfo $Second
	get_cpuinfo $Second
	end_second=`date +%s`
	use_second=$((end_second-start_second))
	if [ $use_second -lt $1 ];then
		sleep $(($1-use_second))
	fi
	a=$((a+1))
	echo "$$,$monitor_start_time,$start_s,$1,$a/$2,$end_second" >$testresult/State.txt
done
