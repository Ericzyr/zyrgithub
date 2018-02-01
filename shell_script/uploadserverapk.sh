#!/bin/bash
echo "***********************************************************"
echo "*before stress test start，Upload local APK to the server*"
echo "***********************************************************"
function pause(){
        read -n 1 -p "$*" INP
}
pause '检查，请按任意键***继续 ～'

expect -c "
	spawn scp -r /home/pc7/StressApp/MainLineMTBF_CN/app/build/outputs/apk/app-debug.apk pc7@10.58.81.227:/home/pc7/jiralog/MTBFAPK/TVAPK/CN/
	
  	expect {
   		 \"*assword\" {set timeout 300; send \"123456\r\";}
   		 \"yes/no\" {send \"yes\r\"; exp_continue;}
  		}
  	expect eof"
expect -c "
	spawn scp -r /home/pc7/StressApp/MainLineMTBF_CN/app/build/outputs/apk/app-debug-androidTest.apk pc7@10.58.81.227:/home/pc7/jiralog/MTBFAPK/TVAPK/CN/
	
  	expect {
   		 \"*assword\" {set timeout 300; send \"123456\r\";}
   		 \"yes/no\" {send \"yes\r\"; exp_continue;}
  		}
  	expect eof"
DateTime=`date`
echo $DateTime
echo "=====================Upload server over================="
