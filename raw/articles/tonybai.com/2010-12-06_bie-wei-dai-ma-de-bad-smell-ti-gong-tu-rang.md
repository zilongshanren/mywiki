---
title: 别为代码的"Bad Smell"提供土壤
url: https://tonybai.com/2010/12/06/do-not-provide-soil-for-bad-smell-code/
published: '2010-12-06'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 别为代码的"Bad Smell"提供土壤

上周初参加了一次[代码评审](http://tonybai.com/2006/05/31/code-review-is-necessary/)，评审时发现一位同事在自己负责的子模块代码里定义了一个私用宏，"重复"这个[Bad Smell](http://en.wikipedia.org/wiki/Code_smell)立马在我头脑中闪现。当时我给出了一个建议：检查一下这个宏定义的必要性，依次检查一下C运行库头文件中是否已经有了同功用宏定义，基础库头文件中是否已经有了同功用宏定义，业务层代码的共用头文件中是否已经有了同功用宏定义。

周末这位同事给出了答复：C运行库、基础库和业务层代码中都没有定义此功用的宏。考虑一下这位同事如此编码的动机：显然一方面他为了避免magic number才去定义一些宏，提高可读性。另一方面确实无此功用的宏可用才考虑定义在自己的子模块中。但是这个宏的定义到底该放在哪里才是正确的呢？

这个宏是作为一个buffer的size而定义的，这个buffer会作为基础库中某个函数的输出参数，而这个函数原型声明所在的头文件中却没有提供相关宏为上层开发者所使用，这才导致了调用者自己猜测并设置buffer size。不讲究的开发者很可能就直接使用一个magic number，而像我这位同事采用的这种方法又会导致一些"重复"的Bad Smell的出现。这样来看，也许正是这个库函数的设计者为Bad Smell提供了滋生的土壤。

库设计者应该多为上层调用者考虑，这方面可参考一些优秀库的设计，如C标准库等。因为你的接口设计而给调用者带去Bad Smell，这是我们不希望看到的。

© 2010, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

我倒是挺感兴趣是哪个接口呢？ 学习一下。：）