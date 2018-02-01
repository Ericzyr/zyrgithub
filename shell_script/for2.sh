#!/bin/bash -
for((i=0;i<10;i++));do
echo "产生的随机数"
echo $RANDOM|md5sum|cut -c 1-5
done
