package com.letv.cases.leui;


import android.os.Build;
import android.os.RemoteException;
import android.support.test.uiautomator.By;
import android.support.test.uiautomator.BySelector;
import android.support.test.uiautomator.UiObject2;
import android.support.test.uiautomator.UiObjectNotFoundException;
import android.support.test.uiautomator.UiWatcher;

import com.letv.common.AppName;
import com.letv.common.CaseName;
import com.letv.common.IntentConstants;
import com.letv.common.LetvTestCase;

import junit.framework.Assert;

import org.junit.Test;

import java.util.regex.Pattern;

/**
 * Created by zhoujine on 2016/4/20.
 */
public class Browser extends LetvTestCase {
    int count=0;
    BySelector clearDataS = By.clazz("android.widget.TextView").text(Pattern.compile("数据清理|Data clear"));
    BySelector okButtonS = By.text(Pattern.compile("确定|OK"));
    BySelector addressBarS = By.clazz("android.widget.EditText").text(Pattern.compile("搜索或输入网址|Search or type URL"));
    BySelector check1S = By.clazz("android.widget.TextView").text(Pattern.compile("设置|Settings"));
    BySelector check2S = By.clazz("android.widget.TextView").text(Pattern.compile("清除网页缓存|Clear web cache"));
    BySelector check3S = By.clazz("android.widget.TextView").text(Pattern.compile("清除历史记录|Clear history"));
    BySelector check4S = By.clazz("android.widget.TextView").text(Pattern.compile("清除所有 Cookie 数据|Clear all cookie data"));
    BySelector clearAllS = By.clazz("android.widget.TextView").text(Pattern.compile("全部清除|Clear all"));
    BySelector goButtonS = By.res("com.android.browser:id/go");
    BySelector allowBtnS = By.clazz("android.widget.Button").text(Pattern.compile("允许|Allow"));
    BySelector numberS = By.res("com.android.browser:id/tabcount");
    BySelector dlUndoneS = By.clazz("android.widget.TextView").text(Pattern.compile("暂无下载任务|No download tasks"));
    BySelector dlManageS = By.clazz("android.widget.TextView").text(Pattern.compile("下载管理|Download"));
    BySelector cancelS = By.clazz("android.widget.TextView").text(Pattern.compile("取消|Cancel"));
    BySelector deAllS = By.text(Pattern.compile("全部删除|Clear all"));
    BySelector dlDoneS = By.clazz("android.widget.TextView").text(Pattern.compile("已完成|Completed"));
    BySelector curlBarS = By.clazz("android.widget.EditText");

    @Override
    public void setUp() throws Exception {
        super.setUp();
        phone.registerWatcher("browserWatcher", browserWatcher);
        phone.registerWatcher("okWatcher", okWatcher);
        UiObject2 txtTitle = phone.findObject(By.text(Pattern.compile("退出浏览器?|Exit browser?")));
        UiObject2 okButton = phone.findObject(okButtonS);
        if (txtTitle != null) {
            okButton.click();
            sleepInt(1);
        }
    }


    @Override
    public void tearDown() throws Exception {
        super.tearDown();
        phone.removeWatcher("browserWatcher");
        phone.removeWatcher("okWatcher");
        phone.removeWatcher("cacelWatcher");
        UiObject2 appTag = phone.findObject(By.clazz("android.widget.TextView").text(Pattern.compile("应用|APP")));
        UiObject2 browser = phone.findObject(By.pkg("com.android.browser"));

        if (appTag == null && browser != null) {
            UiObject2 okButton = phone.findObject(okButtonS);
            for (int i = 0; i < 10; i++) {
                if (okButton == null) {
                    press_back(1);
                } else {
                    okButton.click();
                    sleepInt(1);
                    break;
                }
            }
        }
    }


    @CaseName("Browse baidu website")
    @Test
    public void testActionBar() throws UiObjectNotFoundException, RemoteException {
        addStep("Enter into Browser");
        launchApp(AppName.Browser, IntentConstants.Browser);
        sleepInt(5);
        for (int Loop = 0; Loop < getIntParams("Loop"); Loop++) {
            System.out.println(".............looper : " + Loop);
            try {
                ActionBar();
            }catch (Exception e){
                try {
                    count ++;
                    failCount(count, getIntParams("Loop"), e.getMessage());
                    addStep("Enter into Browser");
                    launchApp(AppName.Browser, IntentConstants.Browser);
                    sleepInt(5);
                    ActionBar();
                }catch (RuntimeException re){
                    screenShot();
                    Assert.fail(re.getMessage());
                }
            }
        }
        addStep("Exit broser");
        press_back(1);
        press_center(1);
    }

    public void ActionBar() throws UiObjectNotFoundException, RemoteException{
        addStep("Open website，www.baidu.com");
        UiObject2 addressBar = phone.findObject(addressBarS);
        check("浏览器输入网址的编辑框未找到", addressBar != null);
        press_up(4);
        if(Build.VERSION.SDK_INT>20){
            callShell("input text www.baidu.com");
        }else addressBar.setText("input text www.baidu.com");

        sleepInt(1);

        addStep("Click go button");
        press_down(1);
        press_center(1);
        sleepInt(2);

        UiObject2 webView = phone.findObject(By.clazz("android.webkit.WebView"));
        sleepInt(5);
        check("can't open the website", webView != null);

        addStep("Open browser setting page");
        press_back(1);
        press_up(4);
        press_left(2);
        press_center(1);

        UiObject2 check1 = phone.findObject(check1S);
        check("open setting page", check1 != null);
        check1.click();
        sleepInt(1);

        addStep("Clear All Data");
        UiObject2 clearData = phone.findObject(clearDataS);
        check("can't find clearData option", clearData != null);
        clearData.click();
        clearData.click();
        sleepInt(1);
        UiObject2 clearAll = phone.findObject(clearAllS);
        check("not find clear all button", clearAll != null);
        clearAll.click();
        sleepInt(1);
        press_center(1);
        sleepInt(2);
        addStep("Clear web cache");
        UiObject2 check2 = phone.findObject(check2S);
        check("not clear cachedata", check2 != null);
        check2.click();
        sleepInt(1);
        press_center(1);
        sleepInt(2);
        addStep("Clear history");
        UiObject2 check3 = phone.findObject(check3S);
        check("not clear history", check3 != null);
        check3.click();
        sleepInt(1);
        press_center(1);
        sleepInt(2);
        addStep("Clear all cookie data");
        UiObject2 check4 = phone.findObject(check4S);
        check("not clear cookie", check4 != null);
        check4.click();
        sleepInt(1);
        press_center(1);
        sleepInt(2);
        addStep("Back to home page");
        press_back(1);
        sleepInt(2);
    }
    @Test
    @CaseName("Broser 浏览器新建不同标签，标签间进行切换")
    public void testLable() throws UiObjectNotFoundException, RemoteException {
        for (int Loop = 0; Loop < getIntParams("Loop"); Loop++) {
            System.out.println(".............looper : " + Loop);
            try {
                Lable();
            }catch (Exception e){
                try {
                    count ++;
                    failCount(count, getIntParams("Loop"), e.getMessage());
                    Lable();
                }catch (RuntimeException re){
                    screenShot();
                    Assert.fail(re.getMessage());
                }
            }
        }
    }

    public void Lable() throws UiObjectNotFoundException, RemoteException {
        addStep("进入浏览器,回到浏览器主页面");
        launchApp(AppName.Browser, IntentConstants.Browser);
        sleepInt(3);
        press_menu(1);
        press_up(1);
        press_center(1);
        for (int i = 0; i < 5; i++) {
            addStep("点击菜单键，查找标签按钮，进入标签页");
            int y = i + 1;
            addStep("添加" + y + "个标签");
            enterLabel();
            addStep("添加新标签");
            press_right(1);
            press_center(1);
            addStep("选择任意网址图标");
            sleepInt(2);
            UiObject2 mIcon = phone.findObject(By.clazz("android.widget.HorizontalScrollView")).getChildren().get(0).getChildren().get(1);
            check("没有找到主页中的网站图标", mIcon != null);
            mIcon.click();
            sleepInt(5);
        }

        for (int a = 0; a < 5; a++) {
            addStep("点击标签里任意标签页打开网页");
            enterLabel();
            press_left(1);
            press_center(1);
            sleepInt(5);
        }
        addStep("调出标签页，按上键关闭当前标签页");
        press_up(1);
        press_menu(1);
        UiObject2 number = phone.findObject(numberS);
        String numbers = number.getText();
        press_up(1);
        press_left(1);
        press_center(1);
        press_up(1);
        press_center(1);
        press_menu(1);
        sleepInt(1);
        UiObject2 number1 = phone.findObject(numberS);
        check("按上键未能删除标签", !numbers.equals(number1.getText()));
        press_back(1);
    }

    public void enterLabel() throws UiObjectNotFoundException {
        press_menu(1);
        UiObject2 number = waitForObj(numberS);
        check("标签个数不存在", number != null);
        String numbers = number.getText();
        System.out.print("有" + numbers + "标签");
        press_up(1);
        press_left(1);
        press_center(1);
        UiObject2 labelPage = phone.findObject(By.clazz("android.widget.Gallery"));
        check("未进入到标签页", labelPage != null);
    }

    private final UiWatcher browserWatcher = new UiWatcher() {
        public boolean checkForCondition() {
            UiObject2 exitWindows = phone.findObject(By.textContains("允许浏览器访问"));
            UiObject2 allow = phone.findObject(By.text("允许"));
            if (exitWindows != null) {
                clickAndWaitForNewWindow(allow);
                sleepInt(15);
                return true;
            } else {
                return false;
            }
        }
    };


    private final UiWatcher okWatcher = new UiWatcher() {
        public boolean checkForCondition() {
            UiObject2 fileExsit = phone.findObject(By.text(Pattern.compile(".*有任务正在下载.*|.*文件已存在.*")));
            UiObject2 okButton = phone.findObject(okButtonS);
            if (fileExsit!= null) {
                addStep("file exists");
                okButton.click();
                sleepInt(1);
                return true;
            } else {
                return false;
            }
        }
};


    @Test
    @CaseName("Download and open music file")
    public void testPlayMusic() throws UiObjectNotFoundException, RemoteException {
        addStep("Enter into browser");
        launchApp(AppName.Browser, IntentConstants.Browser);
        sleepInt(3);
        press_menu(1);
        press_up(1);
        press_center(1);
        UiObject2 homePage = waitForObj(curlBarS);
        verify("can't enter into browser home page", homePage != null);
        for (int Loop = 0; Loop < getIntParams("Loop"); Loop++) {
            System.out.println(".............looper : " + Loop);
            try {
                PlayMusic();
            }catch (Exception e){
                try {
                    count ++;
                    failCount(count, getIntParams("Loop"), e.getMessage());
                    addStep("Enter into browser");
                    launchApp(AppName.Browser, IntentConstants.Browser);
                    sleepInt(3);
                    press_menu(1);
                    press_up(1);
                    press_center(1);
                    UiObject2 homePage1 = waitForObj(curlBarS);
                    check("can't enter into browser home page", homePage1 != null);
                    PlayMusic();
                }catch (RuntimeException re){
                    screenShot();
                    Assert.fail(re.getMessage());
                }
            }
        }
        addStep("Exit browser");
        press_back(1);
        press_center(1);
    }

    public void PlayMusic() throws UiObjectNotFoundException, RemoteException {
        String musicAddress = "http://10.57.2.68/music.php";
        addStep("Open settings page of brower");
        press_menu(1);
        UiObject2 check1 = phone.findObject(check1S);
        check("open setting page", check1 != null);
        clickAndWaitForNewWindow(check1);
        sleepInt(1);

        addStep("Clear Data");
        UiObject2 clearData = phone.findObject(clearDataS);
        check("can't find clearData option", clearData != null);
        clearData.click();
        clearData.click();
        sleepInt(1);
        UiObject2 clearAll = waitForObj(clearAllS);
        check("didn't display clear all note", clearAll != null);
        clearAll.click();
        clickAndWaitForNewWindow(clearAll);
        sleepInt(1);
        UiObject2 okButton = phone.findObject(okButtonS);
        check("clear confirm button not exists", okButton != null);
        okButton.click();
        sleepInt(1);
        addStep("Back to broser home page");
        press_back(1);
        UiObject2 curlBar = phone.findObject(curlBarS);
        check("can't back to broser home page", curlBar != null);
        addStep("Enter into download page");
        press_menu(1);
        UiObject2 dlManage = waitForObj(dlManageS);
        check("can't enter into menu button", dlManage != null);
        dlManage.click();
        sleepInt(2);
        UiObject2 dlUndone = phone.findObject(dlUndoneS);
        if (dlUndone == null) {
            UiObject2 deAll = phone.findObject(deAllS);
            check("clear all button not display", deAll != null);
            deAll.click();
            sleepInt(1);
            UiObject2 okButton1 = phone.findObject(okButtonS);
            check("delete confirm button not display", okButton1 != null);
            okButton1.click();
            sleepInt(1);
        }
        press_back(1);
        UiObject2 addressBar = phone.findObject(addressBarS);
        if (addressBar != null) {
            addStep("Back to browser home page");
        } else {
            press_back(1);
        }
        UiObject2 addressBar1 = phone.findObject(addressBarS);
        check("can't back to browser home page", addressBar1 != null);
        addStep("Open website" + musicAddress);
        addressBar1.setText("http://10.57.2.68/music.php");
        sleepInt(2);
        UiObject2 goButton = waitForObj(goButtonS);
        check("can't find go to website button", goButton != null);
        goButton.click();
        sleepInt(1);
        UiObject2 cacellBar=phone.findObject(cancelS);
        if(cacellBar!=null){
            cacellBar.click();
        }
        sleepInt(3);
        press_menu(1);
        sleepInt(1);
        UiObject2 dlManage1 = phone.findObject(dlManageS);
        if (dlManage1 == null) {
            press_menu(1);
            sleepInt(2);
        }
        UiObject2 dlManage2 = phone.findObject(dlManageS);
        check("Menu page not opened", dlManage2 != null);
        dlManage2.click();
        sleepInt(1);
        press_center(1);
        UiObject2 mp3 = phone.findObject(By.clazz("android.widget.TextView").text("music.mp3"));
        check("downloaded music didn't exists", mp3 != null);
        press_center(1);
        addStep("Play the downloaded music");
        UiObject2 openWith = waitForObj(By.text(Pattern.compile("打开方式|使用音乐打开|仅此一次")));
        if (openWith != null) {
            UiObject2 music = waitForObj(By.text("音乐"));
            if (music != null) {
                check("打开方式中没有音乐选项", music != null);
                music.click();
            }
            sleepInt(1);
            UiObject2 onceOnly = waitForObj(By.text("仅此一次"));
            check("打开方式中没有音乐选项", onceOnly != null);
            onceOnly.click();
            sleepInt(1);
        }
        sleepInt(10);
        addStep("Exit music player");
        press_back(1);
        UiObject2 addressBar2 = phone.findObject(addressBarS);
        if (addressBar2 == null) {
            addStep("Back  to brower home page");
            press_back(1);
        }
    }

    @Test
    @CaseName("Download and open picture")
    public void testDownloadPicture() throws UiObjectNotFoundException, RemoteException {
        addStep("Enter into browser");
        launchApp(AppName.Browser, IntentConstants.Browser);
        press_menu(1);
        press_up(1);
        press_center(1);
        UiObject2 curlBar = phone.findObject(curlBarS);
        verify("can't back to browser home page", curlBar != null);
        for (int Loop = 0; Loop < getIntParams("Loop"); Loop++) {
            System.out.println(".............looper : " + Loop);
            try {
                DownloadPicture();
            }catch (Exception e){
                try {
                    count ++;
                    failCount(count, getIntParams("Loop"), e.getMessage());
                    addStep("Enter into browser");
                    launchApp(AppName.Browser, IntentConstants.Browser);
                    press_menu(1);
                    press_up(1);
                    press_center(1);
                    UiObject2 curlBar1 = phone.findObject(curlBarS);
                    check("can't back to browser home page", curlBar1 != null);
                    DownloadPicture();
                }catch (RuntimeException re){
                    screenShot();
                    Assert.fail(re.getMessage());
                }
            }
        }

        addStep("退出浏览器");
        press_back(2);
        press_center(1);
    }

    public void DownloadPicture() throws UiObjectNotFoundException, RemoteException {
        String pictAddress = "http://10.57.2.68/picture.php";
        addStep("Open settings page of brower");
        press_menu(1);
        UiObject2 check1 = phone.findObject(check1S);
        check("open setting page", check1 != null);
        clickAndWaitForNewWindow(check1);
        sleepInt(1);
        addStep("Clear Data");
        UiObject2 clearData = phone.findObject(clearDataS);
        check("can't find clearData option", clearData != null);
        clearData.click();
        clearData.click();
        sleepInt(1);
        UiObject2 clearAll = phone.findObject(clearAllS);
        check("didn't display clear all note", clearAll != null);
        clearAll.click();
        clearAll.click();
        sleepInt(1);
        UiObject2 okButton = phone.findObject(okButtonS);
        check("delete confirm button not display", okButton != null);
        okButton.click();
        sleepInt(1);
        addStep("清除数据后返回浏览器主页");
        press_back(1);
        addStep("点击菜单查看下载中是否有下载任务");
        press_menu(1);
        UiObject2 dlManage2 = waitForObj(dlManageS);
        check("未能打开菜单界面", dlManage2 != null);
        clickAndWaitForNewWindow(dlManage2);
        UiObject2 localPlay = phone.findObject(By.text("本地播放器"));
        sleepInt(2);
        if (localPlay != null) {
            press_back(1);
        }

        UiObject2 dlAll = phone.findObject(deAllS);
        if (dlAll.isEnabled()) {
            dlAll.click();
            sleepInt(1);
            UiObject2 okButton1 = phone.findObject(okButtonS);
            check("未能弹出删除确认按钮", okButton1 != null);
            okButton1.click();
            sleepInt(2);
        }
        UiObject2 dlUndone = phone.findObject(dlUndoneS);
        check("未能弹出删除确认按钮", dlUndone != null);
        addStep("返回浏览器主界面");
        press_back(1);
        UiObject2 curlBar1 = phone.findObject(curlBarS);
        check("未能返回到浏览器主界面", curlBar1 != null);
        addStep("打开网址" + pictAddress);
        curlBar1.setText("http://10.57.2.68/picture.php");
        sleepInt(1);
        UiObject2 goButton = waitForObj(goButtonS);
        check("未发现go按钮", goButton != null);
        goButton.click();
        sleepInt(1);
        UiObject2 cacellBar=phone.findObject(cancelS);
        if(cacellBar!=null){
            cacellBar.click();
        }
        sleepInt(3);
        press_menu(1);
        sleepInt(1);
        UiObject2 dlManage1 = phone.findObject(dlManageS);
        if (dlManage1 == null) {
            press_menu(1);
            sleepInt(2);
        }
        UiObject2 dlManage = phone.findObject(dlManageS);
        check("未进入到菜单界面", dlManage != null);
        dlManage.click();
        check("未进入到下载管理界面", dlManage != null);
        UiObject2 dlDone = phone.findObject(dlDoneS);
        check("已完成不存在", dlDone != null);
        dlDone.click();
        sleepInt(2);

        addStep("打开图片");
        UiObject2 openWith = waitForObj(By.text(Pattern.compile("打开方式|使用.*打开|仅此一次")));
        if (openWith != null) {
            UiObject2 gallery = waitForObj(By.text("相册"));
            if (gallery != null) {
                check("打开方式中没有音乐选项", gallery != null);
                gallery.click();
            }
            sleepInt(1);
            UiObject2 onceOnly = waitForObj(By.text("仅此一次"));
            check("打开方式中没有音乐选项", onceOnly != null);
            onceOnly.click();
            sleepInt(1);
        }
        UiObject2 gallery = waitForObj(By.pkg("com.android.gallery3d"));
        check("未能正常播放图片", gallery != null);
        addStep("退出图片");
        for(int i=0;i<3;i++){
            UiObject2 addressBar2 = phone.findObject(addressBarS);
            if(addressBar2==null){
                press_right(1);
                press_back(1);
            }else break;
        }
        UiObject2 addressBar1 = waitForObj(addressBarS);
        check("未能返回浏览器主界面", addressBar1 != null);
    }

    @Test
    @CaseName("下载视频文件并打开")
    public void testPlayVideo() throws UiObjectNotFoundException, RemoteException {
        addStep("打开浏览器");
        launchApp(AppName.Browser, IntentConstants.Browser);
        press_menu(1);
        press_up(1);
        press_center(1);
        UiObject2 homePage = waitForObj(curlBarS);
        verify("未能进入浏览器主界面", homePage != null);
        for (int Loop = 0; Loop < getIntParams("Loop"); Loop++) {
            System.out.println(".............looper : " + Loop);
            try {
                PlayVideo();
            }catch (Exception e){
                try {
                    count ++;
                    failCount(count, Loop, e.getMessage());
                    addStep("打开浏览器");
                    launchApp(AppName.Browser, IntentConstants.Browser);
                    press_menu(1);
                    press_up(1);
                    press_center(1);
                    UiObject2 homePage1 = waitForObj(curlBarS);
                    check("未能进入浏览器主界面", homePage1 != null);
                    PlayVideo();
                }catch (RuntimeException re){
                    screenShot();
                    Assert.fail(re.getMessage());
                }
            }
        }
        addStep("退出浏览器");
        press_back(1);
        press_center(1);
    }

    public void PlayVideo() throws UiObjectNotFoundException, RemoteException {
        String videoAddress = "http://10.57.2.68/video.php";
        addStep("打开设置页面");
        addStep("打开设置页面");
        press_menu(1);
        UiObject2 check1 = waitForObj(check1S);
        check("open setting page", check1 != null);
        clickAndWaitForNewWindow(check1);
        sleepInt(1);
        addStep("清除数据");
        UiObject2 clearData = waitForObj(clearDataS);
        check("can't find clearData option", clearData != null);
        clearData.click();
        clearData.click();
        sleepInt(1);
        UiObject2 clearAll1 = waitForObj(clearAllS);
        check("没有打开数据清理项", clearAll1 != null);
        clearAll1.click();
        clearAll1.click();
        sleepInt(1);
        addStep("确认清除数据");
        UiObject2 okButton = waitForObj(okButtonS);
        check("确认清楚按钮不存在", okButton != null);
        okButton.click();
        sleepInt(1);
        addStep("清除数据后返回浏览器主页");
        press_back(1);
        sleepInt(2);
        UiObject2 curlBar1 = phone.findObject(curlBarS);
        if(curlBar1==null){
            press_back(1);
        }
        UiObject2 curlBar = waitForObj(curlBarS);
        check("未能返回到浏览器网页界面", curlBar != null);
        addStep("进入下载页面，无下载任务则退出");
        press_menu(1);
        UiObject2 dlManage = waitForObj(dlManageS);
        check("未能点进菜单按钮", dlManage != null);
        dlManage.click();
        sleepInt(2);
        UiObject2 localPlayer = phone.findObject(By.text("本地播放器"));
        if (localPlayer != null) {
            press_back(1);
        }
        UiObject2 dlAll = phone.findObject(deAllS);
        if (dlAll.isEnabled()) {
            dlAll.click();
            sleepInt(1);
            UiObject2 okButton1 = phone.findObject(okButtonS);
            check("未能弹出删除确认按钮", okButton1 != null);
            okButton1.click();
            sleepInt(2);
        }
        UiObject2 dlUndone = waitForObj(dlUndoneS);
        check("未能弹出删除确认按钮", dlUndone != null);
        addStep("返回浏览器主界面");
        press_back(1);
        UiObject2 addressBar = waitForObj(addressBarS);
        check("未能返回到浏览器主界面", addressBar != null);
        addStep("打开网址" + videoAddress);
        addressBar.setText("http://10.57.2.68/video.php");
        sleepInt(1);
        UiObject2 goButton = waitForObj(goButtonS);
        check("未发现go按钮", goButton != null);
        goButton.click();
        sleepInt(2);
        UiObject2 cacellBar=phone.findObject(cancelS);
        if(cacellBar!=null){
            cacellBar.click();
            UiObject2 cacellBar1=phone.findObject(cancelS);
            if(cacellBar1!=null)cacellBar1.click();
        }
        sleepInt(30);
        press_menu(1);
        UiObject2 dlManage3 = phone.findObject(dlManageS);
        if (dlManage3 == null) {
            press_menu(1);
        }
        UiObject2 dlManage1 = phone.findObject(dlManageS);
        check("未能打开菜单界面", dlManage1 != null);
        dlManage1.click();
        sleepInt(1);
        UiObject2 dlManage2 = waitForObj(By.text(Pattern.compile("下载管理|Download manager")));
        check("未进入到下载管理界面", dlManage2 != null);
        sleepInt(20);
        UiObject2 dlDone = waitForObj(dlDoneS);
        check("已完成不存在", dlDone != null);
        dlDone.click();
        sleepInt(1);
        addStep("打开文件播放视频");
        UiObject2 openWith = waitForObj(By.text(Pattern.compile("打开方式|使用.*打开|仅此一次")));
        if (openWith != null) {
            UiObject2 video = waitForObj(By.text("播放器"));
            if (video != null) {
                check("打开方式中没有播放器选项", video != null);
                video.click();
            }
            sleepInt(1);
            UiObject2 onceOnly = waitForObj(By.text("仅此一次"));
            check("打开方式中没有仅此一次选项", onceOnly != null);
            onceOnly.click();
            sleepInt(5);
        }
        sleepInt(10);
        addStep("退出视频播放");
        press_back(2);
        UiObject2 addressBar1=waitForObj(addressBarS);
        check("未能返回浏览器首页", addressBar1 != null);
    }
}