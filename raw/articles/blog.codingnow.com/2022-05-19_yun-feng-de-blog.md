---
title: 云风的 BLOG
url: https://blog.codingnow.com/2022/05/
published: '2022-05-19'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

### RogueLike 原型开发工具

我很喜欢 RogueLike 游戏，我是说字面意义上的像 [Rogue](https://store.steampowered.com/app/1443430/Rogue/) 那样的游戏 。在这种游戏中，画面是最不重要的部分，只要能清晰表达出游戏需要的交互意义就够了。

我对用字符拼凑出来的游戏界面有种特别的爱好，小时候自制游戏就是从 text mode 开始的。 在今天，如果只是想验证一下某个游戏的原型，一个 Rogue 风，text mode 的交互界面，可能还是最省事的。因为你不必刻意的去准备美术素材，考虑这些素材如何和代码协同工作，制定繁杂的工作流。为游戏创作一点有趣的 ascii art 不仅不用太长的时间，可能还是写代码过程中的一点有趣的调剂。

前段时间在做项目中一个试验性模块时，[我尝试做了一个简单的 Lua 库](https://blog.codingnow.com/2021/05/ansi_escape_code_in_lua.html) 帮助我用 text mode 搭建交互。最近又碰到一个更复杂的需求，评估了一下，基于 SDL2 做一个更完善一点的 RogueLike 库或许更一劳永逸。

于是上周我花了两天时间做了这么一个东西：[https://github.com/cloudwu/rogue](https://github.com/cloudwu/rogue) 。

它的核心是一个 text mode 的 sprite 。支持用 IBM Dos 下的 CP437 字符集以及 Unicode 中简体中文的子集拼凑 Sprite ，当然接口采用现代 UTF-8 标准。可以支持 256 个图层，以及 RGB 描述的色彩（而不是传统意义的 text mode 下16 色调色盘）。

汉字的支持用了一点小技巧，在内部的虚拟 text frame buffer 中的每个 slot ，都保存了完整的 Unicode 码点，以及它可能属于汉字的左半边还是右半边。这样彻底不会有过去 text mode 下半个汉字乱码的问题。

sprite 采用的是 retained mode ，即，只要创建出 sprite ，就一直在内部的链表上，每帧都会画出来。这点和很多传统的类似库不同，传统做法一般是 immediately mode ，也就是每帧你都需要 draw 特定的 sprite ，如果不调用 draw 就不会显示。

我曾考虑过某种混合模式，就是区分 map 和 sprite 。地图用 retained mode ，角色用 immediately mode 。但我觉得会增加接口复杂性。目前这样也暂时够用了。

在写这个玩具时，不时让人回忆起中学时在 Apple ][ 上做那些小游戏的时光。就是从那个时候起，我逐步悟到需要把程序里通用的需求提取出来做成共用的模块；游戏程序就是一个被设计出来的状态机；数据应该和程序分离；设计数据结构是程序设计中最重要的环节；应该为组织数据编写相应的工具……

真是一小段美好的开发经历。