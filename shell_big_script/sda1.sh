#!/bin/bash
sda=`df -h|grep "^/dev"/|awk -F'[ ]+' '{print $5}'|sed 's/%//g'`
[ $sda -ge 10 ]&& echo -e "你的硬盘容量过大超过\033[31m80%\033[0m了"|| exit
zenity --question --title "电脑硬盘详细" --text "你的硬盘容量过大超过了80%" &>/dev/null

