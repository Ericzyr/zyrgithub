#!/bin/bash -
#a=5
#[ ${a} -eq 5 ]&& echo "number is eq" ||echo "number is no"
read -p "input you world:" number
cat wub.txt|grep -a -x -A 1 "${number}"|sed -n 2'p'
	


