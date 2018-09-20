#!/bin/bash
USER_HOME=$(eval echo ~${SUDO_USER})
apk="$USER_HOME/manifest/apk"
sh="$USER_HOME/manifest/sh"
py="$USER_HOME/manifest/py"
IPADDRESS=$1
BUILD_ID=$2
echo ${IPADDRESS}
#check avgs
if [ $# -eq 4 -o $# -eq 5 ];then
	case `echo $1|awk -F. '{print NF}'` in
		#usb connect
		1)
			IPADDRESS=$1
		;;
		#net connect
		4)
			IPADDRESS=$1":5555"
		;;
		#error device
		*)
			echo "$1 is wrong device!!!"
			exit
		;;
	esac
	type=`echo $3|awk -F_ '{if(NF==2){print $2}else{print $0}}'`
	jar="$USER_HOME/manifest/jar/$2/$type.jar"
	if [ ! -f $jar ];then
		echo "No $jar!!! exit!!!"
		exit
	fi
	caselist="$USER_HOME/manifest/caseList/$2/$3/caselist.txt"
	deviceConfig="$USER_HOME/manifest/caseList/$2/$3"
	if [ ! -f $caselist ];then
		echo "No $caselist!!! exit!!!"
		exit
	fi
	case $# in
		4)
			m_avg=15
		;;
		5)
			m_avg=$5
		;;
	esac
else
	echo "Avgs is $#, it should be device project type BUILD_ID"
	echo "device: IP or devices name"
	echo "project: S250;X60;S240"
	echo "type: smoke;stability;CIBN_stability;CIBN_smoke; HK_smoke"
	echo "BUILD_ID: Jenkins job id"
	echo "m_avg: The defaut is 15, or set it at the fifth avg"
	exit
fi

#download apk if not exist
if [ ! -f $apk/qq.apk ];then
	wget http://tc.letv.leshiren.com/download_apk/?file=qq.apk --content-disposition -P $apk/
else
	echo "qq.apk already exists, no need to download"
fi
if [ ! -f $apk/weixin.apk ];then
	wget http://tc.letv.leshiren.com/download_apk/?file=weixin.apk --content-disposition -P $apk/
else
	echo "weixin.apk already exists, no need to download"
fi
if [ ! -f $apk/weibo.apk ];then
	wget http://tc.letv.leshiren.com/download_apk/?file=weibo.apk --content-disposition -P $apk/
else
	echo "weibo.apk already exists, no need to download"
fi
#connect device before run case
reconnect()
{
adb disconnect ${IPADDRESS}
local a=0
while true;do
	sleep 5
    case `adb -s ${IPADDRESS} shell ls|grep -c -w data` in
        0)
		adb connect ${IPADDRESS}
		sleep 2
		adb -s ${IPADDRESS} root
		sleep 5
        ;;
        1)
            echo "reconnect $a times, connected!!! continue!!!"
            break
        ;;
        *)
            echo "date:"`adb -s ${IPADDRESS} shell ls|grep -c -w data`
        ;;
    esac
    local a=$((a+1))
    if [ $a -eq $1 ];then
        echo "reconnect $1 times, failed!!! exit!!!"
		adb -s ${IPADDRESS} wait-for-devices
        #exit
    fi
done
}
# check uiautomator process exist or not
waitUI()
{
local a=0
while true;do
sleep 5
case `adb -s ${IPADDRESS} shell ls|grep -c -w data` in
        0)
		adb connect ${IPADDRESS}
		sleep 2
		adb -s ${IPADDRESS} root
		sleep 5
        ;;
        1)
            if [ `adb -s ${IPADDRESS} shell ps | grep -c uiautomator` -eq 0 ];then
                echo "There is no uiautomator!!! continue!!!"
                break
            else
                sleep 10
            fi
        ;;
        *)
            echo "date:"`adb -s ${IPADDRESS} shell ls|grep -c -w data`
        ;;
    esac
    local a=$((a+1))
    if [ $a -eq 10 ];then
        echo "reconnect 10 times, failed!!! exit!!!"
		adb -s ${IPADDRESS} wait-for-devices
        #exit
    fi
done
}
reconnect 5
adb -s ${IPADDRESS} root
sleep 5
reconnect 5

if [ `adb -s ${IPADDRESS} shell id|grep -c root` -eq 0 ];then
    echo "No root!!!"
    exit
fi
adb -s ${IPADDRESS} remount
adb -s ${IPADDRESS} push $jar /data/local/tmp/
adb -s ${IPADDRESS} push $sh/PullLog.sh /data/local/tmp/
adb -s ${IPADDRESS} push $sh/get_memcpu.sh /data/local/tmp/
adb -s ${IPADDRESS} push $USER_HOME/manifest/filemanager /sdcard/filemanager
adb -s ${IPADDRESS} shell chmod 0777 /data/local/tmp/PullLog.sh
adb -s ${IPADDRESS} shell chmod 0777 /data/local/tmp/get_memcpu.sh
adb -s ${IPADDRESS} shell rm -rf /sdcard/AutoSmoke_UI30/*
adb -s ${IPADDRESS} push $USER_HOME/manifest/Utf7Ime.apk /data/local/tmp
adb -s ${IPADDRESS} push $apk/qq.apk /data/local/tmp
adb -s ${IPADDRESS} push $apk/weibo.apk /data/local/tmp
adb -s ${IPADDRESS} push $apk/weixin.apk /data/local/tmp
adb -s ${IPADDRESS} shell pm install -r /data/local/tmp/Utf7Ime.apk
adb -s ${IPADDRESS} shell pm install -r /data/local/tmp/qq.apk
adb -s ${IPADDRESS} shell pm install -r /data/local/tmp/weibo.apk
adb -s ${IPADDRESS} shell pm install -r /data/local/tmp/weixin.apk
adb -s ${IPADDRESS} shell sh /data/local/tmp/get_memcpu.sh 15 1500 &
result_folder=$4/Device1
mkdir -p $result_folder
deviceType="deviceType=="`adb -s $IPADDRESS shell getprop ro.product.model`
buildVersion="buildVersion=="`adb -s $IPADDRESS shell getprop ro.letv.release.version`
buildDate="buildDate=="`adb -s $IPADDRESS shell getprop ro.letv.release.date`
testStartTime="testStartTime=="`date '+%Y-%m-%d %H:%M:%S'`
testEndTime="testEndTime=="`date '+%Y-%m-%d %H:%M:%S'`
echo $deviceType > $result_folder/deviceInfo.txt
echo $buildVersion >> $result_folder/deviceInfo.txt
echo $buildDate >> $result_folder/deviceInfo.txt
echo $testStartTime >> $result_folder/deviceInfo.txt
echo $testEndTime >> $result_folder/deviceInfo.txt
list=""
ci=0
globalvars=`awk -F ":" '{if(NF==2) a=a " -e " $1 " " $2 fi}END{print a}' ${deviceConfig}/device1`
for ((i=1;i<100;i++))
do
	for line in `cat $caselist`
	do
		testCase=`echo $line| awk -F "," '{print $1}'`
		case_name=`echo $line|awk -F# '{print $2}'|awk -F "," '{print $1}'`
		#case avgs
		case_avg=`echo $line|awk -F "," '{for(i=2;i<=NF;i++)a=a " -e " $i;print a}'|tr ":" " "`
		#current_case_folder='LOOP'$i/${case_name}_`date '+%Y%m%d_%H%M%S'`		
		current_case_folder=${case_name}_`date '+%Y%m%d_%H%M%S'`		
		mkdir -p $result_folder/'LOOP'$i/$current_case_folder
		#current_case_log=$result_folder/$current_case_folder/case.log
		#echo "INSTRUMENTATION_STATUS: class=$line" > $current_case_log
		adb -s ${IPADDRESS} shell busybox pkill uiautomator
		reconnect 5
		adb -s ${IPADDRESS} shell busybox mkdir -p /sdcard/AutoSmoke_UI30/$current_case_folder
		adb -s ${IPADDRESS} shell "echo INSTRUMENTATION_STATUS: class=$line > /sdcard/case.log"
		adb -s ${IPADDRESS} logcat -c &
		adb -s ${IPADDRESS} logcat -v time > $result_folder/'LOOP'$i/$current_case_folder/logcat.log &
		adb -s ${IPADDRESS} shell rm -r /sdcard/AutoSmoke_UI30/* > /dev/null
		#adb -s ${IPADDRESS} wait-for-device
		adb -s ${IPADDRESS} shell "uiautomator runtest /data/local/tmp/$type.jar -c $testCase --nohup -e disable_ime true $globalvars $case_avg -e caseFolder $current_case_folder>> sdcard/case.log"
		adb -s ${IPADDRESS} shell "cat /sdcard/case.log"
		waitUI
		#folder=autoresult_`date '+%Y%m%d_%H%M%S'`
		#tmp_folder=`adb -s ${IPADDRESS} shell ls /sdcard/AutoSmoke_UI30/ | tr -d '\r\n'`
		adb -s ${IPADDRESS} shell mv /sdcard/case.log /sdcard/AutoSmoke_UI30/$current_case_folder
		adb -s ${IPADDRESS} pull /sdcard/AutoSmoke_UI30/$current_case_folder $result_folder/'LOOP'$i/$current_case_folder
		ci=`expr $ci + 1`
		adb -s ${IPADDRESS} shell rm -rf /sdcard/AutoSmoke_UI30/*
		#mv logcat.log $result_folder/$current_case_folder
		ps aux | grep ${IPADDRESS} | grep logcat | cut -c 9-15 | xargs kill
		#echo ====================================== $line ends ======================================
		#echo ==========================================================end========================================================== >> $log.log
		testEndTime="testEndTime=="`date '+%Y-%m-%d %H:%M:%S'`
		sed -i '$d' $result_folder/deviceInfo.txt
		echo $testEndTime >> $result_folder/deviceInfo.txt
	done
done

cd $result_folder
pwd
cd ../..
pwd
echo $4
python $py/parse.py $4
#adb -s ${IPADDRESS} shell pm uninstall com.android.testing.dummyime 
#python parse.py ${IPADDRESS} $ci $result_folder
#mkdir $result_folder/Pss_Cpu
#adb -s ${IPADDRESS} pull /sdcard/Pss_Cpu $result_folder/Pss_Cpu
#pid=` awk -F "," '{print $1}' $result_folder/Pss_Cpu/State.txt`
#print $pid
#adb -s ${IPADDRESS} shell kill -9 $pid
#python formatter.py $result_folder/Pss_Cpu/procrank.csv out.csv $result_folder
#python cpuformatter.py $result_folder/Pss_Cpu/top.csv topout.csv $result_folder
#cp htmlTemplate/cpuPic.htm ${BUILD_ID}
#cp $result_folder/Pss_Cpu/cpu.csv ${BUILD_ID}
