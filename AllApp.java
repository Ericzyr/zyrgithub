package com.letv.cases.leui;

import android.os.RemoteException;
import android.support.test.uiautomator.By;
import android.support.test.uiautomator.UiObject2;
import android.support.test.uiautomator.UiObjectNotFoundException;

import com.letv.common.CaseName;
import com.letv.common.LetvTestCase;

import junit.framework.Assert;

import org.junit.After;
import org.junit.Test;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Pattern;

/**
 * Created by zhoujine on 2016/4/29.
 */
public class AllApp extends LetvTestCase{
    ArrayList<String> listApps = new ArrayList<String>();
    int count =0;
    @After
    public void tearDown(){
        UiObject2 newFolder = phone.findObject(By.text("新建文件夹"));
        if(newFolder!=null){
            newFolder.click();
            newFolder.click();
            sleepInt(1);
            int count=waitForObj(By.clazz("android.support.v7.widget.RecyclerView")).getChildCount();
            press_left(1);
            press_menu(1);
            sleepInt(2);
            UiObject2 moveApp = waitForObj(By.clazz("android.widget.TextView").text("移动应用"));
            verify("移动应用不存在", moveApp!=null);
            addStep("从文件夹移出应用到桌面");
            for (int i = 0; i < count; i++) {
                press_center(1);
                press_up(1);
                press_center(1);
            }
        }
    }
    public void exitApp1() throws UiObjectNotFoundException {
        press_back(1);
        for(int j=0;j<2;j++){
            for(int i=0;i<3;i++){
                if(phone.getCurrentPackageName().equals(PACKAGE_HOME))break;
                UiObject2 exitTips = phone.findObject(By.text(Pattern.compile("退出|.*退出|确定|是的|残忍离去")));
                if(exitTips!=null){
                    exitTips.click();
                    sleepInt(1);
                    break;
                }else press_back(1);
            }
        }
        sleepInt(1);
        if(!phone.getCurrentPackageName().equals(PACKAGE_HOME))press_home(1);
        check("没有退出应用", phone.getCurrentPackageName().equals(PACKAGE_HOME));
    }

    @Test
    @CaseName("逐次打开应用里面所有应用")
    public void testAppDesk() throws UiObjectNotFoundException, RemoteException {
        gotoHomeScreen("应用");
        for (int Loop = 0; Loop < getIntParams("Loop"); Loop++) {
            System.out.println(".............looper : " + Loop);
            try{
                AppDesk();
            }catch (Exception e){
                try {
                    count ++;
                    failCount(count, getIntParams("Loop"), e.getMessage());
                    gotoHomeScreen("应用");
                    AppDesk();
                }catch (RuntimeException re){
                    screenShot();
                    Assert.fail(re.getMessage());
                }
            }
        }
    }

/*    public void AppDesk() throws UiObjectNotFoundException, RemoteException {
        String[] apps={"设置","日历","设置","乐视视频","乐视游戏中心","乐视应用商店","乐视体育","购物","系统更新","音乐","乐看搜索","浏览器","文件管理","电视管家","日历","设置","相册","乐视云盘","同步院线","天气"};
        for(int k=0;k<apps.length;k++){
            enterApps(apps[k]);
            exitApp();
            if(!phone.getCurrentPackageName().equals("com.stv.launcher"))press_home(1);
            UiObject2 application=phone.findObject(By.text("应用").pkg("com.stv.launcher"));
            verify("没有找到应用桌面",application!=null);
            application.click();
            sleepInt(2);
        }
    }*/

    public boolean enterApps(String app) throws UiObjectNotFoundException,RemoteException{
        UiObject2 appItem;
        List<UiObject2> folders;
        for (int i = 0; i < 4; i++) {
            appItem = phone.findObject(By.pkg("com.stv.launcher").text(Pattern.compile(app)));
            if (appItem != null) { // find the app oncurrent window
                appItem.click();
                sleepInt(1);
                for(int k=0;k<3;k++) {
                    UiObject2 appItem1 = phone.findObject(By.text(Pattern.compile(app)));
                    if (appItem1 != null) {
                        appItem1.click();
                        sleepInt(1);
                    }else break;
                }
                sleepInt(3);
                verify("Open " + app + " failed", !phone.getCurrentPackageName().equals("com.stv.launcher"));
                UiObject2 upgrade=phone.findObject(By.text(Pattern.compile("升级|允许")));
                if(upgrade!=null){
                    upgrade.click();
                    sleepInt(1);
                    UiObject2 upgrade1=phone.findObject(By.text(Pattern.compile("升级|允许")));
                    if(upgrade1!=null)upgrade1.click();
                    sleepInt(5);
                }
                return true;
            }
            press_down(2);
            sleep(500);
        }
        return false;
    }

    public void AppDesk() throws UiObjectNotFoundException, RemoteException {
        press_back(1);
        press_down(1);
        //打开应用桌面前三个应用com.stv.launcher:id/app_workspace_top_layout
        for(int i=0;i<3;i++){
            UiObject2 topWorkspace=waitForObj(By.res(Pattern.compile("com.stv.PACKAGE_HOME:id/app_workspace_top_layout|com.stv.plugin.app:id/app_workspace_top_layout|com.stv.launcher:id/app_workspace_top_layout")));
            verify("topworkspace object 不存在",topWorkspace!=null);
            List<UiObject2> topLayout = topWorkspace.getChildren();
            UiObject2 app=topLayout.get(i);
            addStep("打开应用" + app.findObject(By.clazz("android.widget.TextView")).getText());
            if(i==0){
                clickAndWaitForNewWindow(app);
            }else{
                press_center(1);
            }
            sleepInt(3);
            UiObject2 upgrade=phone.findObject(By.text("升 级"));
            if(upgrade!=null){
                upgrade.click();
                sleepInt(30);
                press_right(3);
            }
            sleepInt(5);
            check("没有进入应用", !phone.getCurrentPackageName().equals(PACKAGE_HOME));
            exitApp1();
            if(i!=2){
                press_right(1);
            }
        }

        for(int j=0;j<2;j++){
            press_down(1);
            for(int i=0;i<5;i++){
                UiObject2 recyclerView = phone.findObject(By.clazz("android.support.v7.widget.RecyclerView"));
                UiObject2 app=recyclerView.getChildren().get(i);
                String appName=app.findObject(By.clazz("android.widget.TextView")).getText();
                addStep("打开应用"+appName);
                press_center(1);
                sleepInt(5);

                UiObject2 tools=phone.findObject(By.clazz("android.widget.EditText").text(Pattern.compile("工具|CIBN推荐应用|新建文件夹.*")));
                if(tools!=null){
                    openToolApp();
                }
                UiObject2 tools1=phone.findObject(By.clazz("android.widget.EditText").text(Pattern.compile("工具|CIBN推荐应用|新建文件夹.*")));
                check("没有进入应用", !phone.getCurrentPackageName().equals(PACKAGE_HOME) || tools1 != null);
                exitApp1();
                if(i!=4)press_left(1);
            }
            UiObject2 tools1=phone.findObject(By.clazz("android.widget.EditText").text(Pattern.compile("工具|CIBN推荐应用|新建文件夹.*")));
            if(tools1!=null){
                press_back(2);
            }
            press_down(1);

            for(int i=0;i<5;i++){
                UiObject2 recyclerView = phone.findObject(By.clazz("android.support.v7.widget.RecyclerView"));
                UiObject2 app=recyclerView.getChildren().get(i);
                String appName=app.findObject(By.clazz("android.widget.TextView")).getText();
                addStep("打开应用"+appName);
                press_center(1);
                sleepInt(5);

                UiObject2 tools=phone.findObject(By.clazz("android.widget.EditText").text(Pattern.compile("工具|CIBN推荐应用|新建文件夹.*")));
                if(tools!=null){
                    openToolApp();
                }
                UiObject2 tools2=phone.findObject(By.clazz("android.widget.EditText").text(Pattern.compile("工具|CIBN推荐应用|新建文件夹.*")));
                check("没有进入应用", !phone.getCurrentPackageName().equals(PACKAGE_HOME)||tools2!=null);
                addStep("退出应用"+appName);
                exitApp1();
                if(i!=4)press_right(1);
            }
        }
    }
  /*  @Test
    @CaseName("逐次打开应用里面所有应用")
    public void testAppDesk() throws UiObjectNotFoundException, RemoteException {
        listApps = initListApps();
        for (int Loop = 0; Loop < getIntParams("Loop"); Loop++) {
            System.out.println(".............looper : " + Loop);
            gotoHomeScreen("应用");
            //打开应用桌面前三个应用
            for(int i=0;i<3;i++){
                List<UiObject2> topLayout = phone.findObject(By.res(Pattern.compile("com.stv.PACKAGE_HOME:id/app_workspace_top_layout|com.stv.launcher:id/app_workspace_top_layout"))).getChildren();
                UiObject2 app=topLayout.get(i);
                addStep("打开" + app.findObject(By.clazz("android.widget.TextView")).getText());
                //	press_center(1);
                app.click();
                app.click();
                sleepInt(5);
                verify("没有进入应用", !phone.getCurrentPackageName().equals(PACKAGE_HOME));
                exitApp1();
                //	verify(app.getText()+" 应用没有选中", app.isFocused());
            }
            for(int j=0;j<2;j++){
                if(j==1){
                    press_down(7);
                }

                int count =phone.findObject(By.clazz("android.support.v7.widget.RecyclerView")).findObjects(By.clazz("android.widget.TextView")).size();
                addStep("count="+count);
                for(int i=0;i<count;i++){
                    List<UiObject2> apps =phone.findObject(By.clazz("android.support.v7.widget.RecyclerView")).findObjects(By.clazz("android.widget.TextView"));
                    String appName=apps.get(i).getText();
                    if(listApps.contains(appName) && appName!=null){
                       addStep("i="+i);
                        addStep("打开" + appName);
                        verify(appName + "应用不存在", apps.get(i) != null);
                        apps.get(i).click();
                        sleepInt(2);
                        UiObject2 appTools=phone.findObject(By.pkg("com.stv.launcher").text(appName));
                        if(appTools!=null)appTools.click();
                        sleepInt(2);
                        UiObject2 appTools1=phone.findObject(By.pkg("com.stv.launcher").text(appName));
                        if(appTools1!=null)appTools1.click();
                        sleepInt(5);
                    UiObject2 tools=phone.findObject(By.clazz("android.widget.EditText").text("工具"));
                    if(tools!=null){
                        openToolApp();
                    }
                        exitApp1();
                        for(int w=0;w<5;w++) {
                            UiObject2 tools1 = phone.findObject(By.clazz("android.widget.EditText").text("工具"));
                            if (tools1 != null) {
                                press_back(1);
                            }else break;
                        }
                    }
                }
            }
        }
    }*/

    private ArrayList<String> initListApps() {
        ArrayList<String> list = new ArrayList<String>() {
            {
                addStep("播放记录");
                addStep("电视乐拍");
                addStep("下载中心");
                addStep("使用帮助");
                addStep("超级语音");
                add("购物");
                add("浏览器");
                add("乐视应用商店");
                add("乐看搜索");
                add("乐视游戏中心");
                add("主题");
                add("会员帐号");
                add("电视管家");
                add("文件管理");
                add("消息");
                add("日历");
                add("问题反馈");
                add("电视乐拍");
                add("天气");
                add("设置");
                add("相册");
                add("媒体中心");
                add("系统更新");
                add("使用帮助");
                add("视频通话");
                add("下载中心");
                addStep("同步院线");
                addStep("多乐电视助手");
                addStep("乐视体育");
                addStep("音乐");
                addStep("乐视帐号");
            }
        };
        return list;
    }

    public void openToolApp() throws UiObjectNotFoundException {
        //打开工具文件夹里面的app
        addStep("打开工具文件夹里面的app");
        UiObject2 appTools=waitForObj(By.clazz("android.support.v7.widget.RecyclerView"));
        int count1=appTools.getChildCount();
        press_left(1);
        if(count1>=4){
            for(int k=0;k<4;k++){
                UiObject2 app=appTools.getChildren().get(k);
                String appNameT=app.getText();
                check("没有找到" + appNameT, app != null);
                press_center(1);
                sleepInt(3);
                check("没有进入应用", !phone.getCurrentPackageName().equals(PACKAGE_HOME));
                press_home(1);
                press_right(1);
            }
            press_down(1);
                for(int k=0;k<count1-4;k++){
                    UiObject2 app=appTools.getChildren().get(k);
                    String appNameT=app.getText();
                    check("没有找到" + appNameT, app != null);
                    press_center(1);
                    sleepInt(3);
                    check("没有进入应用", !phone.getCurrentPackageName().equals(PACKAGE_HOME));
                    press_home(1);
                    press_left(1);
                }
        }else {
            for(int k=0;k<count1;k++){
                UiObject2 app=appTools.getChildren().get(k);
                String appNameT=app.getText();
                check("没有找到" + appNameT, app != null);
                press_center(1);
                sleepInt(3);
                check("没有进入应用", !phone.getCurrentPackageName().equals(PACKAGE_HOME));
                press_home(1);
                press_right(1);
            }
        }
    }

    @Test
    @CaseName("新建文件夹，移动应用进出文件夹")
    public void testAppFolder() throws UiObjectNotFoundException, RemoteException {
        gotoHomeScreen("应用");
        press_down(2);
        for (int Loop = 0; Loop < getIntParams("Loop"); Loop++) {
            System.out.println(".............looper : " + Loop);
           // AppFolder();
            try{
                AppFolder();
            }catch (Exception e){
                try {
                    count ++;
                    failCount(count, getIntParams("Loop"), e.getMessage());
                    gotoHomeScreen("应用");
                    press_down(2);
                    AppFolder();
                }catch (RuntimeException re){
                    screenShot();
                    Assert.fail(re.getMessage());
                }
            }
        }
        addStep("退出文件夹模式");
        exitApp();
        exitApp();
    }

    public void AppFolder() throws UiObjectNotFoundException, RemoteException {
        addStep("新建文件夹");
        press_menu(1);
        press_up(1);
        UiObject2 createFolder = waitForObj(By.text("新建文件夹"));
        check("新建文件夹不存在", createFolder != null);
        createFolder.click();
        createFolder.click();
        sleepInt(1);
        List<UiObject2> addAppp=waitForObj(By.clazz("android.support.v7.widget.RecyclerView")).findObjects(By.res(Pattern.compile("com.stv.launcher:id/cellview_editIco")));
            if(addAppp.size()!=0){
                addStep("移动5个应用进入文件夹");
            check("要移动进文件夹的app不存在", addAppp.get(0)!=null);
            addAppp.get(0).click();
            press_center(1);
            sleepInt(1);
            check("要移动进文件夹的app不存在", addAppp.get(1) != null);
            addAppp.get(1).click();
            press_center(1);
            sleepInt(1);
            check("要移动进文件夹的app不存在", addAppp.get(2) != null);
            addAppp.get(2).click();
            press_center(1);
            sleepInt(1);
            check("要移动进文件夹的app不存在", addAppp.get(3) != null);
            addAppp.get(3).click();
            press_center(1);
            sleepInt(1);
            check("要移动进文件夹的app不存在", addAppp.get(4) !=null);
            addAppp.get(4).click();
            press_center(1);
            sleepInt(1);
            press_back(1);
        }else {
                addStep("移动3个应用进入文件夹");
                press_right(1);
                for(int i=0;i<3;i++){
                    UiObject2 folder=phone.findObject(By.clazz("android.widget.RelativeLayout").focused(true));
                    int number=folder.getChildCount();
                    if(number==2){
                        press_right(1);
                    }
                    press_center(1);
                }
                press_back(1);
        }

        addStep("进入新建文件夹");
        UiObject2 newFolder = waitForObj(By.text(Pattern.compile("新建文件夹.*")));
        check("新建文件夹不存在", newFolder != null);
        newFolder.click();
        sleepInt(1);
        UiObject2 newFolder1 = waitForObj(By.text(Pattern.compile("新建文件夹.*")));
        if(newFolder1!=null)newFolder1.click();
        sleepInt(1);
        press_left(1);
        int count1=waitForObj(By.clazz("android.support.v7.widget.RecyclerView")).getChildCount();
        press_menu(1);

        sleepInt(2);
        UiObject2 moveApp = waitForObj(By.clazz("android.widget.TextView").text("移动应用"));
        check("移动应用不存在", moveApp != null);
        addStep("从文件夹移出"+count1+"个应用到桌面");
        for (int i = 0; i < count1; i++) {
            addStep("从文件夹移除1个文件");
            press_center(1);
            press_up(1);
            press_center(1);
            int count2=waitForObj(By.clazz("android.support.v7.widget.RecyclerView")).getChildCount();
            UiObject2 folder=waitForObj(By.clazz("android.widget.EditText").text("新建文件夹"));
            verify("应用移除失败",count1>count2||folder==null);
        }
    }
}
