---
title: ShareSDK Cocos2d-x专用组件的一个Bug
url: https://tonybai.com/2014/04/17/a-bug-from-sharesdk-componet-for-cocos2dx/
published: '2014-04-17'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# ShareSDK Cocos2d-x专用组件的一个Bug

近期研究了一下Game App做社交分享，最后选择了[ShareSDK](http://www.sharesdk.cn)来集成，不仅是因为ShareSDK支持国内外主流社交平台，更重要的是ShareSDK提供了专门的[ cocos2d-x](http://www.cocos2d-x.org)集成方案，有专门的[文档](http://wiki.sharesdk.cn/cocos2d-x%E5%BF%AB%E9%80%9F%E9%9B%86%E6%88%90%E6%8C%87%E5%8D%97)和[代码Demo](https://github.com/ShareSDKPlatform/C2DXShareSDKSample)供开发者参考。

文档中提到了三种集成方式：纯Java方式、plugin-x方式以及Cocos2d-x专用组件方式，这里选择了ShareSDK Cocos2d-x专用组件（v2.3.7版本)的方式。按照文档中描述的步骤进行的相对顺利，在各个社交平台的appkey生效后，我们对demo app进行了测试，居然发现app经常随机性的崩溃，有时甚至是每次都崩溃，经过深入分析，发现这是ShareSDK Cocos2d-x专用组件的一个严重Bug，下面详细说明一下Bug的产生原因以及Fix方法。

**一、App崩溃的场景和代码位置**

发生崩溃的场景如下：

App Demo中有一个"Share"按钮，点击该按钮，App Demo向已经授权的社交平台分享一些Test Content，而App Demo就在收到分享结果应答时发生了崩溃。

代码位置大致如下：

void AppDemo::onShareClick(CCObject* sender)

{

… …

C2DXShareSDK::showShareMenu(NULL, content,

CCPointMake(100, 100),

C2DXMenuArrowDirectionLeft,

**shareResultHandler**);

}

void shareResultHandler(C2DXResponseState state, C2DXPlatType platType,

CCDictionary *shareInfo, CCDictionary *error)

{

switch (state) {

case C2DXResponseStateSuccess:

CCLog("Share Ok");

break;

case C2DXResponseStateFail:

CCLog("Share Failed");

break;

default:

break;

}

}

崩溃的位置大致就在回调shareResultHandler前后的某个位 置，比较随机。

**二、现象分析**

通过查看Eclipse logcat窗口的调试日志，我们发现一些规律，一些在“Share Ok后的崩溃打印出如下日志：

04-16 01:28:33.890: D/cocos2d-x debug info(1748): Share Ok

04-16 01:28:34.090: D/cocos2d-x debug info(1748): Assert failed: reference count should greater than 0

04-16 01:28:34.090: E/cocos2d-x assert(1748): /home1/tonybai/android-dev/cocos2d-x-2.2.2/samples/Cpp/temp/AppDemo/proj.android/../../../../../cocos2dx/cocoa/CCObject.cpp function:release line:81

04-16 01:28:34.130: A/libc(1748): Fatal signal 11 (SIGSEGV) at 0×00000003 (code=1), thread 1829 (Thread-122)

猜测一下，似乎是某个CCObject在真正Release前已经被释放了，然后后续被引用时触发内存非法访问。Cocos2d-x采用的是内存 计数的内存管理机制，在我的《[Cocos2d-x内存管理-绕不过去的坎](http://tonybai.com/2014/03/18/cocos2dx-memory-management/)》一文中有描述。了解Cocos2d-x的内存管理机制是理解这个Bug 的前提条件。

**三、原因分析**

看来不得不挖掘一下ShareSDK组件的代码了。AppDemo中ShareSDK组件的代码分为两个部分：AppDemo/Classes /C2DXShareSDK和AppDemo/proj.android/src/cn/sharesdk。前者是C++代码，后面则是Java 代码，两者通过jni调用联系在一起。我们重点来找出分享应答返回来时的关键联系。

集成ShareSDK的Cocos2d-x程序会在主Activity的onCreate方法中调用ShareSDKUtils.prepare();

我们来看看prepare方法的实现：

//AppDemo/proj.android/src/cn/sharesdk/ShareSDKUtils.java

public class ShareSDKUtils {

private static boolean DEBUG = true;

private static Context context;

private static PlatformActionListener paListaner;

private static Hashon hashon;

… …


public static void prepare() {

UIHandler.prepare();

context = Cocos2dxActivity.getContext().getApplicationContext();

hashon = new Hashon();

final Callback cb = new Callback() {

public boolean handleMessage(Message msg) {

**onJavaCallback**((String) msg.obj);

return false;

}

};

paListaner = new PlatformActionListener() {

public void onComplete(Platform platform, int action, HashMap<String, Object> res) {

if (DEBUG) {

System.out.println("onComplete");

System.out.println(res == null ? "" : res.toString());

}

HashMap<String, Object> map = new HashMap<String, Object>();

map.put("platform", ShareSDK.platformNameToId(platform.getName()));

map.put("action", action);

map.put("status", 1); // Success = 1, Fail = 2, Cancel = 3

map.put("res", res);

Message msg = new Message();

msg.obj = hashon.fromHashMap(map);

**UIHandler.sendMessage(msg, cb);**

}

… …

}

可以看出监听Complete事件的listener将message的处理都交给了cb，而cb调用了onJavaCallback方法。

onJavaCallback方法是jni导出的方法，它的实现在 AppDemo/Classes/C2DXShareSDK/Android/ShareSDKUtils.cpp里面。

JNIEXPORT void JNICALL Java_cn_sharesdk_ShareSDKUtils_onJavaCallback

(JNIEnv * env, jclass thiz, jstring resp) {

CCJSONConverter* json = CCJSONConverter::sharedConverter();

const char* ccResp = env->GetStringUTFChars(resp, JNI_FALSE);

CCLog("ccResp = %s", ccResp);

CCDictionary* dic = json->**dictionaryFrom**(ccResp);

env->ReleaseStringUTFChars(resp, ccResp);

CCNumber* status = (CCNumber*) dic->objectForKey("status"); // Success = 1, Fail = 2, Cancel = 3

CCNumber* action = (CCNumber*) dic->objectForKey("action"); // 1 = ACTION_AUTHORIZING, 8 = ACTION_USER_INFOR,9 = ACTION_SHARE

CCNumber* platform = (CCNumber*) dic->objectForKey("platform");

CCDictionary* res = (CCDictionary*) dic->objectForKey("res");

// TODO add codes here

if(1 == status->getIntValue()){

callBackComplete(action->getIntValue(), platform->getIntValue(), res);

}else if(2 == status->getIntValue()){

callBackError(action->getIntValue(), platform->getIntValue(), res);

}else{

callBackCancel(action->getIntValue(), platform->getIntValue(), res);

}

dic->autorelease();

}

这就是两块代码的关键联系。而问题似乎就出在onJavaCallback方 法里，因为我们看到了该方法中使用了Cocos2d-x的数据结构类。

我们来看一下onJavaCallback方法是在哪个线程里执行的。Cocos2d-x App至少有两个线程，一个UI Thread（Activity），一个Render Thread。显然onJavaCallback是在UI Thread中被执行的。但是我们知道Cocos2d-x的AutoreleasePool是在Render Thread中管理的，并在帧切换时进行释放操作的。

我们似乎闻到了问题的味道。Cocos2d-x基本上算是一个"单线程"游戏架构，所有的渲染操作、渲染树节点逻辑管理、绝大多数游戏逻辑都在 Render Thread中进行，UI Thread更多的是接收系统事件，并传递给Render Thread处理。Cocos2d-x的内存管理在这样的“单线程”背景下是没有大问题的，都是串行操作，不存在thread racing的情况。但一旦另外一个线程也调用内存管理接口进行对象内存操作时，问题就出现了，Cocos2d-x的内存池管理不是线程安全的。

我们回到上面代码，重点看一下json转dic的方法，该方法将分享应答字符串转换为内部的dictionary结构：

//AppDemo/Classes/C2DXShareSDK/Android/JSON/CCJSONConverter.cpp

CCDictionary * CCJSONConverter::dictionaryFrom(const char *str)

{

cJSON * json = cJSON_Parse(str);

if (!json || json->type!=cJSON_Object) {

if (json) {

cJSON_Delete(json);

}

return NULL;

}

CCAssert(json && json->type==cJSON_Object, "CCJSONConverter:wrong json format");

**CCDictionary * dictionary = CCDictionary::create();**

**convertJsonToDictionary**(json, dictionary);

cJSON_Delete(json);

return dictionary;

}

void CCJSONConverter::convertJsonToDictionary(cJSON *json, CCDictionary *dictionary)

{

dictionary->removeAllObjects();

cJSON * j = json->child;

while (j) {

CCObject * obj = **getJsonObj**(j);

dictionary->setObject(obj, j->string);

j = j->next;

}

}

CCObject * CCJSONConverter::getJsonObj(cJSON * json)

{

switch (json->type) {

case cJSON_Object:

{

CCDictionary * dictionary = CCDictionary::create();

convertJsonToDictionary(json, dictionary);

return dictionary;

}

case cJSON_Array:

{

CCArray * array = CCArray::create();

convertJsonToArray(json, array);

return array;

}

case cJSON_String:

{

CCString * string = CCString::create(json->valuestring);

return string;

}

case cJSON_Number:

{

CCNumber * number = CCNumber::create(json->valuedouble);

return number;

}

case cJSON_True:

{

CCNumber * boolean = CCNumber::create(1);

return boolean;

}

case cJSON_False:

{

CCNumber * boolean = CCNumber::create(0);

return boolean;

}

case cJSON_NULL:

{

CCNull * null = CCNull::create();

return null;

}

default:

{

CCLog("CCJSONConverter encountered an unrecognized type");

return NULL;

}

}

}

可以看出整个解析过程，都直接用的是传统的Cocos2d-x对象构造方法：create。在每个对象的create中，代码都会调用该对象的 autorelease方法。而这个方法本身就是线程不安全的，且即便autorelease调用ok，在下一帧切换时，这些对象将都会被release 掉，如果在UI Thread中再引用这些对象的地址，那势必造成内存的非法访问，而引发程序崩溃。

**四、Fix方法**

可能有朋友会问，create后，我retain一下可否？答案是否。因此create的创建不是线程安全的，create和retain两个调 用之间存在时间差，而在这段时间内，该对象就有可能被render thread释放掉。

Fix方法很简单，就是在UI Thread中不使用Cocos2d-x的内存管理机制，我们用传统的new来替代create，并将 Java_cn_sharesdk_ShareSDKUtils_onJavaCallback最后的autorelease改为release，这样就 不用劳烦Render Thread来帮我们释放内存了。CCDictionary的destructor调用时还会将Dictionarny内部所有Element自动释放 掉。

© 2014, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论