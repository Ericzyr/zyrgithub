#!/bin/bash
args=$1
cd djweb4/logcat
cat views.py|sed "s/os.path.dirname(localpath).*/os.path.dirname(localpath) + \'\/${args}\'/g" > viewscope.py
mv viewscope.py views.py 2>&1>/dev/null
sleep 2
fun1(){
#for((i=0;i<1;i++))
#do
cd ..
`python3 manage.py runserver` 2>&1>/dev/null
#sleep 1
#done
}

fun2(){
sleep 5
cd ..
python3 start.py ${args}
sleep 1
}

fun3(){
sleep 10
pig=`netstat -tunlp|grep :8000|awk -F'[ :]+' '{print $9}'|sed 's/\/python.*//g'`
`netstat -tunlp|grep :8000|kill $pig` >/dev/null 2>&1
}

fun1 &
fun2 &
fun3 &
wait

