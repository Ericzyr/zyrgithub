package com.letv.cases.leui;

import android.support.test.uiautomator.By;
import android.support.test.uiautomator.BySelector;
import android.support.test.uiautomator.UiObject2;
import android.support.test.uiautomator.UiObjectNotFoundException;

import com.letv.common.AppName;
import com.letv.common.CaseName;
import com.letv.common.IntentConstants;
import com.letv.common.LetvTestCase;

import org.junit.Test;

/**
 * Created by letv on 16-7-21.
 */
public class CIBN extends LetvTestCase{
    int count =0;

    @Override
    public void tearDown() throws Exception {
        press_back(1);
        press_down(2);
        press_center(1);
        verify("没有返回桌面", phone.getCurrentPackageName().equals(PACKAGE_HOME));
    }

    BySelector CIBNS=By.pkg("cn.cibntv.ott");
    @Test
    @CaseName("CIBN高清影视应用里反复滑动")
    public void testCIBNSwipe() throws UiObjectNotFoundException {
        launchApp(AppName.CIBN, IntentConstants.CIBN);
        sleepInt(5);
        for (int Loop = 0; Loop < getIntParams("Loop"); Loop++) {
            System.out.println(".............looper : " + Loop);
            try {
                CIBNSwipe();
            }catch (Exception e){
                try {
                    count ++;
                    failCount(count, getIntParams("Loop"), e.getMessage());
                    launchApp(AppName.CIBN, IntentConstants.CIBN);
                    sleepInt(5);
                    CIBNSwipe();
                }catch (RuntimeException re){
                    screenShot();
                    junit.framework.Assert.fail(re.getMessage());
                }
            }
        }
//        press_back(1);
//        press_down(2);
//        press_center(1);
//        verify("没有返回桌面", phone.getCurrentPackageName().equals(PACKAGE_HOME));
    }

    public void CIBNSwipe() throws UiObjectNotFoundException{
        addStep("上下键各13次");
        press_down(13);
        UiObject2 CIBN=phone.findObject(CIBNS);
        check("不在CIBN高清影视应用", CIBN != null);
        press_up(13);
        UiObject2 CIBN1=phone.findObject(CIBNS);
        check("不在CIBN高清影视应用", CIBN1 != null);
        for(int i=0;i<13;i++){
            press_right(10);
            UiObject2 CIBN3=phone.findObject(CIBNS);
            check("不在CIBN高清影视应用", CIBN3 != null);
            press_left(10);
            press_down(1);
            UiObject2 CIBN2=phone.findObject(CIBNS);
            check("不在CIBN高清影视应用", CIBN2 != null);
        }
    }

    @Test
    @CaseName("CIBN高清影视各频道列表观看视频")
    public void testLiveChannel() throws UiObjectNotFoundException {
        launchApp(AppName.CIBN, IntentConstants.CIBN);
        sleepInt(5);
        for (int Loop = 0; Loop < getIntParams("Loop"); Loop++) {
            System.out.println(".............looper : " + Loop);
            try {
                LiveChannel();
            }catch (Exception e){
                try {
                    count ++;
                    failCount(count, getIntParams("Loop"), e.getMessage());
                    launchApp(AppName.CIBN, IntentConstants.CIBN);
                    sleepInt(5);
                    LiveChannel();
                }catch (RuntimeException re){
                    screenShot();
                    junit.framework.Assert.fail(re.getMessage());
                }
            }
        }
    }

    public void LiveChannel() throws UiObjectNotFoundException {
        UiObject2 CIBN=phone.findObject(CIBNS);
        check("不在CIBN高清影视应用", CIBN != null);
        press_up(10);
        press_left(10);
        press_down(3);
//            UiObject2 live = waitForObj(By.text("轮播"));
//            check("没有找到轮播频道", live != null);
//            live.click();
//            live.click();
//            sleepInt(1);
        press_right(1);
        press_center(1);
        UiObject2 allChannel=waitForObj(By.text("全部频道"));
        check("没有找到全部频道", allChannel != null);
        sleepInt(1);
        UiObject2 list=waitForObjs(By.clazz("android.widget.ListView")).get(1);
        check("can't find list",list!=null);
        int count =list.getChildCount();
        for(int i=0;i<count;i++){
            UiObject2 list1=waitForObjs(By.clazz("android.widget.ListView")).get(1);
            check("can't find list",list1!=null);
            UiObject2 channel=list1.getChildren().get(i);
            String channelName=channel.findObject(By.res("cn.cibntv.ott:id/textView")).getText();
            addStep("切换到"+channelName+"观看60s");
            check("没有找到频道列表", channel != null);
            channel.click();
            sleepInt(15);
            press_center(1);
        }
        sleepInt(5);
        press_back(1);
    }
}
