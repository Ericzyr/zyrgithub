#!/system/bin/sh

check_su=`ls /system/xbin/|busybox grep -c -w su`
if [ $check_su -eq 0 ];then
	su=""
else
	su="su -k"
fi

date_now(){
local y=`date +%Y`
local m=$((`date +%m`))
local d=$((`date +%d`))
local h=$((`date +%H`+16))
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
		local d=1
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
if [ $m -lt 10 ];then
		local m="0"$m
fi
if [ $d -lt 10 ];then
		local d="0"$d
fi
if [ $h -lt 10 ];then
		local h="0"$h
fi
day=$y"/"$((m))"/"$((d))
time="$h:`date +%M:%S`"
time_name="$m$d"-"$h`date +%M%S`"
}

launch(){
case $1 in
#upgrade
    upgrade)
		su -k pm clear com.letv.systemupgrade
		su -k am start com.letv.systemupgrade/.SystemUpgradeActivity
	;;
esac
}

press(){
case $1 in
#UP
	UP)
        	`$su input keyevent 19`
	;;
#DOWN
	DOWN)
        	`$su input keyevent 20`
	;;
#LEFT
	LEFT)
        	`$su input keyevent 21`
	;;
#RIGHT
	RIGHT)
            `$su input keyevent 22`
	;;
#OK
	OK)
            `$su input keyevent 23`
	;;
#BACK
	BACK)
        	`$su input keyevent 4`
	;;
#HOME
	HOME)
        	`$su input keyevent 3`
	;;
esac
}

xml="/data/local/tmp/check.xml"
dump(){
local a=0
while [ $a -ne 1 ];do
	`$su uiautomator dump $xml`
	if [ -a $xml ];then
		local a=1
	else
		local a=0
	fi
done
}

##daily build升级#################################################################
date_now
testresult="$EXTERNAL_STORAGE/testresult"
if [ ! -d $testresult ];then
	mkdir $testresult
else
    rm -r $testresult
	mkdir $testresult
fi
if [ -a $testresult/tv_reboot ];then
	rm $testresult/tv_reboot
fi

anr=0
fatal=0
fingerprint=0
local_mac=`cat /sys/class/net/eth0/address|busybox tr -d ':'`
system=`getprop | busybox grep ro.letv.release.version|busybox awk -F "[" '{print $3}'|busybox tr -d ']'`
r_date=`getprop | busybox grep ro.letv.release.date|busybox awk -F "[" '{print $3}'|busybox tr -d ']'`

c_log(){
logcat -c
logcat -v time >$EXTERNAL_STORAGE/check_error.log &
check_error=$!
}
output_error(){
if [ -a $1 ];then
    local times1=`busybox grep -c "ANR " $1`
	anr=$((anr+times1))
	local times2=`busybox grep -c "FATAL EXCEPTION" $1`
	fatal=$((fatal+times2))
	local times3=`busybox grep -c "Build fingerprint" $1`
	fingerprint=$((fingerprint+times3))
	if [ $times1 -ne 0 -o $times2 -ne 0 -o $times3 -ne 0 -o $times4 -ne 0 ];then
		date_now
	    if [ ! -d $testresult/log ];then
		    mkdir $testresult/log
		fi
	    busybox mv $1 $testresult/log/$system_$time_name.log
	else
	    rm $1
	fi
	echo -e "版本号：$system\n编译日期：$r_date\n有线mac：$local_mac\nANR次数累计：$anr\nForce close累计：$fatal\ntombstone次数累计：$fingerprint" >$testresult/message.log
fi
}

check_state(){
dump
local check=`$su busybox sed 's/ /\n/g' $xml|busybox grep -c "说出你的不满"`
local check_usb=`$su busybox sed 's/ /\n/g' $xml|busybox grep -c "新设备"`
if [ $check -ge 1 -o $check_usb -ge 1 ];then
	press RIGHT
	sleep 2
	press OK
	sleep 2
fi
rm $xml
}

comment(){
date_now
if [ -a $testresult/comments.csv ];then
	echo "$day $time,$1" >>$testresult/comments.csv
else
	echo "时间,异常备注" >$testresult/comments.csv
	echo "$day $time,$1" >>$testresult/comments.csv
fi
}

check_ok(){
local a=1
while [ $a -ne 0 ]
do
    check_state
	press OK
	sleep 1
	dump
    local check=`$su busybox sed 's/ /\n/g' $xml`
	local check_update=`echo "$check"|busybox grep "文件失败"`
    if [ -n "$check_update" ];then
		comment "系统升级包检查失败"
        press OK
	else
		local message=`echo "$check"|busybox grep "升级测试"`
		if [ -n "$message" ];then
			local a=0
		else
			local message1=`echo "$check"|busybox grep "S版本升级"`
			if [ -n "$message1" ];then
				press BACK
				sleep 2
				press DOWN
				local a=1
				local a=$((a+1))
			else
				launch upgrade
				sleep 5
				press DOWN
				local a=$((a+1))
			fi
		fi
	fi
	if  [ $a -eq 10 ];then
		local a=1
		kill $check_error
		output_error $EXTERNAL_STORAGE/check_error.log
		c_log
	fi
	rm $xml
done
}

#检测下载失败及button状态
check_button_state(){
local a=1
while [ $a -ne 0 ]
do
	sleep 2
	dump
    local check=`$su busybox sed 's/ /\n/g' $xml`
	local package=`echo "$check"|busybox grep -c "com.letv.systemupgrade"`
	if [ $package -eq 0 ];then
		restart=0
	    local a=0
	else
		local button_state0=`echo "$check"|busybox grep -c "$1（"`
		if [ $button_state0 -eq 0 ];then
		    restart=0
	        local a=0
		else
			local button_state1=`echo "$check"|busybox grep -c "取消下载更新包"`
			if [ $button_state1 -ge 1 ];then
				local a=$((a+1))
			else
				local download=`echo "$check"|busybox grep -c "系统升级包下载失败"`
				if [ $download -ge 1 ];then
					comment "系统升级包下载失败"
					sleep 2
					press OK
					sleep 2
					check_ok $1
					sleep 2
					press OK
					local a=$((a+1))
				else
					local button_state=`echo "$check"|busybox grep -c "重启更新"`
					if [ $button_state -ge 1 ];then
						restart=1
						local a=0
					fi
				fi
			fi
		fi
	fi
	rm $xml
done
}

#检测确定后是否正常重启，未重启等待。
check_reboot(){
start_second=`date +%s`
local a=1
while [ $a -ne 0 ]
do
    sleep 2
	dump
    local check=`$su busybox sed 's/ /\n/g' $xml`
	local button_state=`echo "$check"|busybox grep "文件非法"`
	if [ -n "$button_state" ];then
	    comment "校验文件非法"
		sleep 2
		press HOME
		local a=0
	else
		local checking=`echo "$check"|busybox grep -c "正在校验"`
		if [ $checking -ge 1 ];then
			local a=$((a+1))
		fi
	fi
	end_second=`date +%s`
	use_second=$((end_second-start_second))
	if [ $use_second -ge 180 ];then
		comment "确定重启后3分钟仍未重启"
		local a=0
	fi
	rm $xml
done
}

#开始升级
echo "$$" >$testresult/start.txt
if [ -a $xml ];then
	rm $xml
fi
c=1
while [ $c -ne 0 ]
do
	c_log
	check_state
	launch upgrade
    sleep 1
	dump
    upgrade=`$su busybox sed 's/ /\n/g' $xml|busybox grep "$2"`
	rm $xml
    if [ -n "$upgrade" ];then
		sleep 3
		check_state
	    press DOWN
		check_state
		check_ok $2
        check_state
        press OK
		check_state
		sleep 5
		check_button_state $2
		if [ $restart -eq 1 ];then
		    check_state
			date_now
			rm $testresult/start.txt
			kill $check_error
			output_error $EXTERNAL_STORAGE/check_error.log
			c_log
	        press OK
	        check_reboot
		fi
	fi
	kill $check_error
	output_error $EXTERNAL_STORAGE/check_error.log
	c=1
	c=$((c+1))
done
