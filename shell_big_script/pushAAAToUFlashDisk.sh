#!/bin/bash -
echo "============================================"
echo "**uploading AAAA file to TV USB flash disk**"
echo "============================================"
echo "1 number represenrtative tv1 IP:10.58.81.220"
echo "2 number represenrtative tv2 IP:10.58.81.225"
echo "3 number represenrtative tv3 IP:10.58.81.222"
echo "4 number represenrtative tv4 IP:10.58.81.223"
echo "5 number represenrtative tv5 IP:10.58.81.230"
read -p "please choice you TV number:" aNum
TV1="10.58.81.220"
TV2="10.58.81.225"
TV3="10.58.81.222"
TV4="10.58.81.223"
TV5="10.58.81.230"
case $aNum in
	1) IP=$TV1
	;;
	2) IP=$TV2
	;;
	3) IP=$TV3
	;;
	4) IP=$TV4
	;;
	5) IP=$TV5
	;;
	*) echo you input number is error
	;;
esac
tvip=$IP
echo $tvip
adb connect $tvip
adbip=`adb connect $tvip|awk -F' ' '{print $4}'`
#echo getUsbPath=`adb -s ${adbip} shell "mount|grep /dev/block/vold/"`
getUsbPath=`adb -s ${adbip} shell "mount|grep /dev/block/vold/"`
#echo usbPath=`echo ${getUsbPath}|awk -F ' ' '{print $2}'`
usbPath=`echo ${getUsbPath}|awk -F ' ' '{print $2}'`
#echo q= adb -s ${adbip} shell ${usbPath}/

#echo p=adb -s ${adbip}　shell ${usbPath}

echo "清空Ｕ盘,释放空间"
adb -s ${adbip} shell rm -rf * ${usbPath} 2>&1>/dev/null

#echo "Ｕ盘,新建文件"
#adb -s ${adbip} shell mkdir ${usbPath}/wo.txt 2>&1>/dev/null

echo "本地文件AAA上传到Ｕ盘"
adb -s ${adbip} push ./TVAutoFlash/A ${usbPath} 2>&1>/dev/null

DateTime=`date`
echo $DateTime
echo "************uploading AAAA file over*****************************"
