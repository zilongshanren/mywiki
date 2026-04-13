---
title: Cocos2d-x 3.0rc2集成ShareSDK
url: https://tonybai.com/2014/04/25/integrate-cocos2dx3rc2-with-sharesdk/
published: '2014-04-25'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Cocos2d-x 3.0rc2集成ShareSDK

给自己的手机游戏增加些社交分享功能，有助于游戏宣传和提升知名度，是一种不错的社交营销手段。国内这方面的第三方插件有不少，比如[ShareSDK](http://sharesdk.cn)、[友 盟分享组件](http://www.umeng.com/component_social)、[Baidu分享组件](http://developer.baidu.com/soc/share)等，之前在研究[2.2.2版本](http://tonybai.com/2014/03/11/hello-cocos2dx/)时，[集成了ShareSDK](http://tonybai.com/2014/04/17/a-bug-from-sharesdk-componet-for-cocos2dx/)这个组件，这次迁移到[Cocos2d-x 3.0rc2](http://tonybai.com/2014/04/23/changes-in-cocos2dx-3-rc2-for-android/)依旧选择集成ShareSDK，这里就来说说集成的过程，遇到的一些问题以及解决方法。这里仅以Android平台游戏集成为例。

**一、功能描述、****SDK版本和帐号准备**

功能大致是这样的：在游戏中设置一个按钮，点击这个按钮，弹出知名社交平台的分享图标集窗口，用户选择分享目标后，相关信息分享到对应的社交平台。分享结果通知通过Toast显示在屏幕的下方。

这次依旧使用ShareSDK for Android 2.3.7版本（ShareSDK-Android-2.3.7），Cocos2d-x的版本为[3.0rc2](http://www.cocos2d-x.org)。

集成前，你需要有一个基于Cocos2d-x 3.0rc2的可运行的Android平台游戏project，我们的集成就基于该project，这里我们的project名为GameDemo，GameDemo的源码结构大致是：

GameDemo/

– Classes/

– proj.android/

– Resources/

– cocos2d/

– CMakeLists.txt

– … …

使用ShareSDK前，你需要在各大主流社交平台（[微信](http://open.weixin.qq.com/)、[微博](http://open.weibo.com)）申请开发者帐号以及游戏接入权限(app_key、app_secret)等，当然在ShareSDK站点也应该有自己的帐号和应用AppKey，这些申请的审核需要几个工作日，甚至更长。

**二、ShareSDK集成步骤**

按照ShareSDK官方manual说法，Cocos2d-x集成ShareSDK有三种方式，之前在Cocos2d-x 2.2.2引擎中采用的是专用组件集成的方式，该组件(C2DXShareSDKSample)可以在[这里](https://github.com/ShareSDKPlatform/C2DXShareSDKSample)下载（该组件近期已经fix了[我之前发现的bug](http://tonybai.com/2014/04/17/a-bug-from-sharesdk-componet-for-cocos2dx/)）。

**1. jar包集成**

这次我们主要做微博、微信的社交分享，因此只需要微博、微信相关jar包。在C2DXShareSDKSample/proj.android/libs下，我们找到以下几个jar包：

-rw-rw-r– 1 tonybai tonybai 97K 4月 8 18:10 mframework.jar

-rw-rw-r– 1 tonybai tonybai 112K 4月 8 17:39 ShareSDK-Core-2.3.7.jar

-rw-rw-r– 1 tonybai tonybai 19K 4月 8 17:39 ShareSDK-SinaWeibo-2.3.7.jar

-rw-rw-r– 1 tonybai tonybai 4.3K 4月 8 17:39 ShareSDK-Wechat-2.3.7.jar

-rw-rw-r– 1 tonybai tonybai 29K 4月 8 17:39 ShareSDK-Wechat-Core-2.3.7.jar

-rw-rw-r– 1 tonybai tonybai 4.6K 4月 8 17:39 ShareSDK-Wechat-Favorite-2.3.7.jar

-rw-rw-r– 1 tonybai tonybai 4.4K 4月 8 17:39 ShareSDK-Wechat-Moments-2.3.7.jar

把这些jar包文件Copy到GameDemo/proj.android/libs下。

**2. 配置文件与资源部分集成**

修改GameDemo/proj.android/AndroidManifest.xml文件，在application标签下，添加如下Activity标签：

<activity

android:name="cn.sharesdk.framework.ShareSDKUIShell"

android:configChanges="keyboardHidden|orientation|screenSize"

android:screenOrientation="portrait"

android:theme="@android:style/Theme.Translucent.NoTitleBar"

android:windowSoftInputMode="stateHidden|adjustResize" >

</activity>

<activity

android:name=".wxapi.WXEntryActivity"

android:configChanges="keyboardHidden|orientation|screenSize"

android:exported="true"

android:screenOrientation="portrait"

android:theme="@android:style/Theme.Translucent.NoTitleBar" />

将C2DXShareSDKSample/proj.android/res下的如下目录中的文件复制到GameDemo/proj.android/res下：

drawable-hdpi/ drawable-ldpi/ drawable-mdpi/

drawable-xhdpi/ layout/ values/ values-en/

注意，类似icon.png这种文件就不要复制了，自己做一下判断就好。

**3. C++部分代码集成**

将C2DXShareSDKSample/Classes下的C2DXShareSDK文件夹Copy到GameDemo/Classes下面。

由于Cocos2d-x 3.0rc2的类命名发生了变化，我们需要对C2DXShareSDK中使用到的引擎中的类名以及方法名进行修改。但实际上Cocos2d-x 3.0rc2考虑到了一些兼容性的问题，大部分名字通过cocos2d/cocos/deprecated/CCDeprecated.h中定义的typedef得以保留，虽然这些名字已经被建议deprecated了。rc2中CCObject被改名为Ref了，这个我们需要手工在C2DXShareSDK进行修改。

另外ShareSDK组件在实现时大量使用了CCDictionary、CCArray和CCString，而这三个类在Cocos2d-x 3.0rc2中均被deprecated了，但我们依然可以使用，所以我们可以不做修改。但以后随着cocos2d-x版本的演进，这些类很可能被彻底移除出引擎，我们就需要重新使用其替代品进行实现了。

此外我们还需要手工修改一下C2DXShareSDK/Android/JSON/CCJSONConverter.cpp文件中的getObjJson方 法，因为rc2中CCDictionary、CCString、CCArray这些类的真实名称都已经换成了__Dictionary、__String 和__Array，CCDictionary、CCString、CCArray只是些typedef，因此要像下面这样做些修改(如果你是集成 cocos2d-x 2.x.x版本，则无需做下面修改)：

cJSON * CCJSONConverter::getObjJson(Ref * obj)

{

std::string s = typeid(*obj).name();

if(s.find("**__Dictionary**")!=std::string::npos){

cJSON * json = cJSON_CreateObject();

convertDictionaryToJson((CCDictionary *)obj, json);

return json;

}else if(s.find("**__Array**")!=std::string::npos){

cJSON * json = cJSON_CreateArray();

convertArrayToJson((CCArray *)obj, json);

return json;

}else if(s.find("**__String**")!=std::string::npos){

CCString * s = (CCString *)obj;

cJSON * json = cJSON_CreateString(s->getCString());

return json;

}else if(s.find("**CCNumber**")!=std::string::npos){

CCNumber * n = (CCNumber *)obj;

cJSON * json = cJSON_CreateNumber(n->getDoubleValue());

return json;

}else if(s.find("**CCNull**")!=std::string::npos){

cJSON * json = cJSON_CreateNull();

return json;

}

CCLog("CCJSONConverter encountered an unrecognized type");

return NULL;

}

CCNumber和CCNull是ShareSDK组件自己实现的类名，这里无需修改。

接下来我们需要在AppDelegate.cpp中对ShareSDK做初始化了：

bool AppDelegate::applicationDidFinishLaunching() {

… …

initShareSDK();

… ..

}

void AppDelegate::initShareSDK()

{

// sina weibo

CCDictionary *sinaConfigDict = CCDictionary::create();

sinaConfigDict->setObject(CCString::create("*YOUR_WEIBO_APPKEY*"), "app_key");

sinaConfigDict->setObject(CCString::create("*YOUR_WEBIO_APPSECRET*"), "app_secret");

sinaConfigDict->setObject(CCString::create("http://www.sharesdk.cn"), "redirect_uri");

C2DXShareSDK::setPlatformConfig(C2DXPlatTypeSinaWeibo, sinaConfigDict);

// wechat

CCDictionary *wcConfigDict = CCDictionary::create();

wcConfigDict->setObject(CCString::create("*YOUR_WECHAT_APPID*"), "app_id");

C2DXShareSDK::setPlatformConfig(C2DXPlatTypeWeixiSession, wcConfigDict);

C2DXShareSDK::setPlatformConfig(C2DXPlatTypeWeixiTimeline, wcConfigDict);

C2DXShareSDK::setPlatformConfig(C2DXPlatTypeWeixiFav, wcConfigDict);

C2DXShareSDK::open(CCString::create("YOUR_SHARESDK_APPKEY"), false);

}

在Share按钮的事件回调函数中调用ShareSDK的接口进行社交平台分享：

void GameScene::menuShareCallback(Ref* sender)

{

Dictionary *content = Dictionary::create();

content->setObject(String::create("ShareSDK for Cocos2d-x 3.0rc2社交分享测试。")

, "content");

content->setObject(String::create("ShareSDK分享测试"), "title");

content->setObject(String::create("http://tonybai.com"), "titleUrl");

content->setObject(String::create("http://tonybai.com"), "url");

content->setObject(String::create("Tony Bai"), "site");

content->setObject(String::create("http://tonybai.com"), "siteUrl");

content->setObject(String::createWithFormat("%s", *YOUR_LOCAL_IMAGE_PAT*H)

, "image");

content->setObject(String::createWithFormat("%d", C2DXContentTypeNews)

, "type");

C2DXShareSDK::showShareMenu(NULL, content, CCPointMake(100, 100),

C2DXMenuArrowDirectionLeft, shareResultHandler);

}

void shareResultHandler(C2DXResponseState state,

C2DXPlatType platType,

Dictionary *shareInfo,

Dictionary *error)

{

AppDelegate *app = (AppDelegate*)Application::getInstance();

switch (state) {

case C2DXResponseStateSuccess:

CCLog("Share Ok");

app->showShareResultToast("分享成功");

break;

case C2DXResponseStateFail:

app->showShareResultToast("分享失败");

CCLog("Share Failed");

break;

default:

break;

}

}

showShareResultToast实现如下：

void AppDelegate::showShareResultToast(const char *msg)

{

JniMethodInfo t;

if (JniHelper::getStaticMethodInfo(t, "YOUR_ACTIVITY_NAME",

"showShareResultToast", "(Ljava/lang/String;)V")) {

jstring jmsg = t.env->NewStringUTF(msg);

t.env->CallStaticVoidMethod(t.classID, t.methodID, jmsg);

if (t.env->ExceptionOccurred()) {

t.env->ExceptionDescribe();

t.env->ExceptionClear();

return;

}

t.env->DeleteLocalRef(t.classID);

}

}

**4. Java部分代码集成**

在GameDemo/proj.android/src下面建立cn/sharesdk路径，将C2DXShareSDKSample /proj.android/src/cn/sharesdk下的onekeyshare和ShareSDKUtils.java Copy到GameDemo/proj.android/src/cn/sharesdk下面。

将ShareSDK-Android-2.3.7.zip解压后的ShareSDK for Android/Src/wxapi Copy到GameDemo/proj.android/src/com.tonybai.game/下。

修改GameDemo/proj.android/src/com.tonybai.game/GameDemoActivity.java文件：

import android.widget.Toast;

import cn.sharesdk.ShareSDKUtils;

…

public class GameDemoActivity extends Cocos2dxActivity {

private static Context context;

private static Handler notifyHandler = new Handler() {

public void handleMessage(Message msg) {

switch (msg.what) {

case 1:

String message = (String) msg.obj;

Toast.makeText(context, message,

Toast.LENGTH_SHORT).show();

break;

default:

break;

}

}

};

@Override

protected void onCreate(Bundle savedInstanceState) {

super.onCreate(savedInstanceState);

context = this;

ShareSDKUtils.prepare();

ShareSDKUtils.initSDK("YOUR_SHARESDK_APPKEY", true);

}

public static void showShareResultToast(String result) {

Message msg = new Message();

msg.what = 1;

msg.obj = result;

notifyHandler.sendMessage(msg);

}

@Override

public void onDestroy() {

ShareSDKUtils.stopSDK();

super.onDestroy();

}

}

**三、问题与解决方法**

按照上面的集成方法修改后，通过cocos编译app，在模拟器运行GameDemo，点击Share，理论上屏幕下方会出现ShareSDK的分享窗口，选择“新浪微博”图标，会打开“图文分享”内容窗口，点击窗口右上角的“分享”即可。

【**问题1**】“图文分享”窗口内容可编辑，并且总是弹出软键盘，影响体验。


期望：内容不可编辑，默认不弹出软键盘

解决方法：

打开proj.android/src/cn/sharesdk/onekeyshare/EditPage.java，做如下修改：

将窗口的软输入方式默认改为SOFT_INPUT_STATE_HIDDEN。

public void setActivity(Activity activity) {

super.setActivity(activity);

if (dialogMode) {

activity.setTheme(android.R.style.Theme_Dialog);

activity.requestWindowFeature(Window.FEATURE_NO_TITLE);

}

activity.getWindow().setSoftInputMode(

//WindowManager.LayoutParams.SOFT_INPUT_STATE_ALWAYS_VISIBLE);

**WindowManager.LayoutParams.SOFT_INPUT_STATE_HIDDEN);//default: hidden**

}

在initPageView中增加一行：etContent.setKeyListener(null)。让窗口内容无法修改。

private void initPageView() {

… …

// 文字输入区域

etContent = new EditText(getContext());

etContent.setGravity(Gravity.LEFT | Gravity.TOP);

etContent.setBackgroundDrawable(null);

etContent.setText(String.valueOf(reqData.get("text")));

**etContent.setKeyListener(null);//make the edittext uneditable**

etContent.setLayoutParams(lpEt);

… …

}

**【问题2】**向微博分享，点击“分享”后，过一会程序异常停止。

原因分析：

通过调试观察，发现ShareSDK在解析从Weibo收到的Json包时出现内存违法访问。具体位置是在解析一个数组对象时出现的问题。 ShareSDK用CCArray来存储Json中的数组对象。该问题在cocos2d-x 2.2.2版本中不会出现，但在cocos2d-x 3.0rc2版本中会出现。经代码对比发现，3.0rc2版本中的CCArray的实现与2.2.2 CCArray实现有很大不同，似乎是做了较大重构，暂不能确定是否是3.0rc2版本中CCArray实现的bug。

解决方法：由于后续的分享结果通知成功与否只需要根据分享的状态来决定，因此我们只需解析出"status"、“action”和“platform” 这三个CCNumber类型字段的值即可。CCArray类型的对象我们并不需要，因此我们只需绕过对Array类型字段的解析和存储即可，修改如下：

// Classes/C2DXShareSDK/Android/JSON/CCJSONConverter.cpp

void CCJSONConverter::convertJsonToDictionary(cJSON *json, CCDictionary *dictionary)

{

dictionary->removeAllObjects();

cJSON * j = json->child;

while (j) {

**if (j->type == cJSON_Number) {**

Ref * obj = getJsonObj(j);

dictionary->setObject(obj, j->string);

**}**

j = j->next;

}

}

**四、其他**

在使用ShareSDK做社交分享时，注意下面两个现象：

1) 第一次进行微博或微信分享时，会打开授权页面，授权后才能分享成功；

2) 微信分享窗口只有在手机联网状态下才能打开。如果手机无法联网，那微信好友、朋友圈和收藏分享将无法打开分享窗口，也不会有什么提示。

© 2014, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

1.按照你的教程进行测试，在执行到ShareSDKUtils.prepare()时程序奔溃2.点开里面的方法，发现是在UIHandler.prepare();这一步就挂了提示信息是ThreadGroup.uncaughtException(Thread, Throwable) line: 689 3.你这个是cocos2dx3.0的工程吗,我的3.0工程中没有与工程名一致的public class GameDemoActivity extends Cocos2dxActivity 这种activity只有public class Cocos2dxActivity extends NativeActivity