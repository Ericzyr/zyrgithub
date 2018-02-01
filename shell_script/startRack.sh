#!/bin/sh
device1="10.75.111.75"
#device2="10.75.108.140"
#device3="10.75.109.255"
device4="10.75.110.44"
cat >>EOF
"*********************"
"**   $device1   **"
"**   $device2   **"
"**   $device3   **"
"**   $device4   **"
"*********************"
EOF
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
echo "* 自动化测试即将开始，从10.75.109.96服务器copy测试资源（caselist,code,picture,video etc.)*"
echo "*                                                                 *"
echo "**************************************************************************************"
expect -c "
	spawn scp -r pc7@10.75.109.96:/home/share/tools ./
  	expect {
   		 \"*assword\" {set timeout 300; send \"123456\r\";}
   		 \"yes/no\" {send \"yes\r\"; exp_continue;}
  		}
  	expect eof"
echo "==================copy资源完成============================="
fi
+
+
echo "=========================请输入文件夹名称的测试===================="
read resultFolder
echo $resultFolder
#resultFolder="testResult"_`date '+%Y%m%d_%H%M%S'`
#918deviceS40 ||918deviceX50  ||  928device1Max65  ||928deviceMax365  ||928deviceX355  ||938device1  ||938device2  ||deviceHK  ||Max470device  ||device1  ||device3  ||device4	
cd tools
gnome-terminal --maximize --tab -t "938_TV1" -e "bash start.sh $device1 ../$resultFolder 938TV1 device1" --tab -t "938_TV4" -e "bash start.sh $device4 ../$resultFolder 938TV4 device4"
#gnome-terminal --maximize --tab -t "938_TV1" -e "bash start.sh $device1 ../$resultFolder 938TV1 device1" #--tab -t "938_TV2" -e "bash start.sh $device2 ../$resultFolder 938TV2 #device2" --tab -t "938_TV3" -e "bash start.sh $device3 ../$resultFolder 938TV3 device3" --tab -t "938_TV4" -e "bash start.sh $device4 ../$resultFolder 938TV4 device4"
echo "================================== MTBF Rack is Started =================================="
echo " "
echo "MTBF测试已经启动，可以执行以下命令来获取当前测试结果:"
echo " "
echo "python tools/parse.py "$resultFolder
echo " "
echo "================================== MTBF Rack is Started =================================="

