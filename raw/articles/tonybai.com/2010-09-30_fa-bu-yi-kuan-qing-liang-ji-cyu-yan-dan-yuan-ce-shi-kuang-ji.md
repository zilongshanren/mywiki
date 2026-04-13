---
title: 发布一款轻量级C语言单元测试框架
url: https://tonybai.com/2010/09/30/opensource-a-lightweight-c-unit-test-framework/
published: '2010-09-30'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 发布一款轻量级C语言单元测试框架

基于各种[xUnit](http://en.wikipedia.org/wiki/XUnit)框架的单元测试早已不是什么新鲜玩意儿，不过在"古老"的C语言领域，还尚未有哪种框架可以成为“寡头”。

记得2005年末的时候，初出茅庐的我吸取xUnit的设计思想在业余时间编写了一个轻量级的C单元测试框架[lcut](http://code.google.com/p/lcut/)(Lightweight C Unit Test framework)，当时还写了一篇文章《[C单元测试包设计与实现](http://tonybai.com/2005/11/08/the-design-and-implementation-of-c-unittest-framework/)》记录了最初的设计和实现思路。本打算将这个小工具在部门内至少是项目内推广，可无奈当时部门内部尚未认识到使用框架工具进行单元测试的好处，或者尚未形成此种技术风气，当时的我也是“人轻言微”，因此这个小工具也没能吸引足够的眼球。这么长时间以来，都是我自己一直在使用，

其间，lcut做了两次小规模修改。特别是最后一次修改，通过增加测试用例执行的返回状态(增加LCUT_TEST_RESULT()宏)，让lcut可以与一些持续集成工具（如[cruisecontrol.rb](http://tonybai.com/2008/08/20/the-experience-of-cruisecontrol-rb/))结合在一起使用。

随着部门同事对单元测试认识度的提升，基于框架的单元测试也逐渐在组内执行开来，有人使用[cmockery](http://tonybai.com/2009/08/22/introduce-cmockery-for-c-unit-test/)，有人使用[CuTest](http://cutest.sourceforge.net/)，也有一些新同事参考以前我编写的代码开始使用lcut。中秋假期在家读完《[The Passionate Programmer](http://book.douban.com/subject/4923179/)》(中文版名为:《我编程，我快乐-程序员职业规划之道》)后，颇有感触。这几天突然就有了把lcut发布出去的想法(咱不能总享用，不付出吧^_^)。

发布出去前的准备工作还是蛮多的:

* 挑选一个合适的开源项目托管平台

以前是[sourceforge](http://sourceforge.net/)一家独大，现在则有许多选择，主流的平台包括Google code、[github](http://github.com)、[launchpad](http://launchpad.net)等，最终我选择了Google Code，其实也没有什么具体理由，只是因为一直都使用Google的产品，惯性使然。如果你之前已经拥有了Google的account，那么使用Google code就更加方便了。具体如何操作，Google Code有详细的官方manual供你查阅。

* "美化"和包装代码

发布出去之前，需要先对lcut代码进行一下"美化"，毕竟在家里显摆和在大庭广众下展示是有不同的。代码的格式最好能适应大多数人(或者是编辑器）的口味(比如[将TAB换成空格](http://tonybai.com/2010/09/07/a-problem-about-vim-expand-tab/))，可利用类似[astyle](http://tonybai.com/2010/07/29/use-astyle-to-beautify-your-code/)这样的代码格式化工具按照配置号的规则对代码做一次全量格式化。另外由于要应对不同平台、不同OS，我们还要考虑代码的可移植问题，这方面我采用[autoconf和automake](http://tonybai.com/2010/09/26/hello-autoconf-and-automake/)重新编写了lcut的构建脚本。

* 测试

为了保证发布出去的包可用且是正确的，当然需要做测试了。构建测试、安装测试以及包本身的功能测试，这个还是很耗费精力的。lcut在[Ubuntu 10.04](http://tonybai.com/2010/08/25/move-to-ubuntu-thoroughly/)(x86 32bit)和Solaris 10(x86 and Sparc)平台下都测试通过。

* 文档

头疼！lcut本身就没什么文档，另外考虑到一般对外发布都使用English编写文档，我就更纠结了。在目前发布的lcut-0.1.0版本中，文档确是欠缺的。要知lcut是如何使用的，可参考我上面提到的《[C单元测试包设计与实现](http://tonybai.com/2005/11/08/the-design-and-implementation-of-c-unittest-framework/)》或看src/example下的例子。

* Roadmap

lcut尽可能做到不是“发布后不管”，所以还要有Roadmap或是TODO计划。这里想到两点：一是补文档; 二是打算为lcut增加[mock](http://tonybai.com/2008/04/12/mock-test-in-c-unit-test/)功能。

明天就是国庆了，这里将lcut(http://code.google.com/p/lcut/)发布出来权当国庆献礼了，欢迎大家试用并提出宝贵意见和建议。

© 2010, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 仅有 1 条评论