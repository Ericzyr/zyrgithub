#!/bin/bash
echo "***********************************************************"
echo "***************Stress test backupsScript******************"
echo "***********************************************************"
cd /home/pc7/StressApp/$tar
tar=`tar zcvf MainLineMTBF_CN.tar.gz MainLineMTBF_CN`
DateTime=`date`
echo $DateTime
function pause(){
        read -n 1 -p "$*" INP
}
pause '请按任意键***继续 ～'

expect -c "
	spawn scp -r /home/pc7/StressApp/MainLineMTBF_CN.tar.gz pc7@10.58.81.227:/home/pc7/StressScript/
	
  	expect {
   		 \"*assword\" {set timeout 300; send \"123456\r\";}
   		 \"yes/no\" {send \"yes\r\"; exp_continue;}
  		}
  	expect eof"
echo "=====================备份完成================="
