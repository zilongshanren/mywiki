---
title: C语言编码风格和标准
url: https://tonybai.com/2012/03/07/the-chinese-translation-of-recommended-c-style-and-coding-standards/
published: '2012-03-07'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# C语言编码风格和标准

近期在为产品线的[知识库](http://tonybai.com/2011/11/23/those-things-about-knowledge-management/)编写一些指南类的文档，其中有一项就是对现有的C语言编码规范进行一些修订。为了"有米下锅"，我还特意在网上找了一些相关资料。关于C语言编码风格和标准的资料大多都成稿于上个世纪90年代，也就是在C90发布之后的若干年里；在[C99](http://en.wikipedia.org/wiki/C99)发布后，部分资料根据最新的规范做了修订，但也有些资料认为[C99](http://tonybai.com/2011/08/31/simplify-coding-in-c99/)对整体风格影响不大，也就保持了原样。

在这些资料中，我重点关注了一下这份文档《

[Recommended C Style and Coding Standards](http://www.psgd.org/paul/docs/cstyle/cstyle.htm)》，它是著名的"Indian Hill C Style and Coding Standards"的更新版，从Google的搜索结果来看，似乎影响很广。这份文档内容不多，言简意赅，特别是后面的几个小节，例如宏、条件编译、可移植性以及ANSI C等章节很值得细致阅读和理解。我试图google该文档的中文版，居然没有找到。也许是这个文档比较老了，或者是其中有些注意事项在当今C编程领域较少能遇到了，再或许就是C语言老了，关注的人少了，总而言之，网上没有该文档的中文版。于是乎我就花了一些时间翻译了一个粗糙的中文版，供那些看E文和我一样吃力的朋友们参考。中文版以Wiki的形式放在了Google code(http://code.google.com/p/recommended-c-style-and-coding-standards-cn/)上了。这里需要先说明的是：翻译过程不是很细致，较随意，有些地方我理解得也不慎透彻，欢迎大家提出自己的见解，后续有时间还会持续地修订。

这里提供一个快捷入口^_^：

© 2012, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

Google 上 “


4. 声明” 与正文内的标题“2.3 声明”不一致"

16. 可移植性" 的正文无标题十分感谢你发现的问题，已经修改完毕。