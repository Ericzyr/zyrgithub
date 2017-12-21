#!/bin/bash
path=//imgrepo-cnbj.devops.letv.com/dailybuild/SuperTV/demeter/cn/aosp_mangosteen/daily/20170908/x450_demeter_final_V2401RCN02C060260D09081D_20170908_215411_cibn_userdebug/aosp_mangosteen_ota_V2401RCN02C060255D08012D/X450_MANGOSTEEN-cn-cibn-V2401RCN02C060255D08012D-6.0.255D-userdebug.zip
echo $path
echo " "
Server=`echo ${path}| cut -d / -f -3`/
echo $Server
echo " "
Dailybuild=`echo ${path}| cut -d / -f 4-12`/
echo $Dailybuild
echo " "
Name=`echo ${path}| cut -d / -f 13`
echo $Name
echo " "
