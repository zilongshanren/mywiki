---
title: 属于 Unity 的 Flutter——UIWidgets
url: http://frankorz.com/2019/04/01/uiwidgets-practice/
author: 文章作者 猫冬
published: '2019-04-01'
source_blog: 萤火之森
source_site: http://frankorz.com/
category: game programming
fetched: '2026-04-13'
---

## 介绍

[UIWidgets](https://github.com/UnityTech/UIWidgets/) 是 Unity 的一个插件包，是一个从 Google 的移动 UI 框架 Flutter 演变过来的 UI 框架。

相对于原生开发的高开发成本（不同平台都需要不同的一套代码），Flutter、React-Native 等这种跨平台 UI 框架应运而生。

Flutter 自 2018 年 3 月发布以来，社区不断壮大。由于 Flutter 自身设计理念的出色，Unity 中国已经着手将其移植过来。当然了，也因为这两个东西都非常的年轻，因此开发的时候都像开荒一样。

## 框架图

Flutter 有自己的一套渲染系统，那么 Unity 作为一个游戏引擎，底层的图形 API 用自己的一套东西就行了，因此移植过来更方便了。

### Flutter 框架结构

![](../../assets/e2e3cf23bc9ed88e.png)


### UIWidgets 框架结构

![](../../assets/e52ec98550aa3ecb.png)


## 执行效率

![](../../assets/2fd1971af3192acb.gif)


这里提一些基础的知识：

Batch 就是 DrawCall 的另一种说法，了解渲染流水线的同学会知道流水线在 CPU 与 GPU 之间通信时，一般有三个步骤：

- 把数据加载到显存中。
- 设置渲染状态。
- 调用 Draw Call

Draw Call 就是一个调用命令，让 CPU 告诉 GPU 要怎么样用给定的渲染状态和输入的顶点信息来计算。Batch 里面装着顶点信息，也就是 DrawCall 中 GPU 需要的顶点信息。

DrawCall 可以在 Profiler 中看，Batches 可以在 Stats 窗口看，大家可以仔细看看上面动图（右键在新标签页打开图片）里面的数据变化。

![](../../assets/d565bccc42277635.png)


在我随便写的一个例子中间，可以看到 Batches 数只有 1 。即使在有动画的时候 Batches 会多一点，但动画停止后 DrawCall 和 Batches 都马上下来了。这也有我这个应用写的太简单的原因，但是这种效率还是非常值得期待的。

### 组件树

学过前端的同学应该熟悉组件树，这里就不介绍了。

为了更高的渲染效率，Unity 采用了 Render Object Compositiing 的技术。

![](../../assets/81b3dbf0d49da5cd.png)


如果一个子树没有发生改变，Unity 就会将其渲染到一个离屏的 Render Texture 上缓存下来，需要的时候再将其贴到屏幕上。

相比之下，以前的做法是，Canvas 只要有 UI element 改动了，整个 Canvas 都需要重新绘制。即使也有一种优化做法是准备两个 Canvas 分别绘制动态 UI element 和 静态 UI element，但这样也存在很多手动管理的地方。

另外一方面，你可能也意识到了，我们不需要再管什么用同一个材质等等来优化图的合批，UIWidgets 会自动来管理这些事情。这方面也跟 [FairyGUI](http://fairygui.com) 非常像，开发者能专注在生产效率上，让插件来管理麻烦的事情。

## 优点

- 能开发游戏以外的 APP
- 游戏中的 UI
- 新的用户体验
- 不用管渲染过程，提升效率
- 因为是 Unity 的插件，可以轻松加各种粒子效果和其他骚操作。
- 一套代码能跑在游戏中、APP 中、网页中和 Unity 的 Editor 窗口中。（开发者还用其做了一个
[Unity 中文文档的网站](https://github.com/UnityTech/DocCN)，一套代码能用在网页上和 APP 端） - 在静态页面进行降帧的优化，有动画效果再把帧率提上来。
- 和 Flutter 的 API 几乎一样，可以参考 Flutter 教程来用 UIWidgets 搭应用。

## 缺点

- 无论是 Flutter 还是 UIWidgets 都还很年轻，有很多组件 UIWidgets 还没移植过来（GridView、Circle Avatar 等等）
- 官方示例、文档还没完善
- 开发时是开荒模式，所以可能忍不住直接转用 Flutter 去了…

## 我的示例

![](../../assets/2fa8077772cb6ee2.gif)


这里借用了 [ミライ小町](https://github.com/Miraikomachi/MiraikomachiUnity) 的模型，所以代码窗口大小会比较大。（项目里面还有ミライ小町的跳舞动画 animation！）

项目仓库：[Latias94/UIWidget-Practice](https://github.com/Latias94/UIWidget-Practice)

UIWidgets：[UnityTech/UIWidgets](https://github.com/UnityTech/UIWidgets/)