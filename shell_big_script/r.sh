#!/bin/bash
for(( i=1;i<10;i++ ));do
	for(( j=1;j<10;j++));do
	[ $j -le $i ]&& echo -n $j*$i=$(($j*$i))"   "
	done
	echo "-e"
done
