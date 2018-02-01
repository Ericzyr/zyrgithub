#!/bin/bash
read -p"input you name:" name
echo "hello! $name let go game!"
echo "=======是否copy最新测试资源 Y or N======"
read chose
echo $chose
if [ $chose == "Y" ] || [ $chose == "y" ];then
echo "chose correct"
else
echo "chose error"
fi
