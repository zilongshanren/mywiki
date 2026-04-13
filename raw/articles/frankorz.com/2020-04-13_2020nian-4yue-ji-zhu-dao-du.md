---
title: 2020年4月技术导读
url: http://frankorz.com/2020/04/13/2020-04-tech-reading/
author: 文章作者 猫冬
published: '2020-04-13'
source_blog: 萤火之森
source_site: http://frankorz.com/
category: game programming
fetched: '2026-04-13'
---

首先，感谢所有将自己时间贡献在知识分享的人们。

本文将简单地介绍下最近我看到的想学的、有意思的教程、视频等，内容不仅限于游戏开发。大家可以做个参考，说不定其中就能找到适合自己的教程，进一步打算接下来的学习。

这个文章类型和之前写的都不一样，一方面有自己时间少、沉淀不够、不能持续输出的原因，另一方面是因为这些东西都比较碎，也不好在记录生活的微博上发布一些专业的东西。至于这个导读会不会成为一个系列来更新，还要看看我有没有足够东西来分享啦。

# 书籍

## 《程序员修炼之道（第2版）》

在我经过了入门阶段之后，发现很多以前学的很多教程，都很难在工作中进行参考。恰巧云风翻译的第二版已经出版了，里面的内容让我对编程“修炼”有了更深的理解。

投资知识，收益最佳。


——本杰明·富兰克林

![http://img.frankorz.com/invest-knowledge.png](../../assets/c710cd920ed4d834.png)


学习学习再学习！

## 游戏开发：世嘉新人培训教材

这本书我从 17 年等到现在，三年了，拿到手之后觉得所有的等待都是值得的。

从第一章就能看出作者踏实的编程功底和力求和对优化的不倦追求。一个命令行推箱子游戏从过程式的实现，到运用 C++风格的面向对象的实现，到章节末为了讲解底层内存存储结构而把项目中所有变量都存在一个内存数组中的实现。从中作者讲解基础的 C++ 语法、位运算、指针和引用的异同等概念。

接下来的章节，作者还讲解 2D 图形处理、状态、碰撞、数学等等游戏密不可分的章节，由于作者都为章节提供了类库，因此不必担心书是否会过时，读者只需踏踏实实跟着作者打基础即可。

虽然我很少写 C++，也清楚学 C++ 在游戏开发中是逃不开的，干脆就啃这本书的同时把 C++ 也给上手了，一箭双雕！

## Data-Oriented Design

一本深度讲解面向数据设计的书籍，当你熟悉了面向对象编程，可以尝试看看这本书，用一种不同的思维方式看待你的数据。Unity 开发者在 ECS 正式版公布之前，也可以先深入了解一下面向数据设计的模式。

作者在其网站公开了书籍内容，地址为：[Data-Oriented Design](https://www.dataorienteddesign.com/dodbook/)

同时也可以参考这篇导读：[Highly recommended read : dataorienteddesign.com/dodbook](http://dataorienteddesign.com/dodbook)

# 公开课

## 图形学

游戏编程类书籍涉及的内容太杂，不适合用作专门学习图形学的参考资料。OpenGL / Shader 确实是应该学习的内容，但是以我的理解来看，更适合先入门图形学基础之后再去进一步学习，这样会简单很多。这也是我个人的理念：我们要学的是图形学，而不是图形学 API，这两者应该完全分开看待。另外 OpenGL / Shader 这块学多了会容易让人产生理解偏差，觉得图形学就等于实时渲染（当然是错的，但是很多人真的这么认为！）。


于是闫老师发布了一门公开课：“GAMES101: 现代计算机图形学入门”。

本课程将全面而系统地介绍现代计算机图形学的四大组成部分：（1）光栅化成像，（2）几何表示，（3）光的传播理论，以及（4）动画与模拟。每个方面都会从基础原理出发讲解到实际应用，并介绍前沿的理论研究。通过本课程，你可以学习到计算机图形学背后的数学和物理知识，并锻炼实际的编程能力。


课程作业系统：[GAMES2020在线课程：计算机图形学（闫令琪）课程作业系统](http://www.smartchair.org/GAMES2020Course-YLQ/)

## 国外 MIT CMU 部分课程翻译

[Simviso](https://www.simtoco.com/#/home) 是一个翻译国外课程的民间组织，目前已经翻译了：[MIT 6.004 计算机组成原理](https://www.bilibili.com/video/av75384920)、[MIT 6.824 分布式系统 2020](https://www.bilibili.com/video/av91748150)、[CMU数据库15-445/645](https://www.bilibili.com/video/BV1f7411z7dw)、[斯坦福编译原理](https://www.bilibili.com/video/BV1cE411f78c) 等顶级教程。他们接下来的翻译计划也在 [simviso 国外MIT CMU 斯坦福计算机科班顶级课程翻译系列](https://zhuanlan.zhihu.com/p/122550750) 中提到。（我在想这一段字的知识浓度得有多高 Orz）

原理性的东西参考这些教程最好不过了，我们还可以跟着课程手写一个数据库、CPU 等等。

# 教程

## Custom SRP

Catlike Coding 的教程一向是从基础讲到进阶应用，在 SRP 的主题中，他写了不少基于 Unity 2019 版本的自定义渲染流水线的教程，目前还在持续更新。

## Ray Tracing In One Week

跟着 [Ray Tracing In One Week](https://raytracing.github.io/books/RayTracingInOneWeekend.html) 系列教程一步步来做个光线追踪器，也可以在学完上面图形学公开课中的光线追踪部分后来看这个教程作为补充。这个教程也可以用 Unity 来做，例如我的 [Latias94/RayTracingInOneWeekWithUnity](https://github.com/Latias94/RayTracingInOneWeekWithUnity)，虽然只跟到第八章 = =。

跟完这个教程之后，如果对进一步的 DOTS、优化方面学习感兴趣的话，我还提供了下面四篇文章/项目作为参考。

[Daily Pathtracer](https://aras-p.info/blog/2018/03/28/Daily-Pathtracer-Part-0-Intro/)- 跟着 aras-p 做一个 C# + burst 路径追踪器，还可以参考一下陈嘉栋老师的介绍：
[《Daily Pathtracer！安利下不错的Pathtracer学习资料》](https://zhuanlan.zhihu.com/p/37462611)

- 跟着 aras-p 做一个 C# + burst 路径追踪器，还可以参考一下陈嘉栋老师的介绍：
[Unity Toy Path Tracer](http://theinstructionlimit.com/unity-toy-path-tracer)- 路径追踪器的另一个实现，该作者想进一步探索 Unity 的 DOTS 技术栈，尤其是 Burst + Job System，对这方面感兴趣的不要错过。

[weekend-tracer](https://github.com/stella3d/weekend-tracer)- 又一个 C# + burst 的路径跟踪器实现。

[GPU Ray Tracing in One Weekend](https://medium.com/@jcowles/gpu-ray-tracing-in-one-weekend-3e7d874b3b0f)- 用 Compute Shader 实现光追的基于 GPU 的实现。


## Go 语言探索万物原理

了解了当前使用的技术，可以扩宽领域，学习一些和项目不相关的东西，说不定会带来灵感。

### 老司机带你飞系列

Github 地址：[happyer/distributed-computing](https://github.com/happyer/distributed-computing)

[《老司机带你用 Go 语言实现 MapReduce 框架》](https://github.com/happyer/distributed-computing/blob/master/src/mapreduce)[《老司机带你用 Go 语言实现 Raft 分布式一致性协议》](https://github.com/happyer/distributed-computing/blob/master/src/raft)[《老司机带你用 Go 语言实现 Paxos 算法》](https://github.com/happyer/distributed-computing/blob/master/src/paxos)[《老司机带你用 Go 语言实现分布式数据库》](https://github.com/happyer/distributed-computing/blob/master/src/shardkv)

### 7 天用 Go 动手写/从零实现系列

Github 地址：[geektutu/7days-golang](https://github.com/geektutu/7days-golang)

- 7天用Go从零实现Web框架 - Gee
- 7天用Go从零实现分布式缓存 GeeCache
- 7天用Go从零实现ORM框架 GeeORM

# 视频

[【双语】纪念碑谷的关卡创作挑战 | Monument Valley’s Level Design | Mix and Jam](https://www.bilibili.com/video/av77692640)- Mix and Jam 用六分钟清晰地讲解了纪念碑谷制作思路，并提供了
[项目](https://github.com/mixandjam/MonumentValley-LevelDesign)参考。

- Mix and Jam 用六分钟清晰地讲解了纪念碑谷制作思路，并提供了

# 文章

[Ray Wenderlich - Introduction to Shaders in Unity](https://www.raywenderlich.com/5671826-introduction-to-shaders-in-unity)- Ray Wenderlich 的教程通常会提供初始项目，手把手带你写代码，加上独特风格的配图，很适合用来入门某个技术。这次带来的是如何写 Unity Shaders，实现一个简单的水流 Shader。


# 最后

看了看内容，这次分享的视频和文章都偏少了，其实主要是想分享前面的书籍和公开课，有机会的话有价值的视频和文章我也会多关注，并且分享到导读中。如果你喜欢这系列，或者想对这个系列有其他的想法，欢迎在评论区告诉我。