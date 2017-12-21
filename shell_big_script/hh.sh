#!/bin/bash
path=//imgrepo-cnbj.devops.letv.com/dailybuild/SuperTV/hera/cn/aosp_almond_letv_hera_dtmb_sub/daily/20171108/x440r_hera_V2601RCN02C060269D11081D_20171108_021832_cibn_userdebug/aosp_almond_letv_hera_dtmb_sub_ota_V2601RCN02C060269D11081D/X440R_ALMOND_LETV_HERA_DTMB_SUB-cn-cibn-V2601RCN02C060269D11081D-6.0.269D-userdebug.zip
echo $path
echo " "
Server=`echo ${path}| cut -d / -f -3`/
echo $Server
echo " "
Dailybulild=`echo ${path}| cut -d / -f 4-12`/
echo $Dailybulild
echo " "
Name=`echo ${path}| cut -d / -f 13`
echo $Name
echo " "
