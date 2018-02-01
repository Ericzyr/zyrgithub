#!/bin/bash
#传参数的
i=$1

#[ $i -eq 0 ]&& echo 0|| echo 1

if [ $1 -eq 1 ];then
  echo 等于1
else
  echo 等于0
fi
