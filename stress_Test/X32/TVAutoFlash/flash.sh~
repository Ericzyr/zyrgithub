#!/bin/sh
device1="10.57.5.75"
#device2="10.57.4.198"
RELEASE_SMB_SERVER="//imgrepo-cnbj.devops.letv.com/dailybuild/"
server_path="SuperTV/demeter/cn/aosp_mangosteen/daily/20170604/x450_demeter_final_V2401RCN02C060246D06031T_20170603_212506_cibn_userdebug/aosp_mangosteen_ota_V2401RCN02C060246D06031T/"
file_name="X450_MANGOSTEEN-cn-cibn-V2401RCN02C060246D06031T-6.0.246T-userdebug.zip"


#RELEASE_SMB_SERVER="//imgrepo-cnbj.devops.letv.com/dailybuild/"
#server_path="SuperTV/demeter/cn/aosp_mangosteen/daily/20170426/x450_demeter_final_eui5.9_V2401RCN02C059241D04261T_20170426_021201_cibn_userdebug/aosp_mangosteen_ota/"
#file_name="X450_MANGOSTEEN-cn-cibn-V2401RCN02C059241D04261T-5.9.241T-userdebug.zip"


echo "*********************"
echo "**   $device1   **"
echo "**   $device2   **"
echo "**   $device3   **"
echo "**   $device4   **"
echo "*********************"


function download(){
	begin=`date +%s`
	echo "smbclient \"$RELEASE_SMB_SERVER\" -N -D \"$server_path\" -c \"recurse;prompt;mget $file_name\""
	smbclient "$RELEASE_SMB_SERVER" -N -D "$server_path" -c "recurse;prompt;mget $file_name"
}

download

mkdir -p ./flashapk
cd ./flashapk
#从文件共享服务器获取apks和smoke.jar
#smbclient //10.148.18.17/jiralog -c "cd SMOKEAPK/CN_6.0_TV;prompt;mget *" -N
smbclient //10.148.18.17/jiralog -c "cd MTBFAPK/TVAPK/CN;prompt;mget app-debug.apk app-debug-androidTest.apk" -N
cd ../
gnome-terminal --maximize --tab -t "938_TV1_update" -e "bash flashTV.sh $device1 $file_name" 
#--tab -t "938_TV2_update" -e "bash flashTV.sh $device2 $file_name"
#--tab -t "938_TV2" -e "bash start.sh $device2 ../$resultFolder TV2 device2" --tab -t "938_TV3" -e "bash start.sh $device3 ../$resultFolder TV3 device3" --tab -t "938_TV4" -e "bash start.sh $device4 ../$resultFolder TV4 device4"

