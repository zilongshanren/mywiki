---
title: Cocos2d-x 3.0多线程异步资源加载
url: https://tonybai.com/2014/04/28/multithreaded-resource-loading-in-cocos2dx-3/
published: '2014-04-28'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Cocos2d-x 3.0多线程异步资源加载

[Cocos2d-x](http://www.cocos2d-x.org)从[2.x版](http://tonybai.com/2014/03/11/hello-cocos2dx/)本到上周刚刚才发布的[Cocos2d-x 3.0 Final版](http://www.cocos2d-x.org/news/215)，其引擎驱动核心依旧是一个单线程的“死循环”，一旦某一帧遇到了“大活儿”，比如Size很大的纹理资源加载或网络IO或大量计算，画面将 不可避免出现卡顿以及响应迟缓的现象。从古老的Win32 GUI编程那时起，Guru们就告诉我们：别阻塞主线程(UI线程)，让Worker线程去做那些“大活儿”吧。

手机游戏，即便是休闲类的小游戏，往往也涉及大量纹理资源、音视频资源、文件读写以及网络通信，处理的稍有不甚就会出现画面卡顿，交互不畅的情况。虽然引 擎在某些方面提供了一些支持，但有些时候还是自己祭出Worker线程这个法宝比较灵活，下面就以Cocos2d-x 3.0 Final版游戏初始化为例（针对Android平台），说说如何进行多线程资源加载。

我们经常看到一些手机游戏，启动之后首先会显示一个带有公司Logo的闪屏画面(Flash Screen)，然后才会进入一个游戏Welcome场景，点击“开始”才正式进入游戏主场景。而这里Flash Screen的展示环节往往在后台还会做另外一件事，那就是加载游戏的图片资源，音乐音效资源以及配置数据读取，这算是一个“障眼法”吧，目的就是提高用 户体验，这样后续场景渲染以及场景切换直接使用已经cache到内存中的数据即可，无需再行加载。

**一、为游戏添加FlashScene**

在游戏App初始化时，我们首先创建FlashScene，让游戏尽快显示FlashScene画面：

// AppDelegate.cpp

bool AppDelegate::applicationDidFinishLaunching() {

… …

FlashScene* scene = FlashScene::create();

pDirector->runWithScene(scene);

return true;

}

在FlashScene init时，我们创建一个Resource Load Thread，我们用一个ResourceLoadIndicator作为渲染线程与Worker线程之间交互的媒介。

//FlashScene.h

struct ResourceLoadIndicator {

pthread_mutex_t mutex;

bool load_done;

void *context;

};

class FlashScene : public Scene

{

public:

FlashScene(void);

~FlashScene(void);

virtual bool init();

CREATE_FUNC(FlashScene);

bool getResourceLoadIndicator();

void setResourceLoadIndicator(bool flag);

private:

void updateScene(float dt);

private:

ResourceLoadIndicator rli;

};

// FlashScene.cpp

bool FlashScene::init()

{

bool bRet = false;

do {

CC_BREAK_IF(!CCScene::init());

Size winSize = Director::getInstance()->getWinSize();

//FlashScene自己的资源只能同步加载了

Sprite *bg = Sprite::create("FlashSceenBg.png");

CC_BREAK_IF(!bg);

bg->setPosition(ccp(winSize.width/2, winSize.height/2));

this->addChild(bg, 0);

this->schedule(schedule_selector(FlashScene::updateScene)

, 0.01f);

//start the resource loading thread

rli.load_done = false;

rli.context = (void*)this;

pthread_mutex_init(&rli.mutex, NULL);

pthread_attr_t attr;

pthread_attr_init(&attr);

pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_DETACHED);

pthread_t thread;

pthread_create(&thread, &attr,

resource_load_thread_entry, &rli);

bRet=true;

} while(0);

return bRet;

}

static void* resource_load_thread_entry(void* param)

{

AppDelegate *app = (AppDelegate*)Application::getInstance();

ResourceLoadIndicator *rli = (ResourceLoadIndicator*)param;

FlashScene *scene = (FlashScene*)rli->context;

//load music effect resource

… …

//init from config files

… …

//load images data in worker thread

SpriteFrameCache::getInstance()->addSpriteFramesWithFile(

"All-Sprites.plist");

… …

//set loading done

scene->setResourceLoadIndicator(true);

return NULL;

}

bool FlashScene::getResourceLoadIndicator()

{

bool flag;

pthread_mutex_lock(&rli.mutex);

flag = rli.load_done;

pthread_mutex_unlock(&rli.mutex);

return flag;

}

void FlashScene::setResourceLoadIndicator(bool flag)

{

pthread_mutex_lock(&rli.mutex);

rli.load_done = flag;

pthread_mutex_unlock(&rli.mutex);

return;

}

我们在定时器回调函数中对indicator标志位进行检查，当发现加载ok后，切换到接下来的游戏开始场景：

void FlashScene::updateScene(float dt)

{

if (getResourceLoadIndicator()) {

Director::getInstance()->replaceScene(

WelcomeScene::create());

}

}

到此，FlashScene的初始设计和实现完成了。Run一下试试吧。

**二、崩溃**

在[GenyMotion](http://genymotion.com/)的4.4.2模拟器上，游戏运行的结果并没有如我期望，FlashScreen显现后游戏就异常崩溃退出了。

通过monitor分析游戏的运行日志，我们看到了如下一些异常日志：

threadid=24: thread exiting, not yet detached (count=0)

threadid=24: thread exiting, not yet detached (count=1)

threadid=24: native thread exited without detaching

很是奇怪啊，我们在创建线程时，明明设置了 PTHREAD_CREATE_DETACHED属性了啊：

pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_DETACHED);

怎么还会出现这个问题，而且居然有三条日志。翻看了一下引擎内核的代码TextureCache::addImageAsync，在线程创建以及线程主函数中也没有发现什么特别的设置。为何内核可以创建线程，我自己创建就会崩溃呢。Debug多个来回，问题似乎聚焦在resource_load_thread_entry中执行的任务。在我的代码里，我利用SimpleAudioEngine加载了音效资源、利用UserDefault读取了一些持久化的数据，把这两个任务去掉，游戏就会进入到下一个环节而不会崩溃。

SimpleAudioEngine和UserDefault能有什么共同点呢？Jni调用。没错，这两个接口底层要适配多个平台，而对于Android 平台，他们都用到了Jni提供的接口去调用Java中的方法。而Jni对多线程是有约束的。[Android开发者官网](http://developer.android.com/training/articles/perf-jni.html)上有这么一段话：

All threads are Linux threads, scheduled by the kernel. They're usually started from managed code (using Thread.start), but they can also be created elsewhere and then attached to the JavaVM. For example, a thread started with pthread_create can be attached with the JNI AttachCurrentThread or AttachCurrentThreadAsDaemon functions. **Until a thread is attached, it has no JNIEnv, and cannot make JNI calls**.

由此看来pthread_create创建的新线程默认情况下是不能进行Jni接口调用的，除非Attach到Vm，获得一个JniEnv对象，并且在线 程exit前要Detach Vm。好，我们来尝试一下，Cocos2d-x引擎提供了一些JniHelper方法，可以方便进行Jni相关操作。

#if (CC_TARGET_PLATFORM == CC_PLATFORM_ANDROID)

#include "platform/android/jni/JniHelper.h"

#include <jni.h>

#endif

static void* resource_load_thread_entry(void* param)

{

… …

JavaVM *vm;

JNIEnv *env;

vm = JniHelper::getJavaVM();

JavaVMAttachArgs thread_args;

thread_args.name = "Resource Load";

thread_args.version = JNI_VERSION_1_4;

thread_args.group = NULL;

vm->**AttachCurrentThread**(&env, &thread_args);

… …

//Your Jni Calls

… …

vm->**DetachCurrentThread**();

… …

return NULL;

}

关于什么是JavaVM，什么是JniEnv，Android Developer官方文档中是这样描述的：

The JavaVM provides the "invocation interface" functions, which allow you to create and destroy a JavaVM. In theory you can have multiple JavaVMs per process, but **Android only allows one**.

The JNIEnv provides most of the JNI functions. Your native functions all receive a JNIEnv as the first argument.

The JNIEnv is used for thread-local storage. For this reason, you cannot share a JNIEnv between threads.

**三、黑屏**

上面的代码成功解决了线程崩溃的问题，但问题还没完，因为接下来我们又遇到了“黑屏”事件。所谓的“黑屏”，其实并不是全黑。但进入游戏 WelcomScene时，只有Scene中的LabelTTF实例能显示出来，其余Sprite都无法显示。显然肯定与我们在Worker线程加载纹理 资源有关了：

SpriteFrameCache::getInstance()->addSpriteFramesWithFile("All-Sprites.plist");

我们通过碎图压缩到一张大纹理的方式建立SpriteFrame，这是Cocos2d-x推荐的优化手段。但要想找到这个问题的根源，还得看monitor日志。我们的确发现了一些异常日志：

libEGL: call to OpenGL ES API with no current context (logged once per thread)

通过Google得知，只有Renderer Thread才能进行egl调用，因为egl的context是在Renderer Thread创建的，Worker Thread并没有EGL的context，在进行egl操作时，无法找到context，因此操作都是失败的，纹理也就无法显示出来。要解决这个问题就 得查看一下TextureCache::addImageAsync是如何做的了。

TextureCache::addImageAsync只是在worker线程进行了image数据的加载，而纹理对象Texture2D instance则是在addImageAsyncCallBack中创建的。也就是说纹理还是在Renderer线程中创建的，因此不会出现我们上面的 “黑屏”问题。模仿addImageAsync，我们来修改一下代码：

static void* resource_load_thread_entry(void* param)

{

… …

allSpritesImage = new Image();

allSpritesImage->initWithImageFile("All-Sprites.png");

… …

}

void FlashScene::updateScene(float dt)

{

if (getResourceLoadIndicator()) {

// construct texture with preloaded images

Texture2D *allSpritesTexture = TextureCache::getInstance()->

addImage(allSpritesImage, "All-Sprites.png");

allSpritesImage->release();

SpriteFrameCache::getInstance()->addSpriteFramesWithFile(

"All-Sprites.plist", allSpritesTexture);


Director::getInstance()->replaceScene(WelcomeScene::create());

}

}

完成这一修改后，游戏画面就变得一切正常了，多线程资源加载机制正式生效。

© 2014, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

受教了。你好，博主能否提供代码下载呢？

同求

都有addImageAsync，那还这么干的理由是？而且在2dx 3.0, C++11环境下pthread_create不嫌蛋疼？

这个pthread和std::thread都差不多的，没有太大差别

博主能否提供代码下载呢？qq357634525

这样有线程安全问题吧子线程调用 SpriteFrameCache::getInstance()->addSpriteFramesWithFile()，它的内部其实就是创建出一个个SpriteFrame，然后添加进cache列表(Map)里。也就是先“创建”，再“添加”。这是两个动作，中间会有时间间隔，如果此时发生上下文切换，而主线程又刚好执行到自动释放资源，那这个刚创建出来，又还未添加到Map的对象就会被释放。紧接着子线程执行“添加”动作就会出问题了。

SpriteFrameCache::getInstance()->addSpriteFramesWithFile()就是在渲染线程里调用的，再上下文切换也不会受到影响吧。cocos2dx中资源也是在渲染线程中进行的。在同一个线程中执行的代码如何出现racing情况呢？

ken说得对, 之前也被这个坑过 是会有问题的

博主你好， 我这边用3.0 正常的加载的图片, 运行一段时间也会出现黑屏，情况基本和你类似，现在是一头雾水，能不能有什么好的建议或解决方法？？ 希望得到你的回复，谢谢 ！