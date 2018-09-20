#!/bin/sh
device1="10.58.80.199"
#device2="10.58.80.152"
echo "*********************"
echo "**   $device1   **"
echo "**   $device2   **"
echo "*********************"
function pause(){
        read -n 1 -p "$*" INP
}
pause '检查startRack.sh中上述TV IP和对应的账号是否匹配 IP是否需要修改，请按任意键继续 ～'
echo "=========================是否copy最新测试资源 Y or N=================="
read chose
echo $chose
if [ $chose == "Y" ] || [ $chose == "y" ];then
echo "**************************************************************************************"
echo "*                                                                 *"
echo "* 自动化测试即将开始，从10.58.81.227服务器copy测试资源（caselist,code,picture,video etc.)*"
echo "*                                                                 *"
echo "**************************************************************************************"
expect -c "
	spawn scp -r pc6@10.58.81.227:/home/share/tools ./
  	expect {
   		 \"*assword\" {set timeout 300; send \"admin\r\";}
   		 \"yes/no\" {send \"yes\r\"; exp_continue;}
  		}
  	expect eof"
echo "==================copy资源完成============================="
fi

echo "========================= input the Folder name of testing!!! ===================="
read resultFolder
echo $resultFolder
#resultFolder="testResult"_`date '+%Y%m%d_%H%M%S'`
#918deviceS40 ||918deviceX50  ||  928device1Max65  ||928deviceMax365  ||928deviceX355  ||938device1  ||938device2  ||deviceHK  ||Max470device  ||device1  ||device3  ||device4	
# --tab -t "938_TV1" -e "bash start.sh $device1 ../$resultFolder 938TV1_X43 device1"
cd tools
gnome-terminal --maximize --tab -t "938_TV1" -e "bash start.sh $device1 ../$resultFolder 938TV1_X43 device1" #--tab -t "938_TV2" -e "bash start.sh $device2 ../$resultFolder 938TV2_X43N device2" #--tab -t "938_TV4" -e "bash start.sh $device4 ../$resultFolder 938TV4_X50M device4"
echo "================================== MTBF Rack is Started =================================="
echo " "
echo "MTBF测试已经启动，可以执行以下命令来获取当前测试结果:"
echo " "
echo "python tools/parse.py "$resultFolder
echo " "
echo "================================== MTBF Rack is Started =================================="

