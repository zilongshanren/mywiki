---
title: Hello, Cocos2d-x
url: https://tonybai.com/2014/03/11/hello-cocos2dx/
published: '2014-03-11'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Hello, Cocos2d-x

女儿从两岁半开始接触iPad，在这个年龄段也只有一些幼教类游戏适合她玩。虽然知道iPad玩久了对视力有伤害，但有时候还真拗不过果果，索性 也就让她玩一会儿。之前对智能终端上的东西不是很在意，也没啥兴趣，这大概与当年在大学时做Win32 GUI开发的糟糕经历多多少少有点关系。不过智能终端是大势所趋，历史的潮流不能违抗。虽然自己并非以[Android](http://tonybai.com/2011/05/24/develop-android-app-in-command-line-method/)/iOS编程为主业，但适当学习学习 总归没有坏处，万一作出一个像"Flappy Bird"的游戏，爆发一下，还是蛮Happy的。于是在开始学习实践之前给自己定了一个小目标：今年六一儿童节送给女儿一款自己制作的小游戏。

智能终端上的游戏目前风头正劲，试问哪个智能手机上没有几款[企鹅公司](http://qq.com)出品的游戏呢！之前从未涉猎过游戏开发，但知道游戏开发前要挑选一款合适的游 戏引擎，自己从头开始敲代码的时代已经out了。在寻觅游戏引擎之前，我需要回答三道摆在我面前的选择题：

* 1、2D引擎还是3D引擎？
2、平台专用引擎还是跨平台引擎？
3、收费引擎还是开源引擎？*

作为入门级选手，2D游戏显然更适合上手一些，另外适合果果这个年龄段的幼教类的游戏也多以2D游戏居多。3D游戏本身也太难了，不仅要 Programming能力，还要3D建模能力，这些学习起来周期就太长了；一直是[Ubuntu](http://tonybai.com/tag/Ubuntu) Fans，手头没有Mac Book，这样开发iOS程序变成一件糟心的事，在Ubuntu下搭建iOS App开发环境繁杂的很，即便是虚拟机也懒得尝试。但从游戏体验来看，还是在iPad上玩更好一些，因此最好引擎能跨平台，以便后续迁移到iOS上；开源 和用开源惯了，收费的引擎目前不在考虑范围之内。综上，我要寻找的是一款开源的、跨平台的Mobile 2D Game Engine。

于是我找到了[Cocos2d-x](http://cocos2d-x.org/)！Cocos2d-x是[Cocos2d-iphone](http://www.cocos2d-iphone.org/)的C++跨平台分支，由于是国人创立的，在国内有着较大的用 户群，引擎资料也较多，社区十分活跃。国内已经出版了多本有关Cocos2d-x的中文书籍，比如《[Cocos2d-x高级开发教程:制作自己的 “捕鱼达人”](http://book.douban.com/subject/24704115/)》 、《[Cocos2d-x权威指南](http://book.douban.com/subject/23820911/)》 等都还不错。更重要的是Cocos2d-x自带了丰富的例子，供初学者“临摹学习”，其中cocos2d-x-2.2.2/samples/Cpp /TestCpp这个例子几乎涵盖了该引擎的绝大多数功能。下面就开启Cocos2d-x的入门之旅（For Android）。

**一、引擎安装**

试验环境：

* Ubuntu 12.04.1 x86_64
gcc 4.6.3
javac 1.7.0_21
java "1.7.0_21" HotSpot 64-bit Server VM
adt-bundle-linux-x86_64-20131030.zip
android-ndk-r9d-linux-x86_64.tar.bz2*

Cocos2d-x官网目前提供2.2.2稳定版以及3.0beta2版的下载（当然你也可以下载到更老的版本）。由于3.0改变较大，资料不 多，且对编译器等版本的要求较高(需要支持[C++ 11标准](http://en.wikipedia.org/wiki/C++11))，因此这里依旧以2.2.2版本作为学习目标。Cocos2d-x-2.2.2下载后解压到某个目录：比如/home1/tonybai/android-dev/cocos2d-x-2.2.2。 如果仅是用Cocos2d-x开发Android版本游戏，则不需要做什么编译工作。Android Game Project会在Project build时自动用NDK的编译器编译C++代码，并与NDK链接。如果你想早点看看Cocos2d-x sample中的例子运行起来到底是什么样子的，你可以在Ubuntu下编译出Linux版本的游戏：在cocos2d-x-2.2.2下执行make-all-linux-project.sh即可。编译需要一段时间，编译成 功后，我们可以进入到“cocos2d-x-2.2.2/samples/Cpp/HelloCpp/proj.linux/bin/release” 下执行“HelloCpp”这个可执行文件，一个最简单的Cocos2d-x游戏就会展现在你的面前了。

Android sample project的构建稍微复杂些：

首先在Eclipse中添加libcocos2dx Library project from existed code（注意：不Copy到workspace，原地建立）。该Project的代码路径为cocos2d-x-2.2.2/cocos2dx/platform /android/java。在project.properties和AndroidManifest.xml适当修改你所使用的api版本， 以让编译通过。我这里用的是 target=android-19。

然后，设置NDK_ROOT环境变量(比如export NDK_ROOT='/home1/tonybai/android-dev/adt-bundle-linux-x86_64/android-ndk-r9c')， 供build_native.sh使用。

最后添加游戏project。在Eclipse中添加HelloCpp project from existed code，位置cocos2d-x-2.2.2/samples/Cpp/HelloCpp/proj.android（注 意：不Copy到Workspace中，原地建立）。在HelloCpp的project.properties中添加“android.library.reference.1=../../../../cocos2dx/platform/android /java”。同样别忘了在project.properties和AndroidManifest.xml适当修改你所使用 的api版本，以让编译通过。

如果一切顺利的话，你会在Console窗口看到“**** Build Finished ****”。Problems窗口显示“0 errors“。 启动Android模拟器，Run Application，同样的HelloCpp画面会呈现在模拟器上。

Cocos2d-x是建构在OpenGL技术之上的。对于Android平台而言，Android SDK已经完全封装了opengl es 1.1/2.0的API（android.opengl.*;javax.microedition.khronos.egl.*;javax.microedition.khronos.opengles.*）， 引擎完全可以建立在这个之上，无需C++代码。但Cocos2d-x是一个跨平台的2D游戏引擎，核心选择了用C++代码实现(iOS提供的C绑 定，不提供Java绑定；Android则提供了Java和C绑定)，因此 在开发Android平台的2D游戏时，引擎部分是SDK与NDK交相互应，比如GLThread的创建和管理用的是SDK的 GLSurfaceView和GLThread，但真正的Surface绘制部分则是回调Cocos2d-x用C++编写的绘制实现（链接NDK 中的库）。

**二、Cocos2d-x Android工程代码组织结构**

以samples/Cpp/HelloApp的Android工程为例，Android版的Cocos2d-x工程与普通android应用程序 差别 不大，核心部分只是多了一个jni目录和一个build_native.sh脚本文件。其中jni目录下存放的是Java和C++调用转换的“胶 水”代码；build_native.sh则是用于编译jni下C++代码以及 cocos2dx_static library代码的构建脚本。

HelloCpp的构建过程摘要如下：

**** Build of configuration Default for project HelloCpp ****

**bash /home1/tonybai/android-dev/cocos2d-x-2.2.2/samples/Cpp/HelloCpp/proj.android/build_native.sh**

NDK_ROOT = /home1/tonybai/android-dev/adt-bundle-linux-x86_64/android-ndk-r9c

COCOS2DX_ROOT = /home1/tonybai/android-dev/cocos2d-x-2.2.2/samples/Cpp/HelloCpp/proj.android/../../../..

APP_ROOT = /home1/tonybai/android-dev/cocos2d-x-2.2.2/samples/Cpp/HelloCpp/proj.android/..

APP_ANDROID_ROOT = /home1/tonybai/android-dev/cocos2d-x-2.2.2/samples/Cpp/HelloCpp/proj.android

+ /home1/tonybai/android-dev/adt-bundle-linux-x86_64/android-ndk-r9c/ndk-build -C /home1/tonybai/android-dev/cocos2d-x-2.2.2/samples/Cpp/HelloCpp/proj.androidNDK_MODULE_PATH=/home1/tonybai/android-dev/cocos2d-x-2.2.2/samples/Cpp/HelloCpp/proj.android/../../../..:/home1/tonybai/android-dev/cocos2d-x-2.2.2/samples/Cpp/HelloCpp/proj.android/../../../../cocos2dx/platform/third_party/android/prebuilt

Using prebuilt externals

Android NDK: WARNING:/home1/tonybai/android-dev/cocos2d-x-2.2.2/samples/Cpp/HelloCpp/proj.android/../../../../cocos2dx**/Android.mk**:cocos2dx_static: LOCAL_LDLIBS is always ignored for static libraries

make: Entering directory `/home1/tonybai/android-dev/cocos2d-x-2.2.2/samples/Cpp/HelloCpp/proj.android'

[armeabi] Compile++ thumb: hellocpp_shared <= main.cpp

[armeabi] Compile++ thumb: hellocpp_shared <= AppDelegate.cpp

[armeabi] Compile++ thumb: hellocpp_shared <= HelloWorldScene.cpp

[armeabi] Compile++ thumb: cocos2dx_static <= CCConfiguration.cpp

[armeabi] Compile++ thumb: cocos2dx_static <= CCScheduler.cpp

… …

[armeabi] Compile++ thumb: cocos2dx_static <= CCTouch.cpp

[armeabi] StaticLibrary : libcocos2d.a

[armeabi] Compile thumb : cpufeatures <= cpu-features.c

[armeabi] StaticLibrary : libcpufeatures.a

[armeabi] SharedLibrary : libhellocpp.so

[armeabi] Install : libhellocpp.so => libs/armeabi/libhellocpp.so

make: Leaving directory `/home1/tonybai/android-dev/cocos2d-x-2.2.2/samples/Cpp/HelloCpp/proj.android'

**** Build Finished ****

指挥NDK编译的则是jni下的Android.mk文件，其角色类似于Makefile。

**三、Cocos2d-x Android工程代码阅读**

单独将如何阅读代码拿出来，是为了后面分析引擎的驱动流程做准备工作。学习类似Cocos2d-x这样的游戏引擎，仅仅停留在游戏逻辑层代码是不 能很好的把握引擎本质的，因此适当的挖掘引擎实现实际上对于理解和使用 引擎都是大有裨益的。

以一个Cocos2d-x Android工程为例，它的游戏逻辑代码以及涉及的引擎代码涵盖在一下路径下（还是以HelloCpp的Android工程为例）：

项目层：

* cocos2d-x-2.2.2/samples/Cpp/HelloCpp/proj.android/src 主Activity的实现；

* cocos2d-x-2.2.2/samples/Cpp/HelloCpp/proj.android/jni/hellocpp Cocos2dxRenderer类的nativeInit实现，用于引出Application的入口；

* cocos2d-x-2.2.2/samples/Cpp/HelloCpp/Classes 你的游戏逻辑，以C++代码形式呈现；


引擎层：

* cocos2d-x-2.2.2/cocos2dx/platform/android/java/src 引擎层对Android Activity、GLSurfaceView以及Render的封装

* cocos2d-x-2.2.2/cocos2dx/platform/android/jni 对应上面封装的native method实现

* cocos2d-x-2.2.2/cocos2dx、cocos2d-x-2.2.2/cocos2dx/platform、cocos2d-x- 2.2.2/cocos2dx/platform/android cocos2dx引擎的核心实现(针对android平台)

后续的代码分析也将从这两个层次、六处位置出发。

**四、从Activity开始**

之前多少了解了一些Android App开发的知识，Android App都是始于Activity的。游戏也是App的一种，因此在Android平台上，Cocos2d-x游戏也是从Activity开始的。于是 Activity，确切的说是Cocos2dxActivity是我们这次引擎驱动机制分析的出发点。

回顾Android Activity的Lifecycle，Activity启动的顺序是：Activity.onCreate -> Activity.onStart() -> Activity.onResume()。接下来我们将按照 这条主线进行引擎驱动机制的分析。

HelloCpp.java中的HelloCpp这个Activity完全无所作为，仅仅是继承其父类Cocos2dxActivity的实现罢 了。

// HelloCpp.java

public class HelloCpp extends Cocos2dxActivity{

protected void onCreate(Bundle savedInstanceState){

super.onCreate(savedInstanceState);

}

… …

}

我们来看Cocos2dxActivity类。

// Cocos2dxActivity.java

@Override

protected void onCreate(final Bundle savedInstanceState) {

super.onCreate(savedInstanceState);

sContext = this;

this.mHandler = new Cocos2dxHandler(this);

this.init();

Cocos2dxHelper.init(this, this);

}

public void init() {

// FrameLayout

ViewGroup.LayoutParams framelayout_params =

new ViewGroup.LayoutParams(ViewGroup.LayoutParams.FILL_PARENT,

ViewGroup.LayoutParams.FILL_PARENT);

FrameLayout framelayout = new FrameLayout(this);

framelayout.setLayoutParams(framelayout_params);

… …

// Cocos2dxGLSurfaceView

this.mGLSurfaceView = this.onCreateView();

// …add to FrameLayout

framelayout.addView(this.mGLSurfaceView);

… …

this.mGLSurfaceView.setCocos2dxRenderer(new Cocos2dxRenderer());

… …

// Set framelayout as the content view

setContentView(framelayout);

}

从上面代码可以看出，onCreate调用的init方法才是Cocos2dxActivity初始化的核心。在init方法 中，Cocos2dxActivity创建了一个Framelayout实例，并将该实例作为content View赋给了Cocos2dxActivity的实例。Framelayout实例也并不孤单，一个设置了Cocos2dxRenderer实例的 GLSurfaceView被Added to it。而Cocos2d-x引擎的初始化已经悄悄地在这几行代码间完成了，至于初始化的细节我们后续再做分析。

接下来是onResume方法，它的实现如下：

@Override

protected void onResume() {

super.onResume();

Cocos2dxHelper.onResume();

this.mGLSurfaceView.onResume();

}

onResume调用了View的onResume()。

// Cocos2dxGLSurfaceView：

@Override

public void onResume() {

super.onResume();

this.queueEvent(new Runnable() {

@Override

public void run() {

Cocos2dxGLSurfaceView.this.mCocos2dxRenderer.handleOnResume();

}

});

}

Cocos2dxGLSurfaceView将该事件打包放到队列里，扔给了另外一个线程去执行（后续会详细说明这个线程），对应的方法在 Cocos2dxRenderer class中。

public void handleOnResume() {

Cocos2dxRenderer.nativeOnResume();

}

Render实际上调用的是native方法。

JNIEXPORT void JNICALL Java_org_cocos2dx_lib_Cocos2dxRenderer_nativeOnResume() {

if (CCDirector::sharedDirector()->getOpenGLView()) {

CCApplication::sharedApplication()->applicationWillEnterForeground();

}

}

applicationWillEnterForeground方法在你的AppDelegate.cpp中；

void AppDelegate::applicationWillEnterForeground() {

CCDirector::sharedDirector()->startAnimation();//

// if you use SimpleAudioEngine, it must resume here

// SimpleAudioEngine::sharedEngine()->resumeBackgroundMusic();

}

这里仅是重新获得了一下时间罢了。

**五、Render Thread(渲染线程)** **- GLThread**

游戏引擎要兼顾UI事件和屏幕帧刷新。Android的OpenGL应用采用了UI线程(Main Thread) + 渲染线程(Render Thread)的模式。Activity活在Main Thread(主线程)中，也叫做UI线程。该线程负责捕获与用户交互的信息和事件，并与渲染(Render)线程交互。比如当用户接听电话、切换到其他 程序时，渲染线程必须知道发生了 这些事件，并作出即时的处理，而这些事件及处理方式都是由主线程中的Activity以及其装载的View传递给渲染线程的。我们在Cocos2dx的框 架代码中看不到渲染线程的诞生过程，这是因为这一过程是在Android SDK层实现的。

我们回顾一下Cocos2dxActivity.init方法的关键代码：

// Cocos2dxGLSurfaceView

this.mGLSurfaceView = this.onCreateView();

// …add to FrameLayout

framelayout.addView(this.mGLSurfaceView);

this.mGLSurfaceView.setCocos2dxRenderer(new Cocos2dxRenderer());


// Set framelayout as the content view

setContentView(framelayout);

Cocos2dxGLSurfaceView是 android.opengl.GLSurfaceView的子类。在android 上做原生opengl es 2.0编程的人应该都清楚GLSurfaceView的重要性。但渲染线程并非是在Cocos2dxGLSurfaceView实例化时被创建的，而是在 setRenderer的时候。

我们来看Cocos2dxGLSurfaceView.setCocos2dxRenderer的实现：

public void setCocos2dxRenderer(final Cocos2dxRenderer renderer) {

this.mCocos2dxRenderer = renderer;

this.setRenderer(this.mCocos2dxRenderer);

}

setRender是Cocos2dxGLSurfaceView父类GLSurfaceView实现的方法。在Android SDK GLSurfaceView.java文件中，我们看到：

public void setRenderer(Renderer renderer) {

checkRenderThreadState();

if (mEGLConfigChooser == null) {

mEGLConfigChooser = new SimpleEGLConfigChooser(true);

}

if (mEGLContextFactory == null) {

mEGLContextFactory = new DefaultContextFactory();

}

if (mEGLWindowSurfaceFactory == null) {

mEGLWindowSurfaceFactory = new DefaultWindowSurfaceFactory();

}

** mRenderer = renderer;
mGLThread = new GLThread(mThisWeakRef);
mGLThread.start();**

}

GLThread的实例是在这里被创建并开始执行的。至于渲染线程都干了些什么，我们可以通过其run方法看到：

@Override

public void run() {

setName("GLThread " + getId());

if (LOG_THREADS) {

Log.i("GLThread", "starting tid=" + getId());

}

try {

guardedRun();

} catch (InterruptedException e) {

// fall thru and exit normally

} finally {

sGLThreadManager.threadExiting(this);

}

}

run方法并没有给我们带来太多有价值的东西，真正有价值的信息藏在guardedRun方法中。guardedRun是这个源文件中规模最为庞 大的方法，但抽取其核心结构后，我们发现它大致就是一个死循环，以下是摘要式的伪代码：

while (true) {

synchronized (sGLThreadManager) {

while (true) {

…. …

if (! mEventQueue.isEmpty()) {

event = mEventQueue.remove(0);

break;

}

}

}//end of synchronized (sGLThreadManager)

if (event != null) {

event.run();

event = null;

continue;

}

if needed

view.mRenderer.onSurfaceCreated(gl, mEglHelper.mEglConfig);

if needed

view.mRenderer.onSurfaceChanged(gl, w, h);

if needed

view.mRenderer.onDrawFrame(gl);

}

在这里我们看到了event、Renderer的三个回调方法onSurfaceCreated、onSurfaceChanged以及 onDrawFrame，后续我们会对这三个函数做详细分析的。

**六、游戏逻辑的入口**

在HelloCpp的Classes下有好多C++代码文件（涉及具体的游戏逻辑），在HelloCpp的android project jni目录下也有Jni胶水代码，那么这些代码是如何和引擎一起互动生效的呢？

上面讲到过，涉及到画面的一些渲染都是在GLThread中进行的，这涉及到onSurfaceCreated、 onSurfaceChanged以及onDrawFrame三个方法。我们看看 Cocos2dxRenderer.onSurfaceCreated方法的实现，该方法会在Surface被首次渲染时调用：

public void onSurfaceCreated(final GL10 pGL10, final EGLConfig pEGLConfig) {

Cocos2dxRenderer.nativeInit(this.mScreenWidth, this.mScreenHeight);

this.mLastTickInNanoSeconds = System.nanoTime();

}

该方法继续调用HelloCpp工程jni目录下的nativeInit代码:

void Java_org_cocos2dx_lib_Cocos2dxRenderer_nativeInit(JNIEnv* env, jobject thiz, jint w, jint h)

{

if (!CCDirector::sharedDirector()->getOpenGLView())

{

CCEGLView *view = CCEGLView::sharedOpenGLView();

view->setFrameSize(w, h);

AppDelegate *pAppDelegate = new AppDelegate();

CCApplication::sharedApplication()->run();

}

else

{

ccGLInvalidateStateCache();

CCShaderCache::sharedShaderCache()->reloadDefaultShaders();

ccDrawInit();

CCTextureCache::reloadAllTextures();

CCNotificationCenter::sharedNotificationCenter()->postNotification(EVENT_COME_TO_FOREGROUND, NULL);

CCDirector::sharedDirector()->setGLDefaultValues();

}

}

这似乎让我们看到了游戏逻辑的入口了：

CCEGLView *view = CCEGLView::sharedOpenGLView();

view->setFrameSize(w, h);

AppDelegate *pAppDelegate = new AppDelegate();

CCApplication::sharedApplication()->run();

继续追踪CCApplication::run方法：

int CCApplication::run()

{

// Initialize instance and cocos2d.

if (! applicationDidFinishLaunching())

{

return 0;

}

return -1;

}

applicationDidFinishLaunching，没错这就是游戏逻辑的入口了。我们得回到Samples代码目录中去找到对应方法 的实现。

//cocos2d-x-2.2.2/samples/Cpp/HelloCpp/Classes/AppDelegate.cpp

bool AppDelegate::applicationDidFinishLaunching() {

// initialize director

CCDirector* pDirector = CCDirector::sharedDirector();

CCEGLView* pEGLView = CCEGLView::sharedOpenGLView();

pDirector->setOpenGLView(pEGLView);

CCSize frameSize = pEGLView->getFrameSize();

… …

// turn on display FPS

pDirector->setDisplayStats(true);

// set FPS. the default value is 1.0/60 if you don't call this

pDirector->setAnimationInterval(1.0 / 60);

// create a scene. it's an autorelease object

CCScene *pScene = HelloWorld::scene();

// run

pDirector->runWithScene(pScene);

return true;

}

的确，在applicationDidFinishLaunching中我们做了很多引擎参 数的设置。接下来大管家CCDirector实例登场，并运行了HelloWorld Scene的实例。但这依旧是初始化的一部分，虽然方法名让人听起来像是某种持续连贯行为：

//cocos2d-x-2.2.2/cocos2dx/CCDirector.cpp

void CCDirector::runWithScene(CCScene *pScene)

{

… …

pushScene(pScene);

startAnimation();

}

void CCDisplayLinkDirector::startAnimation(void)

{

if (CCTime::gettimeofdayCocos2d(m_pLastUpdate, NULL) != 0)

{

CCLOG("cocos2d: DisplayLinkDirector: Error on gettimeofday");

}

m_bInvalid = false;

}

两个方法均只是初始化了某些数据成员变量，并未真正将引擎驱动起来。

**七、驱动引擎**

之所以游戏画面是运动的，那是因为屏幕以较高的帧数刷新的缘故，这样人眼就会看到连续的动作，就和电影的放映原理是一样的。在Cocos2d-x 引擎中这些驱动屏幕刷新的代码在哪里呢？

我们回顾一下之前谈到的GLThread线程，我们说过画面渲染的工作都是由它来完成的。GLThread的核心是guardedRun函数，该 函数以“死循环”的方式调用Cocos2dxRender.onDrawFrame方法对画面进行持续渲染。

我们来看看引擎实现的Cocos2dxRender.onDrawFrame方法：

public void onDrawFrame(final GL10 gl) {

/*

* FPS controlling algorithm is not accurate, and it will slow down FPS

* on some devices. So comment FPS controlling code.

*/

/*

final long nowInNanoSeconds = System.nanoTime();

final long interval = nowInNanoSeconds – this.mLastTickInNanoSeconds;

*/

// should render a frame when onDrawFrame() is called or there is a

// "ghost"

Cocos2dxRenderer.nativeRender();

/*

// fps controlling

if (interval < Cocos2dxRenderer.sAnimationInterval) {

try {

// because we render it before, so we should sleep twice time interval

**Thread.sleep**((Cocos2dxRenderer.sAnimationInterval – interval) / Cocos2dxRenderer.NANOSECONDSPERMICROSECOND);

} catch (final Exception e) {

}

}

this.mLastTickInNanoSeconds = nowInNanoSeconds;

*/

}

这个方法实现得比较奇怪，似乎修改过多次，但最后还是决定只保留了一个方法调用： Cocos2dxRenderer.nativeRender()。从注释掉的代码来看，似乎是想在这个方法中通过Thread.sleep来控制 Render Thread渲染的帧率。但由于控制的不理想，索性就不控制了，让guardedRun真正变成了dead loop。但从HelloCpp Sample运行时的状态显示，画面始终保持在60帧左右，让人十分诧异。据说Cocos2d-x 3.0版本重新设计了渲染这块的机制。(后记：在Android上虽然没有帧数控制，但真正的渲染帧率实际上还受到"垂直同步"信号 – vertical sync的影响。在游戏中，也许强劲的显卡迅速的绘制完一屏的图像，但是没有垂直同步信号的到达，显卡无法绘制下一屏，只有等vsync信号到达，才可以绘制。这样fps实际上要要受到操作系统刷新率值的制约）。

nativeRender从命名来看，这显然是一个C++编写的函数实现。我们只能到jni目录下寻找。

cocos2d-x-2.2.2/cocos2dx/platform/android/jni/ Java_org_cocos2dx_lib_Cocos2dxRenderer.cpp

JNIEXPORT void JNICALL Java_org_cocos2dx_lib_Cocos2dxRenderer_nativeRender(JNIEnv* env) {

cocos2d::CCDirector::sharedDirector()->mainLoop();

}

nativeRender也很简洁，直接调用了CCDirector的mainLoop，也就是说每帧渲染过程中真正干活地是 CCDirector::mainLoop。到此我们终于找到了引擎渲染的驱动器：GLThead::guardedRun，以“死循环”的方式刷新着画面，让我们感受到“动”的魅力。

**八、mainLoop**

进一步我们来看看mainLoop所做的工作。mainLoop是CCDirector类的一个纯虚函数，CCDirector的子类CCDisplayLinkDirector真正实现了 它：

//CCDirector.cpp

void CCDisplayLinkDirector::mainLoop(void)

{

if (m_bPurgeDirecotorInNextLoop)

{

m_bPurgeDirecotorInNextLoop = false;

purgeDirector();

}

else if (! m_bInvalid)

{

drawScene();

// release the objects

CCPoolManager::sharedPoolManager()->pop();

}

}

void CCDirector::drawScene(void)

{

// calculate "global" dt

calculateDeltaTime();

//tick before glClear: issue #533

if (! m_bPaused)

{

m_pScheduler->update(m_fDeltaTime);

}

glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

/* to avoid flickr, nextScene MUST be here: after tick and before draw.

XXX: Which bug is this one. It seems that it can't be reproduced with v0.9 */

if (m_pNextScene)

{

setNextScene();

}

kmGLPushMatrix();

// draw the scene

if (m_pRunningScene)

{

m_pRunningScene->visit();

}

// draw the notifications node

if (m_pNotificationNode)

{

m_pNotificationNode->visit();

}

if (m_bDisplayStats)

{

showStats();

}

kmGLPopMatrix();

m_uTotalFrames++;

// swap buffers

if (m_pobOpenGLView)

{

m_pobOpenGLView->swapBuffers();

}

if (m_bDisplayStats)

{

calculateMPF();

}

}

帧渲染由mainLoop调用的drawScene()完成，drawScene方法根据Scene下的渲染树，根据node的最新属性逐个渲染 node，并调整各个Node的调度定时器数据，细节这里就不详细说明了。

**九、UI线程与GLThread的交互**

用户的屏幕触控动作由UI线程捕捉到，该类事件需要传递给引擎，并由GLThread根据各个画面元素的最新状态重新绘制画面。UI线程负责处理用户交互 事件，并将特定的事件通知GLThread处理。UI线程通过Cocos2dxGLSurfaceView的queueEvent方法，将事件以及处理方 法传递给GLThread执行的。

Cocos2dxGLSurfaceView的queueEvent方法继承自其父类GLSurfaceView：

public void queueEvent(Runnable r) {

mGLThread.queueEvent(r);

}

而GLThread的queueEvent方法实现如下：

public void queueEvent(Runnable r) {

if (r == null) {

throw new IllegalArgumentException("r must not be null");

}

synchronized(sGLThreadManager) {

**mEventQueue.add(r);
sGLThreadManager.notifyAll();**

}

}

该方法将event互斥地放入EventQueue，并通知阻塞在Queue上的线程取货。

运行着的GLThread实例在guardedRun中会从event队列中取出runnable event并run的。


while (true) {

synchronized (sGLThreadManager) {

while (true) {

if (mShouldExit) {

return;

}

if (! mEventQueue.isEmpty()) {

**event = mEventQueue.remove(0);**

break;

}

…….

}

}

… …

if (event != null) {

**event.run();**

event = null;

continue;

}

…

}

Activity的各种事件Pause、Resume、Stop以及View的各种屏幕触控事件都是通过queueEvent传递给GLThread执行的，比如：View的onKeyDown方法：

//Cocos2dxGLSurfaceView.java

@Override

public boolean onKeyDown(final int pKeyCode, final KeyEvent pKeyEvent) {

switch (pKeyCode) {

case KeyEvent.KEYCODE_BACK:

case KeyEvent.KEYCODE_MENU:

this.queueEvent(new Runnable() {

@Override

public void run() {

Cocos2dxGLSurfaceView.this.mCocos2dxRenderer.handleKeyDown(pKeyCode);

}

});

return true;

default:

return super.onKeyDown(pKeyCode, pKeyEvent);

}

}

**十、小结**

有了以上的对Cocos2d-x引擎的理解后，再编写游戏代码就更加游刃有余了，至少出现问题时，我们知道应该在哪里查找了。就像对汽车的发动机了如指掌 后，一旦发生动力故障，我们基本知道排除的方法。但对发动机了解的再透彻，也不能代表就能设计和生产出好车，游戏也是这样，对引擎了解是一码事，设计和实 现出好游戏是另外一码事。学习引擎只是编写游戏的起点而已。

© 2014, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

涨姿势了！很欣赏博主知其然吃起所以然的态度。博主辛苦了，谢谢分享。

顶下楼主，写得非常好！