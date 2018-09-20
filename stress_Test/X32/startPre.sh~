echo "**************************************************************************************"
echo "*                                                                 *"
echo "* 自动化测试即将开始，从10.57.2.68服务器copy测试资源（caselist,code,picture,video etc.)*"
echo "*                                                                 *"
echo "**************************************************************************************"
function pause(){
        read -n 1 -p "$*" INP
}
pause '检查startRack.sh中TV IP是否修改，请按任意键继续 ～'
expect -c "
	spawn scp -r letv@10.57.2.68:/home/letv/TV_MTBF/Resource/tools ./
  	expect {
   		 \"*assword\" {set timeout 300; send \"letv\r\";}
   		 \"yes/no\" {send \"yes\r\"; exp_continue;}
  		}
  	expect eof"
