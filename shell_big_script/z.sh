#!/bin/bash
function error(){
  echo you choice is number $num
}
read -p "word number:" num  
case $num in
1) error;;
2) echo 2
esac
