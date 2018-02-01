#!/bin/bash
zenity --question --title "电视升级" --text "你是否进入电视离线升级？" &>/dev/null
[ $? -eq 0 ]|| exit 1
number=$(zenity --entry --title "TVIP" --text "电视IP：
1 10.75.111.75
2 10.75.108.140
3 10.75.109.255
4 10.75.110.44
5 10.75.109.177
")&>/dev/null
echo $number
FIRSTNAME=$(zenity --entry --title "TV" --text "请输入你的电视路径：") &>/dev/null
echo $FIRSTNAME
FIRSTNAME1=$(zenity --entry --title "TV" --text "电视包文件：") &>/dev/null
echo $FIRSTNAME1
