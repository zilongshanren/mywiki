---
title: Unity 开源双端框架 ET 中初尝热更新技术
url: http://frankorz.com/2019/01/06/hotfix-introduction-of-unity-et-framework/
author: 文章作者 猫冬
published: '2019-01-06'
source_blog: 萤火之森
source_site: http://frankorz.com/
category: game programming
fetched: '2026-04-13'
---

## ET 框架简介

正所谓时势造英雄，在 Web 开发领域或者传统软件开发领域中，人们把经过千锤百炼的代码总结出一套开发框架，从而提高开发效率，让开发者能更专注于业务本身。对于游戏领域而言，不同游戏需求的东西也不一样：有的游戏对性能有着苛刻要求，有的游戏需要快速地迭代出来，有的游戏需要联网热更新等等。因此不同的游戏框架应运而生。

例如：

[Game Framework](https://github.com/EllanJiang/GameFramework)是一个基于 Unity 引擎的游戏框架，主要对游戏开发过程中常用模块进行了封装，很大程度地规范开发过程、加快开发速度并保证产品质量。[QFramework](https://github.com/liangxiegame/QFramework)一套渐进式的快速开发框架。框架内部积累了多个项目的在各个技术方向的解决方案。[Entitas](https://github.com/sschmid/Entitas-CSharp)一套基于 C# 和 Unity 的实体组件系统。[Entities](https://github.com/Unity-Technologies/EntityComponentSystemSamples)Unity 官方的实体组件系统实现，不过还是 Beta 版本，详细介绍可以查看[官网](https://unity.com/unity/features/job-system-ECS)。[StrangeIoC](https://github.com/strangeioc/strangeioc)一套基于 C# 和 Unity 的控制反转 (Inversion-of-Control) 框架。

今天介绍的是 ET 框架。

ET是一个开源的游戏客户端（基于unity3d）服务端双端框架，服务端是使用C# .net core开发的分布式游戏服务端，其特点是开发效率高，性能强，双端共享逻辑代码，客户端服务端热更机制完善，同时支持可靠udp tcp websocket协议，支持服务端3D recast寻路等等


ET 框架能让我们只用 C# 就能搞定前后端，热更新方面也采用了基于 C# 的 IL 运行时——[ILRuntime](https://ourpalm.github.io/ILRuntime/)， 贯彻了 “珍爱生命，远离 Lua” 这句话。目前自己接触的大多是客户端部分，因此服务器方面不做介绍。

## 框架文件结构

[ET 官网](https://github.com/egametang/ET) 本身给了很多介绍，我们可以克隆 Git 仓库到本地。

下面来看看每个文件夹的作用：

![](../../assets/6a437ae653fceac9.png)


## 客户端文件结构

本文主要来介绍客户端，因此进入到 Unity 文件夹，文件夹结构如下：

![](../../assets/a2d3d6b6180fbb82.png)


当前 Master 分支目前需要 Unity 2018.3 以上版本。使用之前需要参考下官方的 [运行指南](https://github.com/egametang/ET/blob/master/Doc/%E8%BF%90%E8%A1%8C%E6%8C%87%E5%8D%97.md)。

在 VS 中重新编译，或者 Rider Rebuild 一下项目。Scene 选择 Scenes\Init.unity，点 Play 按钮应该就能成功运行，看到登陆界面。

![](../../assets/3a0567f8c5a3e615.png)


## 组件设计

ET 框架使用了组件的设计，一切都是实体（Entity）和组件（Component），官方文档 [组件设计](https://github.com/egametang/ET/blob/master/Doc/%E7%BB%84%E4%BB%B6%E8%AE%BE%E8%AE%A1.md) 介绍的很详细。

看完文档，我们来看看项目代码的启动入口。

![](../../assets/eade7ddc62c96ae9.png)


这个 Init.cs 文件，在 Model 文件夹下。可能有同学注意到 Hotfix 文件夹下也有一个 Init.cs 文件，而且这两个文件夹的结构大同小异，两边都有一些相同的文件，而它们只是命名空间不一样。这是因为我们用到 ILRuntime，而 ILRuntime 最好不要跨域继承。

`Model/Init.cs`

文件中

1 | private async ETVoid StartAsync() |

通过组件设计，可以轻易地加载组件和卸载组件，例如我可以写一个心跳包组件来每隔30秒发送一个心跳包到服务器，当我需要这个组件的时候，可以直接 `AddComponent`

，不需要的时候可以 `RemoveComponent`

移除组件。

## 登陆界面的热更新启动过程

接下来看到 `Hotfix/Init.cs`

文件中

1 | public static void Start() |

来看看发送的事件，代码在

`Hotfix\Module\Demo\UI\UILogin\System\InitSceneStart_CreateLoginUI.cs`


1 | namespace ETHotfix |

再来看看一个界面是怎么生成的，代码在 `Hotfix\Module\Demo\UI\UILogin\System\UILoginFactory.cs`


1 | public static UI Create() |

来看看登陆界面组件，代码在 `Hotfix\Module\Demo\UI\UILogin\Component\UILoginComponent.cs`


1 | public class UILoginComponent: Component |

服务器地址存在了 Tools 菜单中的全局配置，上面的资源路径则是热更新服务器的地址。

![](../../assets/b4f0413a22186d42.png)


游戏运行后，在 Hierarchy 界面中也可以看到组件的结构，其中 `uilogin.unity3d`

就是登陆界面的 AB 包引用：

![](../../assets/eb97d92de68417b0.png)


这就是通过热更新逻辑生成的界面，也就是说，上面的代码让我们可以通过热更新来给应用加载各种界面和改写页面跳转逻辑，当然还可以通过热更来增加修改游戏逻辑和功能。

如果不喜欢这种页面加载方式，可以考虑不使用 `Hotfix/Init.cs`

中的 `Game.Scene.AddComponent<UIComponent>();`

这个 UIComponent，而使用其他 UI 组件，例如主仓库中的 FairyGUI 分支，让 FairyGUI 来单独负责 UI 界面。这里也可以看出基于组件的框架的灵活性，我以后也会出文章单独介绍 FairyGUI。

## 热更新切换

首先看看作者的介绍：

7.客户端热更新一键切换


因为ios的限制，之前unity热更新一般使用lua，导致unity3d开发人员要写两种代码，麻烦的要死。之后幸好出了ILRuntime库，利用ILRuntime库，unity3d可以利用C#语言加载热更新dll进行热更新。ILRuntime一个缺陷就是开发时候不支持VS debug，这有点不爽。ET框架使用了一个预编译指令ILRuntime，可以无缝切换。平常开发的时候不使用ILRuntime，而是使用Assembly.Load加载热更新动态库，这样可以方便用VS单步调试。在发布的时候，定义预编译指令ILRuntime就可以无缝切换成使用ILRuntime加载热更新动态库。这样开发起来及其方便，再也不用使用狗屎lua了

8.客户端全热更新

客户端可以实现所有逻辑热更新，包括协议，config，ui等等

![](../../assets/ace1135835e701c5.png)


预编译指令指的就是在 Player Setting 中，上图右下角箭头指着的地方。当前有两个预编译指令，通常在开发中，可以只填写 `NET452`

，这样可以得到完整的堆栈信息来调试程序。还有一个预编译指令 `ASYNC`

，加上后，应用就会从前面填写的热更新服务器下载热更包，该指令在后文会提到。

在国内环境下，手机游戏热更新的需求较强烈。市场上手机系统普遍分成 Android 和 iOS 阵营，其中 iOS 不支持 JIT 热更，因此 ET 框架给了两种选择：ILRuntime 热更新和 Mono 热更新。

两者概念可以参考文末的参考链接，在这里不多说。

## 体验热更新

体验热更新之前，先把项目切到 Android 平台。

按照下图配置 Mono 热更新：

![](../../assets/d6b9f542c2809f26.png)


确保 Scripting Backend 为 Mono，下面预编译宏去掉 ILRuntime，加上 ASYNC，按下**回车键**执行变更。ASYNC 说明我们现在的热更新资源从资源服务器中获取，这里的热更新资源包括 Res 文件夹、Bundles 文件夹、Hotfix 文件夹中的代码等。在这个例子中，登陆界面的代码就已经写在热更新文件夹中了，我们将尝试通过热更新来展示登陆界面。

点击 Play 按钮，会有两个报错：

![](../../assets/3900812638b2e839.png)


第二个 Log 信息展示了应用想要获取资源的热更资源服务器地址，这个地址可以在 Tools 菜单的全局配置中找到。报错信息提示找不到终端主机。报错是理所当然的，因为我们还没有启动本地服务器。

首先要生成热更新文件，在 Tools 菜单中点击打包工具，如下图所示：

![](../../assets/3041c32e3442454e.png)


平台选择当前的 Android 平台，目前不需要打包应用，所以无视第一个单选按钮。

前面的思维导图提到了 ET 根目录的 Release 文件夹存的就是热更新资源文件。打包工具也会把打包后的资源放在 Release 文件夹下。而第二个按钮指的是是否把打包的热更新资源也放在应用中，目前也不需要选择。开启热更新后，应用会比较服务器和本地应用的 Version 文件，计算文件差异后才会下载相关的热更新资源文件。

如果勾选了第二个按钮，打包工具将会把资源也复制到 Assets/StreamingAssets 文件夹下，同时更新 Version 文件，这样我们将不能测试下载热更包的过程。

![](../../assets/a962d47e01919987.png)


点击开始打包后，热更文件就生成了：

![](../../assets/cb43793d0ce48e1b.png)


再点击 Tools 菜单中的 web 资源服务器开启映射了 Release 文件夹的本地文件服务器。

点击 Play 按钮，应用通过下载热更新资源，生成了登陆界面，也把热更资源下载到了应用中，也就是 Assets/StreamingAssets 文件夹。

![](../../assets/0baa4c2567b89719.png)


重新启动 web 资源服务器清除 log 信息，再次运行应用，会发现没有再次下载热更新资源。因为对比了 Version 文件后，应用本地的文件已经不需要更新了。

![](../../assets/984ab0923c595c52.png)


至此，我们完成了一次完整的热更新。

## 总结

ET 框架给了我们一种统一的开发体验，提供了方便的热更新切换和调试方案，这足以支撑起一些小游戏的开发需求，有需要的同学可以了解下 [ET 框架](https://github.com/egametang/ET)~

2019 年立了个 Flag：周更技术博客，欢迎督促和交流，也欢迎常来我博客 [萤火之森](http://frankorz.com) 逛！