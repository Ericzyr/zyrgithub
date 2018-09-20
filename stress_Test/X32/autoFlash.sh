#!/bin/bash
while true; do
  	echo "check smbclient process"
  	if [ `ps -aux | grep -c smbclient` -eq 1 ];then
    	echo "There is no smbclient!!! continue!!!"
		break
	else
		sleep 10
    fi
  done
  
  test_root_path=~/flash/Smoke
  
  if [ -n "${PRODUCT_NAME}" ] && [ -n "${RELEASE_SMB_SUBPATH}" ] && [ -n "${RELEASE_SMB_SERVER}" ];then
      local_test_path="$test_root_path/${PRODUCT_NAME}/$(basename ${RELEASE_SMB_SUBPATH})"
      echo "--------------------------------------------down pkg to $local_test_path-----------------------------------------------"
      if [ -d $local_test_path ];then
      	if [ -n "`ls $local_test_path`" ];then
        	echo "pkg is already download"
            bash ~/tools/auto/shell/update_x50.sh $PRODUCT_NAME ${IPADDRESS} ${local_test_path}
        	exit 0
        fi
      fi
      test -d $local_test_path || mkdir -p $local_test_path
      oldpath=`pwd`
      cd $local_test_path
      OLD_IFS=$IFS
      IFS=$','
      release_files=X450_CIBN*USERDEBUG.zip
      echo "--------------------------------------------server:${RELEASE_SMB_SERVER} path:${PRODUCT_NAME}/${RELEASE_SMB_SUBPATH}/${release_dir} files:${release_files}-----------------------------------------------"
      smbclient "${RELEASE_SMB_SERVER}" -N -D "${PRODUCT_NAME}/${RELEASE_SMB_SUBPATH}" -c "recurse;prompt;mget ${release_files}" || exit 1
      echo "--------------------------------------------down pkg done-----------------------------------------------"
      echo "--------------------------------------------run update.sh-----------------------------------------------"
      cd ${oldpath}
      bash ~/tools/auto/shell/update_x50.sh $PRODUCT_NAME ${IPADDRESS} ${local_test_path}
      echo "--------------------------------------------update.sh finished-----------------------------------------------"
      IFS=$OLD_IFS
  else
      echo "Local test path parameters missing, pls check."
      exit 1
  fi
