---
title: iOS 应用程序生命周期
url: http://frankorz.com/2015/11/03/iOS-application-life-cycle/
author: 文章作者 猫冬
published: '2015-11-03'
source_blog: 萤火之森
source_site: http://frankorz.com/
category: game programming
fetched: '2026-04-13'
---

## 应用生命周期

作为应用程序的委托对象，AppDelegate类在应用生命周期的不同阶段会回调不同的方法。

### 五种状态

iOS的应用程序一共有5种状态:

- Not Running(非运行状态)。应用没有运行或被系统终止。
- Inactive(前台非活动状态)。应用正在进入前台状态，但是还不能接受事件处理。
- Active(前台活动状态)。应用进入前台状态，能接受事件处理。
- Background(后台状态)。应用进入后台后，依然能够执行代码。如果有可执行的代码，就会执行代码，如果没有可执行的代码或者将可执行的代码执行完毕，应用会马上进入挂起状态。有的程序经过特殊的请求后可以长期处于Backgroud状态。
- Suspended(挂起状态)。处于挂起的应用进入一种“冷冻”状态,不能执行代码。如果系统内存不够,系统就把挂起的程序清除掉，为前台程序提供更多的内存，应用会被终止。

### iOS应用状态图

![](../../assets/b592bd16fce9fec5.jpg)


### 应用回调的方法和本地通知

以下是状态跃迁过程中六个应用回调的方法和本地通知：

![](../../assets/8599f270b2417884.jpg)


### 应用程序的运行状态

我们可以在“AppDelegate.m”文件中查看应用程序运行状态的方法，并为其添加日志输出，其中注释为官方注释，注意理解( ͒•ㅈ• ͒)

1 |
|

打开程序：

![](../../assets/71db714f7ffdcaac.jpg)


按下Home键：

![](../../assets/695839b2811bafed.jpg)


从界面重点图标打开程序：

![](../../assets/3ebf1298db93eae1.jpg)


## 非运行状态——应用启动场景

场景描述：用户点击应用图标的时候，可能是第一次启动这个应用，也可能是应用终止后再次启动。该场景的状态跃迁过程见下图，共经历两个阶段3个状态：Not running→Inactive→Active。

- 在Not running→Inactive阶段。调用application:didFinishLaunchingWithOptions:方法，发出 UIApplicationDidFinishLaunchingNotification通知。
- 在Inactive→Active阶段。调用applicationDidBecomeActive:方法，发出UIApplicationDidBecomeActiveNotification通知。

![](../../assets/bf414ddeede8d219.jpg)


### Active和Inactive的切换

应用程序在前台时有2种状态：Active和Inactive。大多数情况下，Inactive状态只是其他两个状态切换时出现的短暂状态（不是任意两个状态之间的切换都会进入Inactive），如打开应用，它会从Not Running先进入Inactive再进入Active；如前后台应用切换时，Inactive会在Active和Background之间短暂出现。

但是也有其他情况，Active和Inactive可以在前台运行时进行切换，比如系统弹出Alert，此时应用会从Active切换到Inactive，直到用户确认再返回Active；再如用户拉下通知页，也会发生Active和Inactive的切换；还有来电但拒接、双击Home键但返回原应用等都不进入Background，而只是在Active和Inactive切换，这个在下面会讲到~

在应用状态跃迁的过程中，iOS系统会回调AppDelegate中的一些方法，并且发送一些通知。实际上，在应用的生命周期中用到的方法和通知很多。

## 点击Home键——应用退出场景

场景描述：应用处于运行状态(即Active状态)时，点击Home键或者有其他的应用导致当前应用中断。该场景的状态跃迁过程可以分成两种情况：可以在后台运行或者挂起，不可以在后台运行或者挂起。根据产品属性文件(Info.plist)中的相关属性 Application does not run in background 是与否可以控制这两种状态。如果采用文本编辑器打开Info.plist文件该设置项对应的键是UIApplicationExitsOnSuspend。

![](../../assets/2239e003451af1ed.jpg)


程序只要符合以下情况之一，只要进入后台或挂起状态就会终止：

- iOS4.0以前的系统
- app是基于iOS4.0之前系统开发的。
- 设备不支持多任务
- 在Info.plist文件中，程序包含了UIApplicationExitsOnSuspend 键。

app如果终止了，系统会调用app的代理的方法 `applicationWillTerminate:`

这样可以让你可以做一些清理工作，你可以保存一些数据或app的状态。这个方法也有5秒钟的限制，超时后方法会返回程序从内存中清除。

注意：用户可以手工关闭应用程序。

添加了UIApplicationExitsOnSuspend键，并设置Yes。打开应用后再按Home键退出：

![](../../assets/97919f2f53212ed7.jpg)


### 状态跃迁的第一种情况

应用可以在后台运行或者挂起，共经历3个阶段4个状态:Active → Inactive → Background → Suspended。

- 在Active→Inactive阶段。调用applicationWillResignActive:方法,发出UIApplicationWillResignActiveNotification通知。
- 在Inactive→Background阶段。应用从非活动状态进入到后台(不涉及我们要重点说明的方法和通知)。
- 在Background→Suspended阶段。调用applicationDidEnterBackground:方法，发出UIApplicationDidEnterBackgroundNotification通知。

![](../../assets/cd9d1b0b50c89874.jpg)


#### 当应用程序进入后台时，我们应该做些什么呢？

保存用户数据或状态信息，所有没写到磁盘的文件或信息，在进入后台时，最后都写到磁盘去，因为程序可能在后台被杀死，释放尽可能释放的内存。

`applicationDidEnterBackgound: `

方法有大概5秒的时间让你完成这些任务。如果超过时间还有未完成的任务，你的程序就会被终止而且从内存中清除。如果还需要长时间的运行任务，可以调用 `beginBackgroundTaskWithExpirationHandler`

方法去请求后台运行时间和启动线程来运行长时间运行的任务。

#### 应用程序在后台时的内存使用

在后台时，每个应用程序都应该释放最大的内存。系统努力的保持更多的应用程序在后台同时运行。不过当内存不足时，会终止一些挂起的程序来回收内存，那些内存最大的程序首先被终止。

事实上，应用程序应该的对象如果不再使用了，那就应该尽快的去掉强引用，这样编译器可以回收这些内存。如果你想缓存一些对象提升程序的性能，你可以在进入后台时，把这些对象去掉强引用。

下面这样的对象应该尽快的去掉强引用：

- 图片对象
- 你可以重新加载的 大的视频或数据文件
- 任何没用而且可以轻易创建的对象

在后台时，为了减少程序占用的内存，系统会自动在回收一些系统帮助你开辟的内存。比如：

- 系统回收Core Animation的后备存储。
- 去掉任何系统引用的缓存图片
- 去掉系统管理数据缓存强引用

### 状态跃迁的第二种情况

应用不可以在后台运行或者挂起，共经历4个阶段5个状态:Active → Inactive → Background → Suspended→ Not running 。

- 在Active→Inactivd阶段。应用由活动状态转为非活动状态(不涉及我们要重点说明的方法和通知)。
- 在Inactive→Background阶段。应用从非活动状态进入到后台(不涉及我们要重点说明的方法和通知)。
- 在Background→Suspended阶段。调用applicationDidEnterBackground:方法，发出UIApplicationDidEnterBackgroundNotification通知。
- 在Suspended→Not running阶段。调用applicationWillTerminate:方法，发出UIApplicationWillTerminateNotification通知。

![](../../assets/f928d570d08b9c83.jpg)


iOS在iOS 4之前不支持多任务，点击Home键时，应用会退出并中断；而在iOS 4之后(包括iOS 4)，操作系统能够支持多任务处理，点击Home键应用会进入后台但不会中断(内存不够的情况除外)。

应用在后台也可以进行部分处理工作，处理完成则进入挂起状态。

## 挂起重新运行场景

挂起状态的应用重新运行。该场景的状态跃迁过程如图2-26所示,共经历3个阶段4个状态:

Suspended → Background → Inactive → Active。

- Suspended→Background阶段。应用从挂起状态进入后台(不涉及我们讲述的这几个方法和通知)。
- Background→Inactive阶段。调用applicationWillEnterForeground:方法，发出UIApplicationWillEnterForegroundNotification通知。
- Inactive→Active阶段。调用applicationDidBecomeActive:方法,发出UIApplicationDidBecomeActiveNotification通知。

![](../../assets/5a8efa8e08ca3304.jpg)


## 内存清除——应用终止场景

场景描述：应用在后台处理完成时进入挂起状态（这是一种休眠状态），如果这时发出低内存警告，为了满足其他应用对内存的需要，该应用就会被清除内存从而终止运行。

![](../../assets/5e0158d315f04b3b.jpg)


内存清除的时候应用终止运行。内存清除有两种情况，可能是系统强制清除内存，也可能是由使用者从任务栏中手动清除（即删掉应用）。内存清除后如果应用再次运行，上一次的运行状态不会被保存，相当于应用第一次运行。

在内存清除场景下，应用不会调用任何方法，也不会发出任何通知。

## 参考文章

[iOS应用程序生命周期(前后台切换,应用的各种状态)详解](http://blog.csdn.net/totogo2010/article/details/8048652)

《iOS开发指南：从零基础到App Store上架（第2版 ）》