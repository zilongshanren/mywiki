---
title: Cocos2d-x 3.0rc0集成Google AdMob SDK
url: https://tonybai.com/2014/05/01/integrate-cocos2dx3rc0-with-admob/
published: '2014-05-01'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Cocos2d-x 3.0rc0集成Google AdMob SDK

话说[Cocos2d-x](http://www.cocos2d-x.org) 3.0上一周迫不及待地发布了[正式版](http://www.cocos2d-x.org/news/215)，本是一件值得庆幸的事情。但由于不可解决的[技术问题](http://www.cocos2d-x.org/forums/6/topics/48163)，引擎无奈将Android平台的NativeActivity 实现重新[回退](http://tonybai.com/2014/04/23/changes-in-cocos2dx-3-rc2-for-android/)到了Cocos2d-x 2.2.x版本的实现方案。由于之前已经将 GameDemo移植到了[Cocos2d-x 3.0rc0版](http://tonybai.com/2014/04/22/hello-cocos2dx-3-rc0/)，直观感受到了NativeActivity方案带来的游戏操作体验上的提升（触屏事件的响应），因此心里总是“挂念”引擎的 NativeActivity方案。按照Cocos2d-x官方人士的说法，只要NDK的问题修复，NativeActivity还是未来引擎在 Android平台上的第一选择。我的理解，将来Cocos2d-x的某个版本中还会恢复NativeActivity的实现方案。

上次只是将GameDemo的核心逻辑移植到了Cocos2d-x 3.0rc0上，但一些外部SDK集成尚未做完，这两天闲遐时开始着手研究如何做，而首先要移植的就是[Google AdMob SDK](https://developers.google.com/mobile-ads-sdk/)。关于Cocos2d-x 3.0rc0集成Google AdMob SDK，网上已经有了技术方案原型，最初应该是一个[外国开发者提出的方案](http://www.dynadream.com/ddweb/index.php/Special_Blog)，后来被[CocoaChina](http://www.cocoachina.com) cocos2d-x社区版主翻译成了[中文教程](http://www.cocoachina.com/bbs/read.php?tid=194999)，这里基本上也是参考的这个方案，只是做了局部细化和进一步说明，希望能帮助大家进一步解惑。

**一、功能说明**

GameDemo游戏分为三个场景：WelcomeScene、GameScene以及EndScene。集成AdMob SDK的功能要求如下：

– 当游戏进入到WelcomeScene时，AdMob SDK完成初始化，发出Ad Request，当收到Ad的时候才会在屏幕上方显示带有Ad的窗口；

– 当点击**Start**进入到GameScene时，隐藏Ad窗口，以不干扰玩家的游戏操作为优先；

– 当游戏Over进入到EndScene的时候，恢复显示Ad窗口；

– 当玩家点击“**Retry**”回到GameScene时，隐藏Ad窗口。

**二、方案原理**

这个方案就是通过android.widget.PopupWindow实现广告窗口悬浮在当前窗口之上。按照Android[官方Doc](http://developer.android.com/reference/android/widget/PopupWindow.html)中的说 明，PopupWindow用于实现一个弹出框，它可以使用任意布局的View作为其内容，这个弹出框是悬浮在当前activity之上的。

至于PopupWindow为何能显示在当前Activity之上，可以查看PopupWindow的源码，大致思路就是PopupWindow通过 new时传入的context(当前Activity)获得了当前WindowManager，并将AdView作为子View添加到该窗口中。这里简要列出一些关键源码，大家可粗略理解一下：

public PopupWindow(Context context, AttributeSet attrs,

int defStyleAttr, int defStyleRes) {

mContext = context;

**mWindowManager** = (WindowManager)context

.getSystemService(Context.WINDOW_SERVICE);

…. …

}

public void setContentView(View contentView) {

if (isShowing()) {

return;

}

**mContentView** = contentView;

if (mContext == null && mContentView != null) {

mContext = mContentView.getContext();

}

if (mWindowManager == null && mContentView != null) {

mWindowManager = (WindowManager) mContext

.getSystemService(Context.WINDOW_SERVICE);

}

}

public void showAtLocation(View parent, int gravity, int x, int y) {

showAtLocation(parent.getWindowToken(), gravity, x, y);

}

public void showAtLocation(IBinder token, int gravity, int x, int y) {

if (isShowing() || mContentView == null) {

return;

}

unregisterForScrollChanged();

mIsShowing = true;

mIsDropdown = false;

WindowManager.LayoutParams p = createPopupLayout(token);

p.windowAnimations = computeAnimationResource();


**preparePopup**(p);

if (gravity == Gravity.NO_GRAVITY) {

gravity = Gravity.TOP | Gravity.START;

}

p.gravity = gravity;

p.x = x;

p.y = y;

if (mHeightMode < 0) p.height = mLastHeight = mHeightMode;

if (mWidthMode < 0) p.width = mLastWidth = mWidthMode;

**invokePopup**(p);

}


private void invokePopup(WindowManager.LayoutParams p) {

if (mContext != null) {

p.packageName = mContext.getPackageName();

}

mPopupView.setFitsSystemWindows(mLayoutInsetDecor);

setLayoutDirectionFromAnchor();

**mWindowManager.addView(mPopupView, p);**

}

UI线程负责更新窗口，因此popupWindow的创建与操作都应该通过runOnUiThread传递给UI线程执行。

游戏逻辑的C++层代码通过Jni控制PopupWindow的Show和dismiss。别忘了C++层的代码是在渲染线程执行的哦，这也是为何要用handler和runOnUIThread的原因。

在Cocos2d-x 2.2.2版本集成AdMob时，AdMob只是在收到ad后才显示出广告Banner，但是在cocos2d-x 3.0rc0中，当广告加载未成功时，android.widget.PopupWindow会显示一个小黑框，特难看，因此我们需要自己来控制。

**三、集成步骤**

【AdMob准备】

到Google AdMob注册一个帐号，如果你有Google帐号，那直接开通AdMob（需填写更加详细的信息）。

下载Google AdMob SDK，之前一直用GoogleAdMobAdsSdk-6.4.1.jar，这里还以这个版本为例。但Google官方已经不推荐这个版本了，你可以下 载Google Play Services版本的Mobile Ads API，但代码与这里会稍有不同。将下载的jar包放到GameDemo/proj.android/libs中。


【修改AndroidManifest.xml】

在<Application>标签里添加：

<activity

android:name="com.google.ads.AdActivity"

android:configChanges="keyboard|keyboardHidden|orientation|screenLayout|uiMode|screenSize|smallestScreenSize" />

<meta-data

android:name="ADMOB_PUBLISHER_ID"

android:value="*YOUR_PUBLISHER_ID_VALUE*" />

权限方面至少包含如下两个：

<uses-permission android:name="android.permission.INTERNET"/>

<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>

**【Java层代码集成】**

我们只需要修改GameDemoActivity.java这个文件。

import android.app.NativeActivity;

import android.os.Bundle;

import android.util.Log;

import android.os.Handler;

import android.os.Message;

import android.view.Gravity;

import android.view.View;

import android.view.Gravity;

import android.view.ViewGroup.LayoutParams;

import android.view.ViewGroup.MarginLayoutParams;

import android.view.WindowManager;

import android.widget.LinearLayout;

import android.widget.PopupWindow;

import com.google.ads.AdRequest;

import com.google.ads.AdSize;

import com.google.ads.AdView;

import com.google.ads.AdListener;

import com.google.ads.Ad;

public class GameDemoActivity extends NativeActivity{

private static GameDemoActivity context;

private AdView adView;

private PopupWindow popUpWindow;

private LinearLayout popupWindowLayout;

private LinearLayout mainActivityLayout;

private boolean hasAdReceived;

private static Handler adHandler = new Handler() {

public void handleMessage(Message msg) {

if (!context.hasAdReceived)

return;

switch (msg.what) {

case 0:

if (View.VISIBLE ==

context.adView.getVisibility()) {

context.adView.setVisibility(View.GONE);

context.popUpWindow.dismiss();

}

break;

case 1:

if (View.VISIBLE !=

context.adView.getVisibility()) {

context.adView.setVisibility(View.VISIBLE);

context.popUpWindow.showAtLocation(

context.mainActivityLayout, Gravity.TOP, 0, 0);

}

break;

}

}

};

@Override

protected void onCreate(Bundle savedInstanceState) {

super.onCreate(savedInstanceState);

getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);

context = this;

adView = new AdView(this, AdSize.BANNER, "a1533d6de900e31");

adView.setAdListener(new AdmobListener());

//初始时，广告View隐藏起来

adView.setVisibility(View.GONE);

}

public static void setupAds(){

context.initAdPopupWindow();

}

public void initAdPopupWindow() {

if (adView != null) {

context.runOnUiThread(new Runnable() {

@Override

public void run() {

MarginLayoutParams params = new MarginLayoutParams(

LayoutParams.WRAP_CONTENT,

LayoutParams.WRAP_CONTENT);

params.setMargins(0, 0, 0, 0);

popupWindowLayout = new LinearLayout(context);

popupWindowLayout.setPadding(-5, -5, -5, -5);

popupWindowLayout.setOrientation(LinearLayout.VERTICAL);

popupWindowLayout.**addView**(adView, params);

popUpWindow = new PopupWindow(context);

popUpWindow.setWidth(320);

popUpWindow.setHeight(50);

popUpWindow.setWindowLayoutMode(LayoutParams.WRAP_CONTENT,

LayoutParams.WRAP_CONTENT);

popUpWindow.setClippingEnabled(false);

popUpWindow.**setContentView**(popupWindowLayout);

mainActivityLayout = new LinearLayout(context);

context.**setContentView**(mainActivityLayout, params);

context.hasAdReceived = false;

AdRequest adRequest = new AdRequest();

//测试Admob时使用测试Device，发布版需要去掉这行代码

adRequest.addTestDevice("CCE4220B2509A406B515E7C9A205AEE1");

context.adView.loadAd(adRequest);

popUpWindow.update();

}

});

}

}

//GoogleAdMobAdsSdk-6.4.1版本中的AdListener是interface，因此

//我们需要override所有接口，但只有onReceiveAd是我们关心的。

private class AdmobListener implements AdListener {

@Override

public void onReceiveAd(Ad ad) {

//只有第一次成功接收Ad后，我们后续才显示广告窗口，否则

//popupWindow会显示为一个小黑框，特难看。

Log.d("GameDemo", "onReceiveAd");

if (!hasAdReceived){

hasAdReceived = true;

}

}

@Override

public void onFailedToReceiveAd(Ad ad,

AdRequest.ErrorCode error) {

Log.d("GameDemo",

"failed to receive ad (" + error+ ")");

}

@Override

public void onPresentScreen(Ad ad) {

Log.d("GameDemo", "onPresentScreen");

}

@Override

public void onDismissScreen(Ad ad) {

Log.d("GameDemo", "onDismisScreen");

}

@Override

public void onLeaveApplication(Ad ad) {

Log.d("GameDemo", "onLeaveApp");

}

}

public static void setAdVisible(boolean b) {

Message msg = new Message();

if (b) {

msg.what = 1;

} else {

msg.what = 0;

}

adHandler.sendMessage(msg);

}

}

【C++层代码集成】

在AppDelegate.cpp中添加setupAds方法：

void AppDelegate::setupAds()

{

#if (CC_TARGET_PLATFORM == CC_PLATFORM_ANDROID)

JniMethodInfo t;

if (JniHelper::getStaticMethodInfo(t, "com/tonybai/game/GameDemoActivity", "setupAds", "()V")) {

t.env->CallStaticVoidMethod(t.classID, t.methodID);

if (t.env->ExceptionOccurred()) {

t.env->ExceptionDescribe();

t.env->ExceptionClear();

return;

}

t.env->DeleteLocalRef(t.classID);

}

#endif

}

在WelcomeScene的init方法中调用setupAds：

bool WelcomeScene::init()

{

bool bRet = false;

do {

… …

AppDelegate *app = (AppDelegate*)Application::getInstance();

app->**setupAds**();

bRet=true;

} while(0);

return bRet;

}

在点击Start按钮时，隐藏Ad：

void WelcomeScene::menuStartCallback(Ref* pSender)

{

AppDelegate *app = (AppDelegate*)Application::getInstance();

**app->setAdVisible(false);**

GameScene *gameScene = GameScene::create();

Director::getInstance()->replaceScene(gameScene);

}

集成步骤到此就结束了，编译ok就可以部署到模拟器上运行测试一番了。

**四、使用Cocos2d-x 3.0rc0引擎遇到的两个问题**

【问题1】用cocos2d-x 3.0rc0的cocos编译高版本引擎生成的工程遇到的问题

cocos2d-x 3.0rc0生成的proj.android/build-cfg.json与高版本(rc1～正式版) cocos生成的工程的build-cfg.json稍有不同，用cocos2d-x 3.0rc0版cocos编译高版本cocos生成的project，会提示build_android组件无法找到“copy_to_assets”。 因此需要手动修改proj.android/build-cfg.json，将其中的：

"copy_resources": [

{

"from": "../Resources",

"to": ""

}

],

改为：

"copy_to_assets" :[

"../Resources/"

],

【问题2】 W/dalvikvm(1194): dvmFindClassByName rejecting 'org/cocos2dx/lib/Cocos2dxHelper'

使用cocos2d-x 3.0rc0编译的项目，总是出现如下问题，但似乎这个错误还不影响程序的运行：

04-29 09:44:34.968: D/JniHelper(1194): JniHelper::setJavaVM(0xb8835730), pthread_self() = B897B518

04-29 09:44:34.968: W/dalvikvm(1194): dvmFindClassByName rejecting 'org/cocos2dx/lib/Cocos2dxHelper'

Google了一下，这个问题很多童鞋都遇到了，但给出的solution却不甚令我满意，于是我就求甚解的细致挖掘了一下，终于找到了一个让我还算满意 的答案。我们分析一下这两条日志，rejecting那条日志总是伴随setJavaVM后面出现的。可引擎什么时候setJavaVM了呢？显然是在 native_app_glue创建的子进程中，引擎需要attachCurrentThread，获得JniEnv时才做的。于是我们打开cocos2d-x-3.0rc0/cocos/2d/platform/android/nativeactivity.cpp一看究竟。

在nativeactivity.cpp中有两处"org/cocos2dx/lib/Cocos2dxHelper"，我们先看engine_handle_cmd中的那处：

static void engine_handle_cmd(struct android_app* app, int32_t cmd)

{

…. ….

case APP_CMD_INIT_WINDOW:

LOG_RENDER_DEBUG("android_main : APP_CMD_INIT_WINDOW");

// The window is being shown, get it ready.

if (engine->app->window != NULL) {

cocos_dimensions d = engine_init_display(engine);

if ((d.w > 0) &&

(d.h > 0)) {

**cocos2d::JniHelper::setJavaVM(app->activity->vm);**

cocos2d::JniHelper::setClassLoaderFrom(app->activity->clazz);

// call Cocos2dxHelper.init()

cocos2d::JniMethodInfo ccxhelperInit;

if (!cocos2d::JniHelper::getStaticMethodInfo(ccxhelperInit,

"**org/cocos2dx/lib/Cocos2dxHelper**",

"init",

"(Landroid/app/Activity;)V")) {

LOGI("cocos2d::JniHelper::getStaticMethodInfo(ccxhelperInit) FAILED");

}

ccxhelperInit.env->CallStaticVoidMethod(ccxhelperInit.classID,

ccxhelperInit.methodID,

app->activity->clazz);

cocos_init(d, app);

}

engine->animating = 1;

engine_draw_frame(engine);

}

break;

… …

}

初步可以断定，那两条日志就是执行到这里输出的，但为何dvmFindClassByName方法会rejecting “org/cocos2dx/lib/Cocos2dxHelper”这个类名呢？我们还得翻看dalvik虚拟机源码：

/dalvik/vm/native/InternalNative.cpp

/*

* Find a class by name, initializing it if requested.

*/

ClassObject* dvmFindClassByName(StringObject* nameObj, Object* loader,

bool doInit)

{

ClassObject* clazz = NULL;

char* name = NULL;

char* descriptor = NULL;

if (nameObj == NULL) {

dvmThrowNullPointerException("name == null");

goto bail;

}

name = dvmCreateCstrFromString(nameObj);

/*

* We need to validate and convert the name (from x.y.z to x/y/z). This

* is especially handy for array types, since we want to avoid

* auto-generating bogus array classes.

*/

if (!dexIsValidClassName(name, true)) {

**ALOGW("dvmFindClassByName rejecting '%s'", name);**

dvmThrowClassNotFoundException(name);

goto bail;

}

… …

}

我们的确找到了输出rejecting日志的地方，通过注释我们可以看到这个方法是用来验证名字对象，并将x.y.z形式的名字转换成x/y/z的。但引 擎中传入的就是“x/y/z”格式，因此这个方法输出了错误日志。我尝试将上面engine_handle_cmd中的"org/cocos2dx/lib/Cocos2dxHelper"改成"org.cocos2dx.lib.Cocos2dxHelper"，错误日志果然消失了。

不过目前仍不能解释一点：为何在其他位置，比如在前面的AppDelegate::setupAds中，使用x/y/z格式的jni调用参数却没有输出错误日志！难道两个位置dalvik虚拟机使用的是不同的名字对象查找和加载方法？这个目前尚无定论。

© 2014, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

大哥请教下如何把广告放在底部？

感谢楼主的分享。楼主不妨了解下keymob平台吧。keymob平台具有详细的数据统计，高效与专业的服务，以及丰富的广告资源与不断更新的广告形式。想了解更多的特色功能登入www.keymob.com