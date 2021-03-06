#!/bin/bash

source ~/.profile
#此脚本的前提：手机都通过线连pc，电视都通过无线连接pc
basepath=$(cd `dirname $0`; pwd)
echo ${basepath}
IPADDRESS=$1
file_name=$2

function parseParameters(){
	
	#TV or Phone
	case `echo $IPADDRESS|awk -F. '{print NF}'` in
		#usb connect(Phone)
		1)
			ISUSB=1
		;;
		#net connect(TV)
		4)
			IPADDRESS=${IPADDRESS}":5555"
			ISUSB=0
		;;
		#error device
		*)
			echo "$IPADDRESS is wrong device!!!"
			exit ${PARAMETER_MISS}
		;;
	esac
}

function checkProcess(){
	echo 'Checking if smbclient process exists...'
	while true; do
		if [ `ps -aux | grep -c smbclient` -eq 1 ];then
			echo "Smbclient process gone, next step"
			echo ""
			break
		else
			echo "Smbclient process exists, waiting"
			sleep 10
		fi
	done
}


function flash(){
	begain=`date +%s`
	waitForDeviceTimeOut 600 || exit $DEVICE_DISCONNECT
	versionBeforeFlash=`adb -s ${IPADDRESS} shell getprop ro.build.id`
	flashTV

	ota_named=`echo ${file_name} | cut -d '-' -f 4`
	echo "ota_named:"${ota_named}
	adb -s ${IPADDRESS} shell getprop ro.build.id
	phone_version=`adb -s ${IPADDRESS} shell getprop ro.build.id`
	echo "versionBeforeFlash:"${versionBeforeFlash}
	echo "phone_version:"${phone_version}
	if [ "${ota_named}"=="${phone_version}" ];
	then
	echo "device is updated successfully" 
	else
	echo "device is updated Failed"
	fi

	sleep 2
	flash_time=$((`date +%s`-$begain))
	echo "--------------------------------------------flash device done-----------------------------------------------"
	echo "--------------------------------------------time: ${flash_time}-----------------------------------------------"
	echo ""
}

function flashTV(){

        #接下来执行刷机 
	adb -s ${IPADDRESS} shell pm uninstall com.le.tcauto.uitest
	adb -s ${IPADDRESS} shell pm uninstall com.le.tcauto.uitest.test
	adb -s ${IPADDRESS} push flashapk/app-debug.apk /data/local/tmp/
	adb -s ${IPADDRESS} push flashapk/app-debug-androidTest.apk /data/local/tmp/
	adb -s ${IPADDRESS} shell pm install -r /data/local/tmp/app-debug.apk
	adb -s ${IPADDRESS} shell pm install -r /data/local/tmp/app-debug-androidTest.apk

	#更改手机语言至中文简体（利用google play市场的一个apk来实现通过shell命令切换语言）
	#adb -s ${IPADDRESS} push ~/tools/auto/apk/ADBChangeLanguage_0.52_apk-dl.com.apk /data/local/tmp
	#adb -s ${IPADDRESS} shell pm install -r /data/local/tmp/ADBChangeLanguage_0.52_apk-dl.com.apk
	#adb -s ${IPADDRESS} shell pm grant net.sanapeli.adbchangelanguage android.permission.CHANGE_CONFIGURATION
	#adb -s ${IPADDRESS} shell am start -n net.sanapeli.adbchangelanguage/.AdbChangeLanguage -e language zh-rCN

	runtime1=`adb -s ${IPADDRESS} shell cat /proc/uptime | awk '{print $1}'`
	adb -s ${IPADDRESS} shell input keyevent 4
	adb -s ${IPADDRESS} shell input keyevent 4
	adb -s ${IPADDRESS} shell "am instrument -w -r -e class com.letv.cases.leui.MtbfTest#testSystemUpgrade com.le.tcauto.uitest.test/android.support.test.runner.AndroidJUnitRunner"
	sleep 70
	
	waitDeviceEnterUpgradeMode 600
	

	waitForDeviceTimeOut 4000 || exit $OTA_PKG_ERROR 
	sleep 20
	adb -s ${IPADDRESS} shell input keyevent 4
	adb -s ${IPADDRESS} shell input keyevent 4
	adb -s ${IPADDRESS} shell "am instrument -w -r -e class com.letv.cases.leui.MtbfTest#testFactoryReset com.le.tcauto.uitest.test/android.support.test.runner.AndroidJUnitRunner"
	
	sleep 30
	adb connect ${IPADDRESS}
	


	waitForDeviceTimeOut 4000 || exit $OTA_PKG_ERROR 
	adb devices
	sleep 20
	adb connect ${IPADDRESS}
	adb devices
	adb -s ${IPADDRESS} shell pm uninstall com.le.tcauto.uitest
	adb -s ${IPADDRESS} shell pm uninstall com.le.tcauto.uitest.test
	adb -s ${IPADDRESS} push flashapk/app-debug.apk /data/local/tmp/
	adb -s ${IPADDRESS} push flashapk/app-debug-androidTest.apk /data/local/tmp/
	adb -s ${IPADDRESS} shell pm install -r /data/local/tmp/app-debug.apk
	adb -s ${IPADDRESS} shell pm install -r /data/local/tmp/app-debug-androidTest.apk

	adb -s ${IPADDRESS} shell "am instrument -w -r -e class com.letv.cases.leui.MtbfTest#testMTBFinitialize com.le.tcauto.uitest.test/android.support.test.runner.AndroidJUnitRunner"
	
}

function waitDeviceEnterUpgradeMode(){
	echo "Waitting for device enter upgrade mode..."
	start=`date +%s`

	while true;do
		if [ $((`date +%s`-$start)) -gt $1 ];then
			echo -e "\nWaitting device enter upgrade mode timeout, stop."
			exit $UPGRADE_SCRIPT_ERROR
		fi
		if [ $ISUSB -eq 0 ];then
			adb disconnect ${IPADDRESS} 2>&1>/dev/null
			sleep 1
			adb connect ${IPADDRESS} 2>&1>/dev/null
			sleep 1
		fi
		case `adb -s ${IPADDRESS} shell ls 2>&1 | grep -c -w data` in
			0)
				echo -e "\nChecked device is already in upgrade mode."
				break
			;;
			1)	
				sleep 5
			;;
			*)
				echo "reconnect function: data: "`adb -s ${IPADDRESS} shell ls|grep -c -w data`
			;;
		esac
		sleep 5
		echo -e ".\c"
	done
}


function sendToDeviceByADB(){
	local_file_path="./${file_name}"
	echo "Push $local_file_path to device..."
	#获取Ｕ盘路径
	getUsbPath=`adb -s ${IPADDRESS} shell "mount|grep /dev/block/vold/"`
	usbPath=`echo ${getUsbPath}|awk -F ' ' '{print $2}'`
	sendtopath="${usbPath}/update.zip"
	#清空Ｕ盘释放空间
	#echo "清空Ｕ盘,释放空间"
	#adb -s ${IPADDRESS}　shell rm -r ${usbPath}
	#电视升级包需要发送到U盘
	echo "电视升级包，发送到U盘"
	echo "adb -s ${IPADDRESS} push $local_file_path ${sendtopath} 2>&1>/dev/null"
	adb -s ${IPADDRESS} push $local_file_path ${sendtopath} 2>&1>/dev/null
	sleep 2
}


function sendToDevice(){
	begin=`date +%s`
	waitForDeviceTimeOut 600 || exit $DEVICE_DISCONNECT
	sendToDeviceByADB
	sendToDevice_time=$((`date +%s`-$begin))
	echo "--------------------------------------------send package to device done-----------------------------------------------"
	echo "--------------------------------------------time: ${sendToDevice_time}-----------------------------------------------"
	echo ""
}

function waitForDeviceTimeOut(){
	echo "Waitting for device..."
	start=`date +%s`
	adb disconnect ${IPADDRESS} 2>&1>/dev/null
	#usb connect
	while true;do
		if [ $((`date +%s`-$start)) -gt $1 ];then
			echo "Wait for device timeout, stop."
			return 1
		fi
		case `adb -s ${IPADDRESS} shell ls 2>&1 | grep -c -w data` in
			0)
				adb connect ${IPADDRESS} 2>&1>/dev/null
				sleep 5
			;;
			1)	
				adb -s ${IPADDRESS} root
				sleep 2
				adb connect ${IPADDRESS}
				echo "Device is connected!!! continue!!!"
				return 0
			;;
			*)
				echo "reconnect function: data: "`adb -s ${IPADDRESS} shell ls|grep -c -w data`
			;;
		esac
		sleep 5
		echo -e ".\c"
	done
}
parseParameters
sendToDevice
flash
function pause(){
        read -n 1 -p "$*" INP
}
pause '检查电视升级是否完成，完成请按任意键继续 ～'

