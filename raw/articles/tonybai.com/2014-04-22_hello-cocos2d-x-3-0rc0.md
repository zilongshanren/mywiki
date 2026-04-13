---
title: Hello, Cocos2d-x 3.0rc0
url: https://tonybai.com/2014/04/22/hello-cocos2dx-3-rc0/
published: '2014-04-22'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Hello, Cocos2d-x 3.0rc0

[Cocos2d-x](http://www.cocos2d-x.org) 3.0版本已经发布了[rc2](http://www.cocos2d-x.org/news/207)，这让这段时间用熟了Cocos2d-x 2.2.2的我也有些蠢蠢欲动。按照[触控科技](http://www.chukong-inc.com/)主创人员在CocoaChina2014大会上的讲解，Cocos2d-x 3.0版本相比2.x版本在各方面都有不错的提升，于是乎就想把手头上的一款习作移植到3.0版本引擎下，看看运行效果如何。不过在移植之前，我先来看看 3.0与2.0相比在整体代码结构以及引擎驱动核心方面到底有哪些变化。一旦搞定这些原理，迁移什么都不是问题了。这里以Cocos2d-x 3.0rc0版的Android平台引擎为例。

**一、从NativeActivity开始**

Cocos2d-x 2.x版本中，游戏的Main Activity继承于引擎实现的Cocos2dxActivity（见《[Hello，Cocos2d-x](http://tonybai.com/2014/03/11/hello-cocos2dx/)》），Cocos2dxActivity将一个 GLSurfaceView实例set给Window对象，并在为GLSurfaceView设置Renderer实例时创建Renderer Thread(渲染线程）。而Java代码则通过jni将游戏引擎中的C++代码引入。

Cocos2d-x 3.0版本则进一步摆脱Java束缚，当然也有新渲染器设计方面的考虑，3.0版本直接使用了Android NDK中提供的NativeActivity，我们游戏的主Activity(比如cpp-empty-test中的Cocos2dxActivity) 直接从NativeActivity继承：

// tests/cpp-empty-test/proj.android/src/org/cocos2dx/cpp_empty_test/Cocos2dxActivity.java

public class Cocos2dxActivity extends NativeActivity {

@Override

protected void onCreate(Bundle savedInstanceState) {

// TODO Auto-generated method stub

super.onCreate(savedInstanceState);

… …

//2.Set the format of window

// getWindow().setFormat(PixelFormat.TRANSLUCENT);

}

}

可以看出这里的Cocos2dxActivity啥也没做，因此整个Cocos2d-x 3.0游戏的起点就应该是NativeActivity了。

NativeActivity是Android专为使用NDK开发Android应用而实现的一个Activity类，通过使用 NativeActivity，开发者可以最大程度地摆脱Java代码的编写，尽可能的使用C++代码。

**二、NativeActivity的原理**

NativeActivity在Android 2.3版本引入，其核心方法依旧是onCreate，我们一起来看一下(省略部分与分析无关的代码)：

// NativeActivity.java(Android 4.4.2_r1)

@Override

protected void onCreate(Bundle savedInstanceState) {

**String libname = "main";
String funcname = "ANativeActivity_onCreate";**

ActivityInfo ai;

… …

mNativeContentView = new NativeContentView(this);

mNativeContentView.mActivity = this;

setContentView(mNativeContentView);

mNativeContentView.requestFocus();

mNativeContentView.getViewTreeObserver()

.addOnGlobalLayoutListener(this);


try {

ai = getPackageManager().getActivityInfo(

getIntent().getComponent(),

PackageManager.GET_META_DATA);

if (ai.metaData != null) {

String ln = ai.metaData.getString(META_DATA_LIB_NAME);

if (ln != null) libname = ln;

ln = ai.metaData.getString(META_DATA_FUNC_NAME);

if (ln != null) funcname = ln;

}

} catch (PackageManager.NameNotFoundException e) {

throw new RuntimeException("Error getting activity info", e);

}


String path = null;


File libraryFile = new File(ai.applicationInfo.nativeLibraryDir,

System.mapLibraryName(libname));

if (libraryFile.exists()) {

path = libraryFile.getPath();

}


if (path == null) {

throw new IllegalArgumentException(

"Unable to find native library: " + libname);

}


byte[] nativeSavedState = savedInstanceState != null

? savedInstanceState.getByteArray(KEY_NATIVE_SAVED_STATE) : null;

**mNativeHandle = loadNativeCode**(path, funcname, Looper.myQueue(),

getAbsolutePath(getFilesDir()), getAbsolutePath(getObbDir()),

getAbsolutePath(getExternalFilesDir(null)),

Build.VERSION.SDK_INT, getAssets(), nativeSavedState);

if (mNativeHandle == 0) {

throw new IllegalArgumentException("Unable to load native library: "

+ path);

}

super.onCreate(savedInstanceState);

}

从NativeActivity的onCreate代码我们大致可以看出，NativeActivity在游戏对应的原生库(.so)中查找名为"ANativeActivity_onCreate"的函数，并执行该函数。其执行 是通过loadNativeCode这个Jni方法实现的。loadNativeCode在 /core/jni/android_app_NativeActivity.cpp中有实现：

/core/jni/android_app_NativeActivity.cpp

static jint

loadNativeCode_native(JNIEnv* env, jobject clazz, jstring path, jstring funcName,

jobject messageQueue,

jstring internalDataDir, jstring externalDataDir, int sdkVersion,

jobject jAssetMgr, jbyteArray savedState)

{

LOG_TRACE("loadNativeCode_native");

const char* pathStr = env->GetStringUTFChars(path, NULL);

NativeCode* code = NULL;

void* handle = dlopen(pathStr, RTLD_LAZY);

env->ReleaseStringUTFChars(path, pathStr);

if (handle != NULL) {

const char* funcStr = env->GetStringUTFChars(funcName, NULL);

code = new NativeCode(handle, (ANativeActivity_createFunc*)

**dlsym**(handle, funcStr));

env->ReleaseStringUTFChars(funcName, funcStr);

if (code->createActivityFunc == NULL) {

LOGW("ANativeActivity_onCreate not found");

delete code;

return 0;

}

… …

code->**createActivityFunc**(code, rawSavedState, rawSavedSize);

if (rawSavedState != NULL) {

env->ReleaseByteArrayElements(savedState, rawSavedState, 0);

}

}

return (jint)code;

}

做过系统编程的朋友想必对dlsym都很熟系，这个函数用来从一个打开的.so中(dlopen)获得某个函数对应的代码地址。 code->createActivityFunc则是执行这个函数。

我们在强化一下，费了半天劲儿找到并执行的这个函数的名字是：**ANativeActivity_onCreate**。 如果你要使用NativeActivity，你就必须提供一份ANativeActivity_onCreate函数的实现。在该函数的实现中， 你要为Activity注册各种生命周期事件以及其他输入事件的回调函数，比如onStart、onResume、onDestroy等。NDK 官方文档中有详细的说明。

不过这样一来，所有的事件处理均在NativeActivity所在的主线程里执行，为了不阻塞主线程的页面刷新以及交互响应，我们需要将这些回 调函数实现的短小精悍，不能拖泥带水，不能“干重活儿”。以前使用SDK时，Android SDK提供了AsyncTask, Handler, Runnable, Thread等诸多手段帮助在后台处理一些“重量级”的事情，但在NDK中，我们该如何处理呢？NDK也为我们提供了一种方案： android_native_app_glue。

android_native_app_glue大致做了这么几件事：

1、实现了ANativeActivity_onCreate函数，注册了 Callback函数；

2、创建一个新的子Thread，用于干重活儿

3、在Main Thread和新线程之间建立了一个管道，用于Main Thread给新线程传递各种事件，以便后者读取并处理。

可以说native_app_glue的存在，进一步降低了 NativeActivity的使用门槛，否则以上诸事均要有开发人员自行实现。

下面结合源码做简单说明：

// android-ndk-r9c/sources/android/native_app_glue/android_native_app_glue.c

void ANativeActivity_onCreate(ANativeActivity* activity,

void* savedState, size_t savedStateSize) {

LOGV("Creating: %p\n", activity);

activity->callbacks->onDestroy = onDestroy;

activity->callbacks->onStart = onStart;

activity->callbacks->onResume = onResume;

activity->callbacks->onSaveInstanceState = onSaveInstanceState;

activity->callbacks->onPause = onPause;

activity->callbacks->onStop = onStop;

activity->callbacks->onConfigurationChanged = onConfigurationChanged;

activity->callbacks->onLowMemory = onLowMemory;

activity->callbacks->onWindowFocusChanged = onWindowFocusChanged;

activity->callbacks->onNativeWindowCreated = onNativeWindowCreated;

activity->callbacks->onNativeWindowDestroyed = onNativeWindowDestroyed;

activity->callbacks->onInputQueueCreated = onInputQueueCreated;

activity->callbacks->onInputQueueDestroyed = onInputQueueDestroyed;

activity->instance = **android_app_create**(activity, savedState, savedStateSize);

}

static struct android_app* android_app_create(ANativeActivity* activity,

void* savedState, size_t savedStateSize) {

struct android_app* android_app = (struct android_app*)malloc(sizeof(struct android_app));

memset(android_app, 0, sizeof(struct android_app));

android_app->activity = activity;

pthread_mutex_init(&android_app->mutex, NULL);

pthread_cond_init(&android_app->cond, NULL);

… …

int msgpipe[2];

if (**pipe(msgpipe)**) {

LOGE("could not create pipe: %s", strerror(errno));

return NULL;

}

android_app->msgread = msgpipe[0];

android_app->msgwrite = msgpipe[1];

pthread_attr_t attr;

pthread_attr_init(&attr);

pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_DETACHED);

**pthread_create**(&android_app->thread, &attr, **android_app_entry**, android_app);

// Wait for thread to start.

pthread_mutex_lock(&android_app->mutex);

while (!android_app->running) {

pthread_cond_wait(&android_app->cond, &android_app->mutex);

}

pthread_mutex_unlock(&android_app->mutex);

return android_app;

}

上面的android_app_create创建了子线程，建立了两个线程的pipe，新线程的入口是android_app_entry：

static void* android_app_entry(void* param) {

struct android_app* android_app = (struct android_app*)param;

android_app->config = AConfiguration_new();

AConfiguration_fromAssetManager(android_app->config,

android_app->activity->assetManager);

print_cur_config(android_app);

android_app->cmdPollSource.id = LOOPER_ID_MAIN;

android_app->cmdPollSource.app = android_app;

android_app->cmdPollSource.process = process_cmd;

android_app->inputPollSource.id = LOOPER_ID_INPUT;

android_app->inputPollSource.app = android_app;

android_app->inputPollSource.process = process_input;

ALooper* looper = ALooper_prepare(

ALOOPER_PREPARE_ALLOW_NON_CALLBACKS);

ALooper_addFd(looper, android_app->msgread,

LOOPER_ID_MAIN,

ALOOPER_EVENT_INPUT, NULL,

&android_app->cmdPollSource);

android_app->looper = looper;

pthread_mutex_lock(&android_app->mutex);

android_app->running = 1;

pthread_cond_broadcast(&android_app->cond);

pthread_mutex_unlock(&android_app->mutex);

**android_main(android_app);**

android_app_destroy(android_app);

return NULL;

}

新线程建立了事件处理设施(looper)，并通知主线程（通过条件变量）app正式开始运行了(running = 1)，之后进入**android_main**。

Cocos2d-x 3.0采用的就是android_native_app_glue这 种方案，而android_main则是Cocos2d-x 3.0引擎层的入口。

//cocos/2d/platform/android/Android.mk

LOCAL_WHOLE_STATIC_LIBRARIES := **android_native_app_glue** cocos_png_static cocos_jpeg_static cocos_tiff_static cocos_webp_static

$(call import-module,**android/native_app_glue**)

三**、走进引擎**

从android_main函数开始，我们就进入了Cocos2d-x 3.0引擎的范畴。android_main函数比较长，我们挑重点说：

cocos/2d/platform/android/nativeactivity.cpp

void android_main(struct android_app* state) {

… …

memset(&engine, 0, sizeof(engine));

state->userData = &engine;

state->onAppCmd = engine_handle_cmd;

state->onInputEvent = engine_handle_input;

state->inputPollSource.process = process_input;

engine.app = **state**;

// Prepare to monitor accelerometer

… …

while (1) {

// Read all pending events.

int ident;

int events;

struct android_poll_source* source;

// If not animating, we will block forever waiting for events.

// If animating, we loop until all events are read, then continue

// to draw the next frame of animation.

while ((ident=**ALooper_pollAll**(engine.animating ? 0 : -1,

NULL, &events,

(void**)&source)) >= 0) {

// Process this event.

if (source != NULL) {

source->process(state, source);

}

… …

// Check if we are exiting.

if (state->destroyRequested != 0) {

engine_term_display(&engine);

memset(&engine, 0, sizeof(engine));

s_methodInitialized = false;

**return**;

}

}

if (engine.animating) {

// Done with events; draw next animation frame.

engine.state.angle += .01f;

if (engine.state.angle > 1) {

engine.state.angle = 0;

}

// Drawing is throttled to the screen update rate, so there

// is no need to do timing here.

LOG_RENDER_DEBUG("android_main : engine.animating");

**engine_draw_frame(&engine);**

} else {

LOG_RENDER_DEBUG("android_main : !engine.animating");

}

…

}

}

android_main有些像cocos2d-x 2.2.2中GLThread的guardedRun方法，里面基本上就是一个死循环(while (1))，简化后的逻辑大致如下：

void android_main(struct android_app* state) {

while (1) {

Do Main Thread Event Processing & Input Event Processing;

if (engine.animating) {

// draw next animation frame 画下一帧

engine_draw_frame(&engine);

}

}

}

而引擎的初始化和帧渲染就是在这个死循环中一步步完成的。

引擎的初始化始于APP_CMD_INIT_WINDOW事件，在engine_handle_cmd中，我们可以看到：

static void engine_handle_cmd(struct android_app* app, int32_t cmd)

{

struct engine* engine = (struct engine*)app->userData;

switch (cmd) {

… …

case APP_CMD_INIT_WINDOW:

// The window is being shown, get it ready.

if (engine->app->window != NULL) {

cocos_dimensions d = **engine_init_display**(engine);

if ((d.w > 0) &&

(d.h > 0)) {

cocos2d::JniHelper::setJavaVM(app->activity->vm);

cocos2d::JniHelper::setClassLoaderFrom(app->activity->clazz);

// call Cocos2dxHelper.init()

cocos2d::JniMethodInfo ccxhelperInit;

if (!cocos2d::JniHelper::getStaticMethodInfo(ccxhelperInit,

"org/cocos2dx/lib/Cocos2dxHelper",

"init",

"(Landroid/app/Activity;)V")) {

LOGI("cocos2d::JniHelper::getStaticMethodInfo(ccxhelperInit) FAILED");

}

ccxhelperInit.env->CallStaticVoidMethod(ccxhelperInit.classID,

ccxhelperInit.methodID,

app->activity->clazz);

**cocos_init**(d, app);

}

**engine->animating = 1;**

engine_draw_frame(engine);

}

break;

… …

}

}

当收到主线程通知的窗口建立事件时，engine_handle_cmd的APP_CMD_INIT_WINDOW事件处理函数主要做了两件事：

1、调用engine_init_display初始化EGL；

2、调用cocos_init初始化引擎的主要角色。

这里进入到引擎初始化的前提是“engine->app->window != NULL”。而app->window的设置是在native_app_glue中进行的，大致流程是：

Main Thread：

onNativeWindowCreated

-> android_app_set_window

-> android_app->pendingWindow = window;

-> android_app_write_cmd(android_app, APP_CMD_INIT_WINDOW);

Sub Thread:

process_cmd

-> android_app_pre_exec_cmd

-> android_app->window = android_app->pendingWindow;

-> engine_handle_cmd(即app->onAppCmd回调)，此时android_app->window != NULL。

**四、引擎初始化**

前面说过，引擎初始化包括两部分：engine_init_display和cocos_init，我们分别来说说。

1、**engine_init_display**

//cocos/2d/platform/android/nativeactivity.cpp

static cocos_dimensions engine_init_display(struct engine* engine)

{

cocos_dimensions r;

… …

EGLDisplay display = **eglGetDisplay**(EGL_DEFAULT_DISPLAY);

**eglInitialize**(display, 0, 0);

**eglChooseConfig**(display, attribs, &config, 1, &numConfigs);

**eglGetConfigAttri**b(display, config, EGL_NATIVE_VISUAL_ID, &format);

ANativeWindow_setBuffersGeometry(engine->app->window, 0, 0, format);

surface = **eglCreateWindowSurface**(display, config, engine->app->window, NULL);

const EGLint eglContextAttrs[] =

{

EGL_CONTEXT_CLIENT_VERSION, 2,

EGL_NONE

};

context = **eglCreateContext**(display, config, NULL, eglContextAttrs);

if (**eglMakeCurrent**(display, surface, surface, context) == EGL_FALSE) {

LOGW("Unable to eglMakeCurrent");

return r;

}

eglQuerySurface(display, surface, EGL_WIDTH, &w);

eglQuerySurface(display, surface, EGL_HEIGHT, &h);

engine->display = display;

engine->context = context;

engine->surface = surface;

engine->width = w;

engine->height = h;

engine->state.angle = 0;

r.w = w;

r.h = h;

return r;

}

这段代码应该是典型的EGL初始化流程，几乎每本有关EGL或opengl es的教程中都会有类似描述。个人对opengl以及EGL了解不多，从一些书籍或网络资料中大致得到如下一些理解：

首先，Android下每个Activity都会有对应窗口(Window)以及View，View就是显示在屏幕上的内容。NativeActivity初始化时设置了一个NativeContentView（View的子类）：

// android/app/NativeActivity.java

static class NativeContentView extends View {

NativeActivity mActivity;

public NativeContentView(Context context) {

super(context);

}

public NativeContentView(Context context,

AttributeSet attrs) {

super(context, attrs);

}

}

protected void onCreate(Bundle savedInstanceState) {

… …

mNativeContentView = new NativeContentView(this);

mNativeContentView.mActivity = this;

setContentView(mNativeContentView);

… …

}

但Cocos2d-x显然不会使用这个View，而是直接在窗口用opengl绘图。EGL大致有三个元素：Context、Display以及 Surface。它们之间的大致关系是：EGL通过Context指挥opengl在Surface画布（一种帧缓冲FrameBuffer）上绘制，绘 制完成后再Swap到窗口的Display显示器上去，这样我们就能看到绘制的图像了。2D游戏引擎的渲染器用的都是这个原理。关于上述EGL初始化的具 体调用含义这里就不赘述了，大家如要深入了解，可以找本OpenGL ES相关的书去看看。

**2、cocos_init**

static void cocos_init(cocos_dimensions d, struct android_app* app)

{

LOGI("cocos_init(…)");

pthread_t thisthread = pthread_self();

LOGI("pthread_self() = %X", thisthread);

cocos2d::FileUtilsAndroid::setassetmanager(app->activity->assetManager);

auto director = cocos2d::Director::getInstance();

auto glview = director->getOpenGLView();

if (!glview)

{

glview = cocos2d::GLView::create("Android app");

glview->setFrameSize(d.w, d.h);

director->setOpenGLView(glview);

cocos_android_app_init(app);

cocos2d::Application::getInstance()->run();

}

else

{

cocos2d::GL::invalidateStateCache();

cocos2d::ShaderCache::getInstance()->reloadDefaultShaders();

cocos2d::DrawPrimitives::init();

cocos2d::VolatileTextureMgr::reloadAllTextures();

cocos2d::EventCustom foregroundEvent(EVENT_COME_TO_FOREGROUND);

director->getEventDispatcher()->dispatchEvent(&foregroundEvent);

director->setGLDefaultValues();

}

}

分析过Cocos2d-x 2.x版本引擎结构的朋友对这段代码一定比较眼熟，没错，在2.x版本中这段代码是放在游戏项目的proj.android/jni/下的，在jni方法Java_org_cocos2dx_lib_Cocos2dxRenderer_nativeInit中我们可以看到类似代码。

在cocos_init中我们看到了Cocos2d-x游戏引擎的一个重要角色Director的创建和初始化：

auto director = cocos2d::Director::getInstance();

//cocos/2d/CCDirector.cpp

bool Director::init(void)

{

setDefaultValues();

… …

**_openGLView = nullptr;**

_contentScaleFactor = 1.0f;

// scheduler

_scheduler = new Scheduler();

// action manager

_actionManager = new ActionManager();

_scheduler->scheduleUpdate(_actionManager,

Scheduler::PRIORITY_SYSTEM, false);

_eventDispatcher = new EventDispatcher();

_eventAfterDraw = new EventCustom(EVENT_AFTER_DRAW);

_eventAfterDraw->setUserData(this);

_eventAfterVisit = new EventCustom(EVENT_AFTER_VISIT);

_eventAfterVisit->setUserData(this);

_eventAfterUpdate = new EventCustom(EVENT_AFTER_UPDATE);

_eventAfterUpdate->setUserData(this);

_eventProjectionChanged = new EventCustom(EVENT_PROJECTION_CHANGED);

_eventProjectionChanged->setUserData(this);

//init TextureCache

initTextureCache();

**_renderer = new Renderer;**

_console = new Console;

return true;

}

诸多引擎基础设施都是在Director::init中被初始化的，这里最重要的就是Renderer了，这个就是Cocos2d-x 3.0新实现的渲染器。

Director初始化后，_openGLView == NULL，后续cocos_init调用cocos2d::GLView::create("Android app")创建GLView，并set到Director中。这个View似乎更多是用来辅助处理屏幕适配以及触屏事件处理的。

cocos_init最后调用了cocos_android_app_init(app)，这个函数实现在你的游戏工程中，以cpp-empty- test为例，在tests/cpp-empty-test/proj.android/jni/main.cpp中我们看到了该函数的实现：

void cocos_android_app_init (struct android_app* app) {

LOGD("cocos_android_app_init");

AppDelegate *pAppDelegate = new AppDelegate();

}

我们已经进入游戏业务逻辑层了。和Cocos2d-x 2.x版本一样，Classes/AppDelegate.cpp中的 AppDelegate::applicationDidFinishLaunching依旧是我们初始化我们游戏业务逻辑层的入口。而这一入口函数是在 cocos_init中的cocos2d::Application::getInstance()->run()调用时被调用的。

// /cocos/2d/platform/android/CCApplication.cpp

int Application::run()

{

// Initialize instance and cocos2d.

if (! applicationDidFinishLaunching())

{

return 0;

}

return -1;

}

至此，我们又回到了熟悉的游戏业务逻辑层，也就是你的游戏project中。

**五、到底发生了哪些重要变化**

之前听说Cocos2d-x 3.0引擎的一个重要改造就是尽可能利用多线程，利用硬件的多核来提升游戏渲染性能。这给我的错觉是Renderer Thread完全独立出去，只负责渲染。但实际发布的版本似乎并不是这么回事。Cocos2d-x 2.x版本是两个线程，3.0版本依旧是两个线程，从cpp-empty-test运行的logcat日志也能看出来：

04-21 07:36:52.779 **1522 1522** D dalvikvm: Late-enabling CheckJNI

04-21 07:36:52.783 1522 1522 I dalvikvm: Enabling JNI app bug workarounds for target SDK version 9…

04-21 07:36:52.783 561 573 I ActivityManager: Start proc org.cocos2dx.cpp_empty_test for activity org.cocos2dx.cpp_empty_test/. Cocos2dxActivity: pid=1522 uid=10056 gids={50056}

04-21 07:36:53.047 **1522 1535** D libEGL : loaded /system/lib/egl/libEGL_genymotion.so

04-21 07:36:53.047 1522 1535 D : HostConnection::get() New Host Connection established 0xb918a7c8, tid 1535

04-21 07:36:53.071 1522 1535 D libEGL : loaded /system/lib/egl/libGLESv1_CM_genymotion.so

04-21 07:36:53.083 1522 1535 D libEGL : loaded /system/lib/egl/libGLESv2_genymotion.so

04-21 07:36:53.143 1522 1535 D JniHelper: JniHelper::setJavaVM(0xb903a730), pthread_self() = B9180250

04-21 07:36:53.155 1522 1535 I cocos2dx/nativeactivity.cpp: cocos_init(…)

… …

04-21 07:36:53.395 1522 1535 D main : cocos_android_app_init

04-21 07:36:53.419 1522 1535 D CCFileUtilsAndroid.cpp: relative path = ipadhd/CloseNormal.png

04-21 07:36:53.427 1522 1535 D CCFileUtilsAndroid.cpp: relative path = ipadhd/CloseSelected.png

04-21 07:36:53.439 1522 1535 D cocos2d-x debug info: cocos2d: fullPathForFilename: No file found at Arial. Possible missing file.

04-21 07:36:53.447 1522 1535 D dalvikvm: GC_FOR_ALLOC freed 64K, 4% free 3455K/3584K, paused 7ms, total 7ms

04-21 07:36:53.467 1522 1535 D CCFileUtilsAndroid.cpp: relative path = ipadhd/HelloWorld.png

04-21 07:36:54.003 1522 1535 I cocos2dx/nativeactivity.cpp: engine_draw_frame(…)

04-21 07:36:54.003 1522 1535 I cocos2dx/nativeactivity.cpp: pthread_self() = B9180250

04-21 07:36:54.003 **1522 1535** I cocos2dx/nativeactivity.cpp: engine_draw_frame : just called cocos' mainLoop()

04-21 07:36:54.051 1522 1535 I cocos2dx/nativeactivity.cpp: android_main : engine.animating

04-21 07:36:54.051 1522 1535 I cocos2dx/nativeactivity.cpp: engine_draw_frame(…)

04-21 07:36:54.051 1522 1535 I cocos2dx/nativeactivity.cpp: pthread_self() = B9180250

… …

04-21 07:36:56.507 **1522 1535** I Process : Sending signal. PID: 1522 SIG: 9

可以看出NativeActivity所在的主线程号为1522，但绝大多数工作都在1535这个渲染线程，也就是native_app_glue库中创 建的那个线程。Scene Graph管理和Renderer::render依旧都在该Thread内完成，这似乎也很难有效并充分的利用起多核的效能啊。cpp-empty- test在我的genymotion模拟器上跑时，帧数始终在50帧左右。

不过Renderer的确是重写的，并且将2.x版本中Scene Graph的管理与渲染之间的耦合解耦开来。每帧按Scene Graph Visit Node时并不真正执行渲染，而只是构造DrawCommand，并插入到Renderer的DrawCommand队列中：

// draw

void Sprite::draw(Renderer *renderer, const kmMat4 &transform, bool transformUpdated)

{

// Don't do calculate the culling if the transform was not updated

_insideBounds = transformUpdated ? isInsideBounds() : _insideBounds;

if(_insideBounds)

{

_quadCommand.init(_globalZOrder, _texture->getName(), _shaderProgram, _blendFunc, &_quad, 1, transform);

renderer->addCommand(&_quadCommand);

#if CC_SPRITE_DEBUG_DRAW

_customDebugDrawCommand.init(_globalZOrder);

_customDebugDrawCommand.func = CC_CALLBACK_0(Sprite::drawDebugData, this);

renderer->addCommand(&_customDebugDrawCommand);

#endif //CC_SPRITE_DEBUG_DRAW

}

}

在Director::drawScene尾部我们能看到真正的渲染动作render()被调用：

void Director::drawScene()

{

… …

// draw the scene

if (_runningScene)

{

_runningScene->**visit**(_renderer, identity, false);

_eventDispatcher->dispatchEvent(_eventAfterVisit);

}

**_renderer->render();**

_eventDispatcher->dispatchEvent(_eventAfterDraw);

kmGLPopMatrix();

_totalFrames++;

// swap buffers

if (_openGLView)

{

**_openGLView->swapBuffers();**

}

if (_displayStats)

{

calculateMPF();

}

}

这里我们看到了 _openGLView->swapBuffers()，但该方法的具体实现为空，真正swapBuffers调用在外层：

static void engine_draw_frame(struct engine* engine)

{

LOG_RENDER_DEBUG("engine_draw_frame(…)");

pthread_t thisthread = pthread_self();

LOG_RENDER_DEBUG("pthread_self() = %X", thisthread);

if (engine->display == NULL) {

// No display.

LOGW("engine_draw_frame : No display.");

return;

}

dispatch_pending_runnables();

**cocos2d::Director::getInstance()->mainLoop();**

LOG_RENDER_DEBUG("engine_draw_frame : just called cocos' mainLoop()");

/* // Just fill the screen with a color. */

/* glClearColor(((float)engine->state.x)/engine->width, engine->state.angle, */

/* ((float)engine->state.y)/engine->height, 1); */

/* glClear(GL_COLOR_BUFFER_BIT); */

if (s_pfEditTextCallback && editboxText)

{

s_pfEditTextCallback(editboxText, s_ctx);

free(editboxText);

editboxText = NULL;

}

**eglSwapBuffers(engine->display, engine->surface);**

}

还记得android_main中的“死循环”么？那个死循环在每一帧都会调用engine_draw_frame方法，而这恰是**整个Cocos2d-x 3.0引擎的驱动中心**。

通过汇集各个Node的DrawCommand而不是直接Draw，新渲染器可以做一些优化，比如Batch Renderer等。这在上一版本引擎中较难实现，或者只能显式的通过CCSpriteBatchNode实现。更多的好处可以参考官方说明，或待日后使 用引擎时挖掘。

**六、其他**

Cocos2d-x 3.0引擎的C++部分采用了[C++ 11](http://en.wikipedia.org/wiki/C++11)标准中的语法，因此如果你要编译Linux版本游戏，你需要升级你的gcc编译器到4.7以上版本。但如果只构建Android 游戏，Android NDK(r9c以后版本)早为我们准备好了arm和x86平台的4.8版本的g++编译器了。

Cocos2d-x 3.0的内存管理依旧沿用内存计数机制，如果你理解了2.x版本的内存管理，理解3.0版本应该不会有太大问题。

**七、参考资料**


– Android NDK源码（r9c)

- Cocos2d-x 3.0rc1源码

– Android SDK源码（4.4.2_r1)

– 《[Android Native Development Kit Cookbook — A step-by-step tutorial with more than 60 concise recipes on Android NDK development skills](http://book.douban.com/subject/24672232)》。

© 2014, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论