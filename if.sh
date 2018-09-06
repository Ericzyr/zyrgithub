#!/bin/bash
cd /home/pc6
if [ -e 'thtest' ];then
    echo '文件已存在!'
else
    mkdir thtest
fi
