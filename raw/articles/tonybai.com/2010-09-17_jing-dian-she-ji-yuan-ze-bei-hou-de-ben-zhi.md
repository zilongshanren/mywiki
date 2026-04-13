---
title: 经典设计原则背后的本质
url: https://tonybai.com/2010/09/17/the-nature-of-some-classical-design-rules/
published: '2010-09-17'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 经典设计原则背后的本质

近一段时间重读了一些经典书籍，诸如《[敏捷软件开发：原则、模式与实践](http://book.douban.com/subject/1140457/)》、 《[程序员修炼之道](http://book.douban.com/subject/1152111/)》、《[Unix编程艺术](http://book.douban.com/subject/1467587/)》等。这些书中关于如何衡量或评价一个类或函数设计好坏的几个原则(Principle)让人印象深刻。《敏捷软件开发》中谈到了[SRP](http://en.wikipedia.org/wiki/Single_responsibility_principle)、[OCP](http://en.wikipedia.org/wiki/Open/closed_principle)、[DIP](http://en.wikipedia.org/wiki/Dependency_inversion_principle); 程序员修炼之道则以[DRY](http://en.wikipedia.org/wiki/DRY)、“正交性”为话题展开;《Unix编程艺术》围绕紧凑性、SPOT、分离等阐述作者立场。这么多经典原则，如何学习把握？我们不妨来挖掘一下这些新设计原则背后的本质。

追本溯源，从计算机编程语言的发展历史来看，成熟的结构化程序设计语言(如[C语言](http://tonybai.com/2006/03/28/c-refactoring/)、Pascal等)要先于成熟的OO设计语言(C++、Java等)出现，那么其成熟的设计理论显然也是要早于后者的。这里就不能不提到经典结构化设计的代表作：《[Structured Design: Fundamentals of a Discipline of Computer Program and System
Design](http://book.douban.com/subject/2357689/)》，这本书出于1975年(年份来自

[维基百科](http://en.wikipedia.org)，Amazon上卖的是1979年版)。说实话我也没有看过此书原版，不过书中的内容和思想早已被其他后继书籍引用和借鉴，我们在市面上能看到的关于结构化设计方面的书籍，尤其是中文书籍，多照搬了此书内容和思想，所以也算是间接学习到了。

书中对抽象、模块化、信息隐藏(黑盒)作了阐述，并介绍了数据流/控制流图、结构图等设计方法。特别是书中关于内聚(Cohesion)与耦合( Coupling)的讲解对之后的程序设计评价方法影响至深。我们一直常说高内聚低耦合的模块是良好的设计，这里的内聚和耦合概念的提出者恰是这本书的作者[Larry L.Constantine](http://en.wikipedia.org/wiki/Larry_Constantine)。内聚和耦合这两个概念是用来评价一个module设计好坏的。module一词中文意为“模块”，模块一词的范围让人很难界定，关于module这个概念，书中给出了这样的解释："A module is a lexically contiguous sequence of program statements, bounded by boundary elements, having an aggregate identifier. Another way of saying this is that a module is a bounded, contiguous group of statements having a single name by which it can be referred to as a unit." 显然类或子程序（函数）是符合module的定义的。用内聚和耦合来评价类或子程序（函数）的设计是适合的。

关于[Cohesion](http://en.wikipedia.org/wiki/Cohesion_(computer_science))(CC2e 7.2小节)和[Coupling](http://en.wikipedia.org/wiki/Coupling_(computer_science))(CC2e 5.3小节)的具体内容，这里就不细说了，《代码大全2》作者说的肯定比我好多了，另外维基百科中对coupling和cohesion的描述也很详尽。

以上所说的内聚和耦合其实就是我认为的以上诸多经典设计原则背后本质的东西。诸多设计原则应该可以看作是耦合和内聚概念在不同语言范式上下文情境下的延伸、再包装或升华。虽然有些原则说法发生变化了，但是本质却是一样的。比如: 单一职责原则(Single Responsibilty Principle, SRP) 显然是"功能内聚(Functional cohesion)"的另一种表述; 有些原则虽然无法直接与内聚耦合概念进行直接对号，比如依赖倒置原则(Dependency Inversion Principle，DIP)，但是可以理解成追求低耦合的一种设计技法！

把握好内聚和耦合的核心理念，你将以不变应万变，你也会更深刻理解诸如OCP、DIP等新原则了。

俗话说“物以类聚”，这句同样适用于程序设计！一个module的设计如果有一处优点，那常常这个module也具备其他优点; 反之，如果发现这个module设计的一个缺点，那么离发现其他缺点也就不远了。

内聚与耦合的概念不仅仅适用于程序设计领域，在所有其他设计领域似乎同样普适！考虑对比一下一个具备电加热除霜功能的后视镜与一个普通后视镜在设计层面上的优点与不足吧！

发觉题目似乎有些夸张^_^。

© 2010, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论