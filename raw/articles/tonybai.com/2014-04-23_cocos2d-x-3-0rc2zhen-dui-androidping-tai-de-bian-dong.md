---
title: Cocos2d-x 3.0rc2针对Android平台的变动
url: https://tonybai.com/2014/04/23/changes-in-cocos2dx-3-rc2-for-android/
published: '2014-04-23'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Cocos2d-x 3.0rc2针对Android平台的变动

《[Hello, Cocos2d-x 3.0](http://tonybai.com/2014/04/22/hello-cocos2dx-3-rc0/)》一文发出后没多久，我就迫不及待地将手头的一个习作尝试从2.2.2版本迁移到3.0rc0引擎上。

核心代码迁移相对顺利，大致流程如下：

*** 创建项目**

1) cd cocos2d-x-3.0rc0；

2) 执行setup.py，设置引擎依赖的环境变量，脚本会将COCOS_CONSOLE_ROOT和ANT_ROOT写入到~/.bash_profile中； 执行source ~/.bash_profile使得环境变量生效；

3) 在cocos2d-x-3.0rc0下建立projects目录；

4) 利用cocos2d-console工具建立新项目： cocos new GameDemo -p com.tonybai.game.gamedemo -l cpp -d ./projects

5) cd ./projects/GameDemo，我们可以看到项目目录结构如下：

bin/ Classes/ CMakeLists.txt cocos2d/ proj.android/

proj.ios_mac/ proj.linux/ proj.win32/ Resources/

6) 执行cocos compile -p android -j 4 –ap 19 -m release，这个Demo的apk就会被生成，大致就是一个cpp-empty-test；


** * 代码移植**


代码移植的主要工作包括：

1) 改名

带有CC前缀的类名大都要将前缀去掉；

各主要类的单例方法sharedXXXX都改为getInstance；

2) 菜单、按钮事件处理

由menu_selector(GameScene::menuStartCallback) 改为CC_CALLBACK_1(GameScene::menuStartCallback, this)；

3) 触屏事件处理

在Cocos2d-x 2.2.2中，我们直接使用Layer的setTouchEnabled(true)，并Override 三个触屏事件处理函数；

在新版引擎中，我们需要建立事件Listener，并将Listener注册到全局EventDispatcher中，诸如：

auto listener = EventListenerTouchOneByOne::create();

listener->setSwallowTouches(true);

listener->onTouchBegan = CC_CALLBACK_2(GameLayer::onTouchBegan, this);

listener->onTouchMoved = CC_CALLBACK_2(GameLayer::onTouchMoved, this);

listener->onTouchEnded = CC_CALLBACK_2(GameLayer::onTouchEnded, this);

Director::getInstance()->getEventDispatcher()->addEventListenerWithSceneGraphPriority(listener, this);

然后将这里的三个事件处理方法实现出来即可。

核心功能迁移后，GameDemo在[genymotion](http://www.genymotion.com/) 4.4 Android模拟器以及真机上都能正常运行，在模拟器上能保持40左右的帧率，在真机上帧率一直在60左右。玩了一会后，感觉引擎渲染性能的确有提升， 而且这种提升是可以在真机上直观感受到的。

不过好景不长，我又尝试将GameDemo在genymotion 2.3.7 Android上运行，这回得到的结果却是：**黑屏**。 又将Cocos2d-x 3.0rc0自带的cpp-empty-test编译后放到模拟器上运行，得到了同样的黑屏结果，显然这可能是rc0的一个问题。在Cocos2d-x forum上粗略搜到的结果是：升级到最新版本可以解决黑屏问题。于是到官方下载目前最新发布版Cocos2d-x 3.0rc2。这里也吐槽一下：cocos2d-x引擎包Size太大了，似乎也没有提供什么patch文件，导致每发一个版本都要下载几百M的包。官方[ git repository](https://github.com/cocos2d/cocos2d-x)也太大了，尝试clone了几次都失败了，最终还只能下载源码的zip包。

Cocos2d-x 3.0rc2下载解压后，先编译了一下cpp-empty-test，然后部署到Android 2.3.7上运行，这回“黑屏”的确不见了，看来rc2修正了这个问题。接下来就是将我的GameDemo移植到rc2上了。

我用解压后的“cocos2d-x 3.0rc2”替换GameDemo下的cocos2d，然后运行cocos compile编译，install到模拟器行运行，程序启动失败，从monitor logcat中看到一行错误日志：

“ANativeActivity_onCreate not found”

怎么会呢？ANativeActivity_onCreate是由NDK的 native_app_glue static library提供的，怎么会找不到呢？

于是乎打开GameDemo/cocos2d/cocos/2d/platform/android/Android.mk打算查看一下究竟：

LOCAL_WHOLE_STATIC_LIBRARIES := cocos_png_static cocos_jpeg_static cocos_tiff_static cocos_webp_static

include $(BUILD_STATIC_LIBRARY)

$(call import-module,jpeg/prebuilt/android)

$(call import-module,png/prebuilt/android)

$(call import-module,tiff/prebuilt/android)

$(call import-module,webp/prebuilt/android)

Android.mk内容中居然没有将native_app_glue列入，又翻看了一下cocos2d-x 3.0rc0中的同位置Android.mk，后者是有native_app_glue的库依赖的。难道是rc2这块忘记了？于是我尝试将 native_app_glue依赖加上：

LOCAL_WHOLE_STATIC_LIBRARIES := android_native_app_glue cocos_png_static cocos_jpeg_static cocos_tiff_static cocos_webp_static

include $(BUILD_STATIC_LIBRARY)

$(call import-module,jpeg/prebuilt/android)

$(call import-module,png/prebuilt/android)

$(call import-module,tiff/prebuilt/android)

$(call import-module,webp/prebuilt/android)

$(call import-module,android/native_app_glue)

再次尝试编译，不过这次连编译都没能通过，错误的build结果如下：

/home1/tonybai/android-dev/adt-bundle-linux-x86_64/android-ndk-r9c/sources/android/native_app_glue/android_native_app_glue.c:232: error: undefined reference to '**android_main**'

collect2: error: ld returned 1 exit status

make: *** [obj/local/armeabi/libgamedemo.so] Error 1

从结果来看，链接器没能找到native_app_glue中android_main对 应的函数体定义。android_main可是cocos2d-x 3.0引擎提供的实现啊。于是乎再次进入到rc2引擎代码中查找原因，结果却让我很是吃惊：**“NativeActivity被引擎移除了”！**cocos2d/cocos/2d/platform /android目录下面已经没有了nativeactivity.h和nativeactivity.cpp了：

$ ls -F cocos2d/cocos/2d/platform/android

Android.mk CCApplication.h CCDevice.cpp CCFileUtilsAndroid.h CCGLView.cpp CCPlatformDefine.h java/ jni/

CCApplication.cpp CCCommon.cpp CCFileUtilsAndroid.cpp CCGL.h CCGLView.h CCStdC.h javaactivity.cpp

我们看到了一个新文件：javaactivity.cpp，打开该文件，我们发现了和cocos2d-x 2.2.2版本类似的名字：Java_org_cocos2dx_lib_Cocos2dxRenderer_nativeInit。难道rc2针对 Android平台的引擎入口代码回退到2.x版本的设计了？于是乎赶紧进到/cocos2d/cocos/2d/platform/android/java/src/org/cocos2dx/lib目 录下一看究竟。

果不其然，一切看起来都那么的熟悉：Cocos2dxActivity.java、Cocos2dxGLSurfaceView.java、 Cocos2dxRenderer.java….。自此可以断定，rc2中Android平台的引擎设计退回到了2.x版：

– 你的GameActivity要集成Cocos2dxActivity；

– mGLSurfaceView.setCocos2dxRenderer(new Cocos2dxRenderer())时，GLThread(渲染线程)诞生

– 死循环调用Cocos2dxRenderer.onDrawFrame

– 引擎逻辑就在Cocos2dxRenderer.onDrawFrame中被执行。

关于2.2.2版Cocos2dx引擎的结构说明可以参考我的《[Hello, Cocos2d-x](http://tonybai.com/2014/03/11/hello-cocos2dx/)》一文。

回到了2.2.2版本设计的引擎在性能上是否会像rc0那样给人以直观提升的感觉呢，即便渲染器是新写的？真机测试的结果表明，没有直观感觉到提 升。难道是Native Thread(pthread_create创建）和Java Thread之间的差别？不得而知，后续慢慢体会吧。

另外要提一句：javaactivity.cpp将以往2.2.2版本放在项目jni中的 Java_org_cocos2dx_lib_Cocos2dxRenderer_nativeInit挪到了引擎中，本来就是基本不变的代码， 放在引擎中的确更好。rc2的设计回归也有一定好处，一是以前对引擎的认识还适用，二呢就是适合集成在2.2.2版本中的第三方工具的方法应该同样适合3.0rc2版本，这样移 植成本估计会小些。这样我们针对新的3.0引擎，重点还是去关注渲染器、事件分发机制以及物理引擎的变化吧。

最后要做的一件事，就是将上一篇blog的名字做下修改，那篇文章的分析只能对3.0rc0版本有效了，对后续版本无效，已经不能代表3.0的引 擎结构了。事实上NativeActivity是在rc1就被[移除](https://github.com/cocos2d/cocos2d-x/commit/98dfa2c5091cae4ab9e590eabeacca59e46542f8)了，这种较大的改动让人始料不急。这么大的改动，这么短时间发布，让人对目前的 3.0引擎，至少是Android版本引擎的质量表示些许担忧啊。不知道3.0正式版中这块的代码会变啥样，拭目以待吧。

BTW，rc2版本cpp-empty-test在Android 2.3.7模拟器上的帧数在10帧以下，我的Demo也只有5帧，而在4.4版本模拟器上，可以达到40帧，还好还好。

© 2014, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论