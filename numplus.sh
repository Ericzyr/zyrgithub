#!/bin/bash
for((i=0;i<3;i++));do
	for((j=0;j<10;j++));do
		b=5
		a=$(($j+$b))
		echo $a
	done
done
