#!/bin/bash
read -p "请输入你的IP地址:" IP
adb connect $IP
active=`adb -s $IP:5555 shell dumpsys activity activities|grep "mFocusedActivity: ActivityRecord"|awk -F'[ :]+' '{print $5}'`
echo $active
