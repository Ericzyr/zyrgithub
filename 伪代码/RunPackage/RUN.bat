rd /S /Q AutoSmoke_UI30
adb connect 10.75.109.255
adb shell rm -rf /sdcard/AutoSmoke_UI30
adb shell rmdir /sdcard/smoketest
copy E:\TVAutoTest\app\build\outputs\apk\* .
adb push app-debug.apk /data/local/tmp/com.le.tvtest
adb shell pm install -r "/data/local/tmp/com.le.tvtest"
adb push app-debug-androidTest.apk /data/local/tmp/com.le.tvtest.test
adb shell pm install -r "/data/local/tmp/com.le.tvtest.test"
adb shell pm grant com.le.tvtest android.permission.READ_EXTERNAL_STORAGE
adb shell pm grant com.le.tvtest android.permission.WRITE_EXTERNAL_STORAGE
adb push Utf7Ime.apk /data/local/tmp
adb shell pm install -r /data/local/tmp/Utf7Ime.apk
adb shell ime set com.android.testing.dummyime/.DummyIme
adb push TVBOX_TEST_CASE.csv /sdcard/TVBOX_TEST_CASE.csv
rem adb shell am instrument -w -r  -e caseName com.letv.cases.dailybuildin.APPDeskstop#testAppAccountLoginTBO-88964 -e caseFolder test123456 -e debug false com.le.tvtest.test/android.support.test.runner.AndroidJUnitRunner   
rem adb shell am instrument -w -r  -e caseName com.letv.cases.dailybuild.APP#testAPPDeskstopsShowTheWeather183165 -e debug false com.le.tvtest.test/android.support.test.runner.AndroidJUnitRunner 
rem adb shell am instrument -w -r  -e caseName com.letv.cases.dailybuild.APP#testAPPDeskstopsUpdateTheweather183166 -e caseFolder test123456 -e debug false com.le.tvtest.test/android.support.test.runner.AndroidJUnitRunner 
rem adb shell am instrument -w -r  -e caseName com.letv.cases.dailybuild.APP#testAPPDeskstopsSelectCity183167 -e caseFolder test123456 -e debug false com.le.tvtest.test/android.support.test.runner.AndroidJUnitRunner 
rem adb shell am instrument -w -r  -e caseName com.letv.cases.dailybuild.APP#testAPPDeskstopsSelectCity183168 -e caseFolder test123456 -e debug false com.le.tvtest.test/android.support.test.runner.AndroidJUnitRunner 
rem adb shell am instrument -w -r  -e caseName com.letv.cases.dailybuild.APP#testAPPDeskstopsNotificationBar183169 -e caseFolder test123456 -e debug false com.le.tvtest.test/android.support.test.runner.AndroidJUnitRunner 
rem adb shell am instrument -w -r  -e caseName com.letv.cases.dailybuild.APP#testAPPDeskstopsTemperature -e caseFolder test123456 -e debug false com.le.tvtest.test/android.support.test.runner.AndroidJUnitRunner 
rem adb shell am instrument -w -r  -e caseName com.letv.cases.dailybuild.APP#testAPPDeskstopsLanguage183170 -e caseFolder test123456 -e debug false com.le.tvtest.test/android.support.test.runner.AndroidJUnitRunner 
rem adb shell am instrument -w -r  -e caseName com.letv.cases.dailybuild.APP#testAPPDeskstopsSetKey18376 -e caseFolder test123456 -e debug false com.le.tvtest.test/android.support.test.runner.AndroidJUnitRunner 
rem adb shell am instrument -w -r  -e caseName com.letv.cases.dailybuild.APP#testAPPDeskstopsHomeKey183179 -e caseFolder test123456 -e debug false com.le.tvtest.test/android.support.test.runner.AndroidJUnitRunner 
rem adb shell am instrument -w -r  -e caseName com.letv.cases.dailybuild.APP#testAPPDeskstopsReturnKey183180 -e caseFolder test123456 -e debug false com.le.tvtest.test/android.support.test.runner.AndroidJUnitRunner 
rem adb shell am instrument -w -r  -e caseName com.letv.cases.dailybuild.APP#testAPPDeskstopsLeKey183181 -e caseFolder test123456 -e debug false com.le.tvtest.test/android.support.test.runner.AndroidJUnitRunner 
rem adb shell am instrument -w -r  -e caseName com.letv.cases.dailybuild.APP#testAPPDeskstopsSignalSource183182 -e caseFolder test123456 -e debug false com.le.tvtest.test/android.support.test.runner.AndroidJUnitRunner 
adb shell am instrument -w -r  -e caseName com.letv.cases.dailybuild.APP#testAPPDeskstopsShowTheWeather183165 -e caseFolder test123456 -e debug false com.le.tvtest.test/android.support.test.runner.AndroidJUnitRunner 
rem adb shell am instrument -w -r  -e caseName com.letv.cases.dailybuild.APP#testAPPDeskstopsRefresh183189 -e caseFolder test123456 -e debug false com.le.tvtest.test/android.support.test.runner.AndroidJUnitRunner 
rem adb shell am instrument -w -r  -e caseName com.letv.cases.dailybuild.APP#testAPPDeskstopsSwitchTheCity183190 -e caseFolder test123456 -e debug false com.le.tvtest.test/android.support.test.runner.AndroidJUnitRunner 
rem shell am instrument -w -r  -e caseName com.letv.cases.System#testSetTBO-175596 -e caseFolder test123456 -e debug false com.le.tvtest.test/android.support.test.runner.AndroidJUnitRunner 
rem adb shell am instrument -w -r  -e caseName com.letv.cases.System#testSetTBO-175599 -e caseFolder test123456 -e debug false com.le.tvtest.test/android.support.test.runner.AndroidJUnitRunner 
rem adb shell am instrument -w -r  -e caseName com.letv.cases.System#testSetTBO-175600 -e caseFolder test123456 -e debug false com.le.tvtest.test/android.support.test.runner.AndroidJUnitRunner 
rem adb shell am instrument -w -r  -e caseName com.letv.cases.System#testSetTBO-175602 -e caseFolder test123456 -e debug false com.le.tvtest.test/android.support.test.runner.AndroidJUnitRunner 
rem adb shell am instrument -w -r  -e caseName com.letv.cases.System#testSetTBO-175603 -e caseFolder test123456 -e debug false com.le.tvtest.test/android.support.test.runner.AndroidJUnitRunner 
rem adb shell am instrument -w -r  -e caseName com.letv.cases.System#testSetTBO-175615 -e caseFolder test123456 -e debug false com.le.tvtest.test/android.support.test.runner.AndroidJUnitRunner 
rem adb shell am instrument -w -r  -e caseName com.letv.cases.System#testSetTBO-175616 -e caseFolder test123456 -e debug false com.le.tvtest.test/android.support.test.runner.AndroidJUnitRunner
rem adb shell am instrument -w -r  -e caseName com.letv.cases.System#testSetTBO-175650 -e caseFolder test123456 -e debug false com.le.tvtest.test/android.support.test.runner.AndroidJUnitRunner 
rem adb shell am instrument -w -r  -e caseName com.letv.cases.System#testSetTBO-175652 -e caseFolder test123456 -e debug false com.le.tvtest.test/android.support.test.runner.AndroidJUnitRunner  
rem adb shell am instrument -w -r  -e caseName com.letv.cases.System#testSetTBO-175682 -e caseFolder test123456 -e debug false com.le.tvtest.test/android.support.test.runner.AndroidJUnitRunner  
adb pull /sdcard/AutoSmoke_UI30

