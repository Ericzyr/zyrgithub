#!/bin/bash
cd /home/pc7
if [ -e 'thtest' ];then
    echo '文件已存在!'
else
    mkdir thtest
fi
echo "to"
