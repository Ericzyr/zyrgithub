#!/bin/bash
IPADDRESS=$1
IP=$1
BUILD_ID=$2
PRODUCT=$3
PARAMETER=$4
#check avgs
if [ $# -eq 4 ];then
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
            #exit
        ;;
    esac
    case $# in
        2)
            m_avg=15
        ;;
        3)
            m_avg=$5
        ;;
    esac
else
    echo "Avgs is $#, it should be device BUILD_ID"
    echo "device: IP or devices name"
    echo "BUILD_ID: Test result root folder"
    echo "m_avg: The defaut is 15, or set it at the fifth avg"
    #exit
fi
#connect device before run case
reconnect()
{
echo "reconnect"
echo "adb devices"
adb devices
local a=0
while true;do
	sleep 5
    case `adb -s ${IPADDRESS} shell ls|grep -c -w data` in
        0)
	echo "reconnect0"
		adb disconnect ${IP}
		adb connect ${IP}
		sleep 2
		adb -s ${IPADDRESS} root
		sleep 5
		
        ;;
        1)
	echo "reconnect1"
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
	    echo "enter 0"
	    adb disconnect ${IP}
	    echo "disconnect device"
            adb connect ${IP}
	    echo "connect device"
	    sleep 2
	    adb -s ${IPADDRESS} root
	    sleep 5
        ;;
        1)
	     echo ${IP}:5555
            if [ `adb -s ${IPADDRESS} shell ps | grep -c com.le.tcauto.uitest` -eq 0 ];then
                echo "There is no uiautomator!!! continue!!!"
                break
            else
	    echo "case is running sleep 10s"
                sleep 10
            fi
        ;;
        *)
            echo "date:"`adb -s ${IPADDRESS} shell ls|grep -c -w data`
        ;;
esac
local a=$((a+1))
echo $a
if [ $a -gt 720 ];then
echo "Kill the uiautomator by command"
adb -s ${IPADDRESS} root
PID=`adb -s ${IPADDRESS} shell ps |grep com.le.tcauto.uitest|cut -c 11-15`	
adb -s ${IPADDRESS} shell kill $PID
fi
#   if [ $a -eq 10 ];then
#	    echo "a=10"
#       echo "case is still running"
#		adb -s ${IPADDRESS} wait-for-devices
#        exit
#    fi
done
}
getTestType()
{
echo "************************************************************************************************"
echo "*                          选择乐视自动化测试类型                                          *"
echo "*                             测试类型决定测试用例                                             *"
echo "************************************************************************************************"
	echo "1 = caselist_Android.txt , 适用于Android caselist"
	echo "2 = caselist2.0_CN.txt , 适用于918/928/938/Max4-70/8096国内均可用"
	echo "3 = caselist2.0_HK.txt , 适用于TV HK UI"
	echo "4 = caselist2.0_CIBN.txt , 适用于CIBN 国广版"
	echo "5 = caselist_Android_NoCamera.txt , 适用Android caselist & Camera case removed"
	echo "6 = caselist2.0_CN_NoCamera.txt , 适用(918/928/938/Max4-70/8096国内均可用 & Camera case removed"
	echo "7 = caselist2.0_HK_NoCamera.txt , 适用于TV HK UI & Camera case removed"
	echo "8 = caselist2.0_CIBN_NoCamera.txt , 适用于CIBN 国广版 & Camera case removed"
	echo "9 = caselist2.0_India.txt , 适用于TV India UI"
	echo "10 = caselist2.0_India_NoCamera.txt , 适用于India UI & Camear case removed"
	echo "11 = caselist2.0_Russia.txt , 适用于Russia cases"
	echo "12 = caselist2.0_US.txt , 适用于US LEUI cases"
	echo "13 = caselist2.0_918HK.txt , 适用于918TV HK UI"
	echo "14 = caselist2.0_918HK_NoCamera.txt , 适用于918TV HK UI"
	echo "15 = caselist2.0_Box.txt , 适用于U4_Box_cibn"
	echo "16 = caselist2.0_BoxUS.txt , 适用于U4_Box_US"
	echo "17 = caselist2.0_BoxHK.txt , 适用于U2_Box_HK"
	
	read type
	if [ $type == "1" ];then
		caselist="caselist_Android.txt"
		area="ATV"
	elif [ $type == "2" ];then
		caselist="caselist2.0_CN.txt"
		area="CN"
	elif [ $type == "3" ];then
		caselist="caselist2.0_HK.txt"
		area="HK"
	elif [ $type == "4" ];then
		caselist="caselist2.0_CIBN.txt"
		area="CN"
	elif [ $type == "5" ];then
		caselist="caselist_Android_NoCamera.txt"
		area="ATV"
	elif [ $type == "6" ];then
		caselist="caselist2.0_CN_NoCamera.txt"
		area="CN"
	elif [ $type == "7" ];then
		caselist="caselist2.0_HK_NoCamera.txt"
		area="HK"
	elif [ $type == "8" ];then
		caselist="caselist2.0_CIBN_NoCamera.txt"
		area="CN"
	elif [ $type == "9" ];then
		caselist="caselist2.0_India.txt"
		area="India"
	elif [ $type == "10" ];then
		caselist="caselist2.0_India_NoCamera.txt"
		area="India"
	elif [ $type == "11" ];then
		caselist="caselist2.0_Russia.txt"
		area="Russia"
	elif [ $type == "12" ];then
		caselist="caselist2.0_US.txt"
		area="US"
	elif [ $type == "13" ];then
		caselist="caselist2.0_918HK.txt"
		area="HK"
	elif [ $type == "14" ];then
		caselist="caselist2.0_918HK_NoCamera.txt"
		area="HK"
	elif [ $type == "15" ];then
		caselist="caselist2.0_Box.txt"
		area="CN"
	elif [ $type == "16" ];then
		caselist="caselist2.0_BoxUS.txt"
		area="HK"
	elif [ $type == "17" ];then
		caselist="caselist2.0_BoxHK.txt"
		area="HK"
	else
	     echo "出错！没有输入正确的测试类型！"
	     sleep 50
	     exit
	fi
	if [ ! -f $caselist ];then
		echo "No $caselist!!! exit!!!"
		exit
	fi
}
AnalysisError()
{	
	reconnect 5
	#anr1=`adb -s ${IPADDRESS} shell busybox find /data/Logs/|busybox grep trace|sed '/traces.txt.bugreport/'d|wc -l`
	#tombstone1=`adb -s ${IPADDRESS} shell busybox find /data/Logs/|busybox grep tombstone_|wc -l`
	PIDSysA=`adb -s ${IPADDRESS} shell ps system_server|awk 'NR==2{print $2}'`
	dateA=`date +%s|grep -o "^[0-9].*[0-9]"`
	uptimeA=`adb -s ${IPADDRESS} shell cat /proc/uptime|awk -F. '{print $1}'`
	rebootA=`expr $dateA - $uptimeA`
	#rebootA=`adb -s ${IPADDRESS} shell getprop ro.runtime.firstboot|grep -o "^[0-9].*[0-9]"`
	if [ `adb -s ${IPADDRESS} shell busybox find /data/system/dropbox -name "*@*" -print |busybox grep -c "app_crash@"` -ne 0 ];then
		echo INSTRUMENTATION_STATUS: logstack=logstack.log >> $result_folder/'LOOP'$i/$current_case_folder/case.log
		grep "FATAL EXCEPTION" -A15 $result_folder/'LOOP'$i/$current_case_folder/logcat.log >> $result_folder/'LOOP'$i/$current_case_folder/logstack.log
		echo ==========FC occurred========== >> $result_folder/'LOOP'$i/$current_case_folder/case.log
	fi
	if [ `adb -s ${IPADDRESS} shell busybox find /data/system/dropbox -name "*@*" -print |busybox grep -c "anr@"` -ne 0 ];then
		echo INSTRUMENTATION_STATUS: logstack=logstack.log >> $result_folder/'LOOP'$i/$current_case_folder/case.log
		echo ==========ANR occurred========== >> $result_folder/'LOOP'$i/$current_case_folder/case.log
		grep "ANR in" -A15 $result_folder/'LOOP'$i/$current_case_folder/logcat.log >> $result_folder/'LOOP'$i/$current_case_folder/logstack.log
	fi
	if [ `adb -s ${IPADDRESS} shell busybox find /data/system/dropbox -name "*@*" -print |busybox grep -c "TOMBSTONE@"` -ne 0 ];then
		echo ==========Tombstone occurred========== >> $result_folder/'LOOP'$i/$current_case_folder/case.log
		echo INSTRUMENTATION_STATUS: logstack=logstack.log >> $result_folder/'LOOP'$i/$current_case_folder/case.log
		#zcat system_app_anr@1493216297341.txt.gz|grep "Build fingerprint:"
		grep "Build fingerprint:" -A10 $result_folder/'LOOP'$i/$current_case_folder/logcat.log >> $result_folder/'LOOP'$i/$current_case_folder/logstack.log
		grep "backtrace:" -A10 $result_folder/'LOOP'$i/$current_case_folder/logcat.log >> $result_folder/'LOOP'$i/$current_case_folder/logstack.log
		adb -s ${IPADDRESS} shell dumpsys dropbox --print | grep TOMBSTONE >> $result_folder/'LOOP'$i/$current_case_folder/logstack.log
	fi
	if [ `adb -s ${IPADDRESS} shell busybox find /data/system/dropbox -name "*@*" -print |busybox grep -c "native_crash@"` -ne 0 ];then
		echo ==========Tombstone occurred========== >> $result_folder/'LOOP'$i/$current_case_folder/case.log
		echo INSTRUMENTATION_STATUS: logstack=logstack.log >> $result_folder/'LOOP'$i/$current_case_folder/case.log
		grep "Build fingerprint:" -A10 $result_folder/'LOOP'$i/$current_case_folder/logcat.log >> $result_folder/'LOOP'$i/$current_case_folder/logstack.log
		grep "backtrace:" -A10 $result_folder/'LOOP'$i/$current_case_folder/logcat.log >> $result_folder/'LOOP'$i/$current_case_folder/logstack.log
		adb -s ${IPADDRESS} shell dumpsys dropbox --print | grep native_crash >> $result_folder/'LOOP'$i/$current_case_folder/logstack.log
	fi

	RebootAnalysis
	PullLog
	PIDSysB=$PIDSysA
	rebootB=$rebootA
	#anr2=`adb -s ${IPADDRESS} shell busybox find /data/Logs/|busybox grep trace|sed '/traces.txt.bugreport/'d|wc -l`
	#tombstone2=`adb -s ${IPADDRESS} shell busybox find /data/Logs/|busybox grep tombstone_|wc -l`
}


RebootAnalysis()
{
	if [ `adb -s ${IPADDRESS} shell busybox find /data/system/dropbox -name "*@*" -print |busybox grep -c "RESTART@"` -ne 0 ]; then
		echo ==========Reboot occurred========== >> $result_folder/'LOOP'$i/$current_case_folder/case.log
		echo ==========This is UI reboot========== >> $result_folder/'LOOP'$i/$current_case_folder/case.log
	fi
	if [ `adb -s ${IPADDRESS} shell busybox find /data/system/dropbox -name "*@*" -print |busybox grep -c "BOOT@"` -ne 0 ] || [ $((rebootA-rebootB)) -gt 10 ];then
		echo ==========This is System reboot========== >> $result_folder/'LOOP'$i/$current_case_folder/case.log
		echo ==========Reboot occurred========== >> $result_folder/'LOOP'$i/$current_case_folder/case.log
		if [ `adb -s ${IPADDRESS} shell busybox find /data/Logs/Log.1 -name "panic-kernel-restart.log"|busybox wc -l` -ne 0 ];then
		echo ==========Kernel Panics========== >> $result_folder/'LOOP'$i/$current_case_folder/case.log
		fi
	fi
}

PullLog()
{
	if [ `grep -c "ANR occurred" $result_folder/'LOOP'$i/$current_case_folder/case.log` -ne 0 ] || [ `grep -c "Tombstone occurred" $result_folder/'LOOP'$i/$current_case_folder/case.log` -ne 0 ] || [ `grep -c "FC occurred" $result_folder/'LOOP'$i/$current_case_folder/case.log` -ne 0 ] || [ `grep -c "Reboot occurred" $result_folder/'LOOP'$i/$current_case_folder/case.log` -ne 0 ]; then
		adb -s ${IPADDRESS} pull /data/Logs/ $result_folder/'LOOP'$i/$current_case_folder/
		grep "已停止运行" $result_folder/'LOOP'$i/$current_case_folder/logcat.log >> $result_folder/'LOOP'$i/$current_case_folder/case.log
		grep "无响应" $result_folder/'LOOP'$i/$current_case_folder/logcat.log >> $result_folder/'LOOP'$i/$current_case_folder/case.log
	fi
	adb -s ${IPADDRESS} pull /data/tombstones/ $result_folder/'LOOP'$i/$current_case_folder/
	adb -s ${IPADDRESS} pull /data/anr/ $result_folder/'LOOP'$i/$current_case_folder/
	adb -s ${IPADDRESS} pull /data/system/dropbox/ $result_folder/'LOOP'$i/$current_case_folder/dropbox
	adb -s ${IPADDRESS} shell rm -rf /data/Logs/Log.0/core_dump*
	adb -s ${IPADDRESS} shell rm -rf /data/Logs/Log.2
	adb -s ${IPADDRESS} shell rm -rf /data/system/dropbox/*
}

reconnect 5
adb -s ${IPADDRESS} root
sleep 5
reconnect 5
if [ `adb -s ${IPADDRESS} shell id|grep -c root` -eq 0 ];then
    echo "No root!!!"
    #exit
fi
string=`adb -s ${IPADDRESS} shell getprop ro.product.device`
sdk=`adb -s ${IPADDRESS} shell getprop ro.build.version.sdk|grep -o "^[0-9].*[0-9]"`
getTestType
adb -s ${IPADDRESS} remount
if [ `adb -s ${IPADDRESS} shell ls /sdcard/ |grep -c -w AAA` -ne 1 ];then
	adb -s ${IPADDRESS} push ./AAA /sdcard/AAA
fi
adb -s ${IPADDRESS} push shell/PullLog.sh /data/local/tmp/
adb -s ${IPADDRESS} push shell/get_memcpu.sh /data/local/tmp/
adb -s ${IPADDRESS} shell chmod 0777 /data/local/tmp/PullLog.sh
#adb -s ${IPADDRESS} shell chmod 0777 /data/local/tmp/get_memcpu.sh
adb -s ${IPADDRESS} shell rm -rf /sdcard/AutoSmoke_UI30/*
adb -s ${IPADDRESS} push Utf7Ime.apk /data/local/tmp
adb -s ${IPADDRESS} shell pm install -r /data/local/tmp/Utf7Ime.apk
adb -s ${IPADDRESS} shell ime enable com.android.testing.dummyime/.DummyIme
adb -s ${IPADDRESS} shell ime set com.android.testing.dummyime/.DummyIme
adb -s ${IPADDRESS} shell am broadcast -a android.intent.action.MEDIA_MOUNTED -d file:///mnt/sdcard/filemanager
adb -s ${IPADDRESS} shell rm -rf /data/system/dropbox/*
#adb -s ${IPADDRESS} shell sh /data/local/tmp/get_memcpu.sh 15 1500 &
result_folder=${BUILD_ID}/${PRODUCT}
mkdir -p $result_folder
buildModel="buildModel=="`adb -s $IPADDRESS shell getprop ro.product.model`
productDevice="productDevice=="`adb -s $IPADDRESS shell getprop ro.product.device`
productUitype="productUitype=="`adb -s $IPADDRESS shell getprop ro.product.uitype`
buildVersion="buildVersion=="`adb -s $IPADDRESS shell getprop ro.letv.release.version`
buildDate="buildDate=="`adb -s $IPADDRESS shell getprop ro.letv.release.date`
testStartTime="testStartTime=="`date '+%Y-%m-%d %H:%M:%S'`
testEndTime="testEndTime=="`date '+%Y-%m-%d %H:%M:%S'`
#anr2=`adb -s ${IPADDRESS} shell busybox find /data/Logs/|busybox grep trace|sed '/traces.txt.bugreport/'d|wc -l`;
#tombstone2=`adb -s ${IPADDRESS} shell busybox find /data/Logs/|busybox grep tombstone_|wc -l`;
rm -rf $result_folder/app-debug-androidTest.apk
md5B=`md5sum $result_folder/app-debug-androidTest.apk`
PIDSysB=`adb -s ${IPADDRESS} shell ps system_server|awk 'NR==2{print $2}'`
dateB=`date +%s|grep -o "^[0-9].*[0-9]"`
uptimeB=`adb -s ${IPADDRESS} shell cat /proc/uptime|awk -F. '{print $1}'`
rebootB=`expr $dateB - $uptimeB`
rebootB=`adb -s ${IPADDRESS} shell getprop ro.runtime.firstboot|grep -o "^[0-9].*[0-9]"`
echo $buildModel > $result_folder/phoneInfo.txt
echo $productDevice >> $result_folder/phoneInfo.txt
echo $productUitype >> $result_folder/phoneInfo.txt
echo $buildVersion >> $result_folder/phoneInfo.txt
echo $buildDate >> $result_folder/phoneInfo.txt
echo $testStartTime >> $result_folder/phoneInfo.txt
echo $testEndTime >> $result_folder/phoneInfo.txt
touch $2/jiraInfo.txt
buildModel="buildModel=="`adb -s $IPADDRESS shell getprop ro.product.model`
jiraVersion="jiraVersion=="
versionPath="versionPath=="
buildDescription="buildDescription=="`adb -s $IPADDRESS shell getprop ro.build.description`
buildProduct="buildProduct=="`adb -s $IPADDRESS shell getprop ro.build.product`
letvUI="letvUI=="`adb -s $IPADDRESS shell getprop ro.letv.ui`
testType="testType==16776" 
testPhase="testPhase=="

appinfo=`adb -s ${IPADDRESS} shell dumpsys package |grep -e "Package \[" -e "versionName" | sed 'N;s/\s*\n\s*/ /'`
echo -e $buildModel"\n"$jiraVersion"\n"$versionPath"\n"$buildDescription"\n"$buildProduct"\n"$letvUI"\n"$testType"\n"$testPhase"\n\n"$appinfo > $2/jiraInfo.txt
list=""
ci=0
globalvars=`awk -F ":" '{if(NF==2) a=a " -e " $1 " " $2 fi}END{print a}' ${PARAMETER}`
exittime=`date -d "168 hours" +%s|grep -o "^[0-9].*[0-9]"`
for ((i=1;i<10000;i++))
do
	for line in `cat $caselist`
	do
		testCase=`echo $line| awk -F "," '{print $1}'`
		case_name=`echo $line|awk -F# '{print $2}'|awk -F "," '{print $1}'`
		#case avgs
		case_avg=`echo $line|awk -F "," '{for(i=2;i<=NF;i++)a=a " -e " $i;print a}'|tr ":" " "`
		echo $case_avg
		current_case_folder=${case_name}_`date '+%Y%m%d_%H%M%S'`		
		mkdir -p $result_folder/'LOOP'$i/$current_case_folder
		#echo "INSTRUMENTATION_STATUS: class=$line" > $current_case_log
		reconnect 5
		echo =============================== copy MTBF code from server =============================
		#smbclient //cmsmb.letv.cn/jiralog -c "cd MTBFAPK/TVAPK/$area;prompt;lcd $result_folder;mget app-debug.apk app-debug-androidTest.apk" -N
		smbclient //10.75.109.96/jiralog -c "cd MTBFAPK/TVAPK/$area;prompt;lcd $result_folder;mget app-debug.apk app-debug-androidTest.apk" -N
		echo "area="$area
		md5A=`md5sum $result_folder/app-debug-androidTest.apk`
		if [ "$md5B" != "$md5A" ];then
			adb -s ${IPADDRESS} push $result_folder/app-debug.apk /data/local/tmp/
			adb -s ${IPADDRESS} push $result_folder/app-debug-androidTest.apk /data/local/tmp/
			adb -s ${IPADDRESS} shell pm uninstall com.le.tcauto.uitest
			adb -s ${IPADDRESS} shell pm uninstall com.le.tcauto.uitest.test
			if [ $sdk -lt 23 ];then
				echo "android sdk version less than 23 use install -r"
				adb -s ${IPADDRESS} shell pm install -r /data/local/tmp/app-debug.apk
				adb -s ${IPADDRESS} shell pm install -r /data/local/tmp/app-debug-androidTest.apk
			else
				adb -s ${IPADDRESS} shell pm install -g -r /data/local/tmp/app-debug.apk
				adb -s ${IPADDRESS} shell pm install -g -r /data/local/tmp/app-debug-androidTest.apk
			fi
		fi
		md5B=$md5A
		adb -s ${IPADDRESS} remount
		adb -s ${IPADDRESS} shell busybox mkdir -p /sdcard/AutoSmoke_UI30/$current_case_folder
		echo "PIDSysB="+$PIDSysB > $result_folder/'LOOP'$i/$current_case_folder/PID.log
		echo "rebootB="+$rebootB >> $result_folder/'LOOP'$i/$current_case_folder/PID.log
		echo "dateB="+$dateB >> $result_folder/'LOOP'$i/$current_case_folder/PID.log
		echo "uptimeB="+$uptimeB >> $result_folder/'LOOP'$i/$current_case_folder/PID.log
		adb -s ${IPADDRESS} shell "echo INSTRUMENTATION_STATUS: class=$line > /sdcard/case.log"
		adb -s ${IPADDRESS} logcat -c
		echo ====================================== $line start ======================================
		adb -s ${IPADDRESS} logcat -v time > $result_folder/'LOOP'$i/$current_case_folder/logcat.log &
		adb -s ${IPADDRESS} shell cat /proc/kmsg > $result_folder/'LOOP'$i/$current_case_folder/kernel.log &
		echo "am instrument -w -r -e class $testCase -e caseFolder $current_case_folder $globalvars ${case_avg} com.le.tcauto.uitest.test/android.support.test.runner.AndroidJUnitRunner >> /sdcard/case.log &" >$result_folder/currentCase.txt
		echo "exit" >>$result_folder/currentCase.txt
                adb -s ${IPADDRESS} shell < $result_folder/currentCase.txt &
		waitUI
		sleep 5
		reconnect
		adb -s ${IPADDRESS} shell "cat /sdcard/case.log"
		#folder=autoresult_`date '+%Y%m%d_%H%M%S'`
		#tmp_folder=`adb -s ${IPADDRESS} shell ls /sdcard/AutoSmoke_UI30/ | tr -d '\r\n'`
		adb -s ${IPADDRESS} shell mv /sdcard/case.log /sdcard/AutoSmoke_UI30/$current_case_folder
		adb -s ${IPADDRESS} pull /sdcard/AutoSmoke_UI30/$current_case_folder $result_folder/'LOOP'$i/$current_case_folder
		adb -s ${IPADDRESS} pull /sdcard/tmp.png $result_folder/'LOOP'$i/$current_case_folder
		adb -s ${IPADDRESS} shell rm -rf /sdcard/tmp.png
		echo "---------case end time is "`date "+%Y-%m-%d %H:%M:%S"`>>$result_folder/'LOOP'$i/$current_case_folder/case.log
		ci=`expr $ci + 1`
		adb -s ${IPADDRESS} shell rm -rf /sdcard/AutoSmoke_UI30/*
		#mv logcat.log $result_folder/$current_case_folder
		ps aux | grep ${IPADDRESS} | grep logcat | cut -c 9-15 | xargs kill
		ps aux | grep ${IPADDRESS} | grep /proc/kmsg | cut -c 9-15 | xargs kill
		echo ====================================== $line ends ======================================
		sleep 5
		echo ====================================Analysis Errors=====================================
		AnalysisError
		echo "PIDSysA="+$PIDSysA >> $result_folder/'LOOP'$i/$current_case_folder/PID.log
		echo "rebootA="+$rebootA >> $result_folder/'LOOP'$i/$current_case_folder/PID.log
		echo "dateA="+$dateA >> $result_folder/'LOOP'$i/$current_case_folder/PID.log
		echo "uptimeA="+$uptimeA >> $result_folder/'LOOP'$i/$current_case_folder/PID.log
		adb -s ${IPADDRESS} shell cat /proc/meminfo > $result_folder/'LOOP'$i/$current_case_folder/meminfo.log
		adb -s ${IPADDRESS} shell procrank > $result_folder/'LOOP'$i/$current_case_folder/procrank.log
		adb -s ${IPADDRESS} shell dumpsys meminfo >> $result_folder/'LOOP'$i/$current_case_folder/meminfo.log
		#adb -s ${IPADDRESS} shell dumpstate > $result_folder/'LOOP'$i/$current_case_folder/dumpstate.log
		adb -s ${IPADDRESS} shell dmesg > $result_folder/'LOOP'$i/$current_case_folder/Dmesg.log
		adb -s ${IPADDRESS} shell top -m 10 -n 2 > $result_folder/'LOOP'$i/$current_case_folder/top.log
		testEndTime="testEndTime=="`date '+%Y-%m-%d %H:%M:%S'`
		sed -i '$d' $result_folder/phoneInfo.txt
		echo $testEndTime >> $result_folder/phoneInfo.txt
	done
done
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
