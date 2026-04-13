---
title: '"%05s"行为未定义'
url: https://tonybai.com/2010/12/17/undefined-behavior-of-%05s/
published: '2010-12-17'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# "%05s"行为未定义

下班前，一位同事发来的mail中提到这样一个问题：在[Solaris](http://tonybai.com/2009/09/10/something-about-installing-solaris-10/)上，新添加到Project中的一段代码编译有Warning，由于我们在Makefile的[GCC](http://tonybai.com/2006/03/14/explain-gcc-warning-options-by-examples/)命令行中设置了"[视警告如错误](http://tonybai.com/2010/09/05/view-warning-as-error/)"的-Werror编译选项，导致了项目无法成功Build。

这个Warning内容如下：

warning: `0' flag used with `%s' printf format

产生这个Warning的那行代码大致是类似这样的：printf("%05s%06s\n", "11", "222"); 其实这段代码是从老项目中Copy出来的，在老项目中，这段代码运行的很是正常，也许它在老项目Build时也会产生Warning，不过之前大家也都没有关注。

这个Warning我以前还真未遇到过，代码看起来写的也没有问题，我在[Ubuntu](http://tonybai.com/2010/08/25/move-to-ubuntu-thoroughly/) 10.04(GCC 4.4.3)上测试了一下这段代码，同样产生了Warning。不过执行一下编译后的程序，我发现了问题。显然这段代码的意图是想通过"%05s"这样的格式控制串来达到自动补0的目的，但是Ubuntu下输出的结果却与此预期相悖–没有补0，补的是空格。我又拿同样的代码在Solaris(Solaris 10 for x86, gcc 3.4.6)上试了一下，虽然也有Warning，但结果和预期是相符的。

这个问题显然比我预期的严重：一段代码在两个平台上产生了不同的行为，问题显然出在"%05s"的使用上。翻开《[C语言参考手册](http://book.douban.com/subject/1134988/)》找到输入/输出函数一章，在"输出转换说明"一表中可与s转换搭配的只有'-标志'，没有'0标志'，但手册里并未明确说明如果将0标志与s转换结合会有什么后果。又Google了一下，发现一些资料里提到在printf系列接口中使用类似"%5s"这样的格式控制串的行为是未定义的，和我试验的结果一致。

考虑到可移植性，"%05s"这样的格式控制串不能再继续使用了，替代方法有多种，这里就不赘述了。如果你的代码里也有使用类似"%05s"这种格式控制串，那赶紧想办法替换掉吧，除非你的代码一直跑在Solaris上。

© 2010, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

看到这篇博客, 我才突然察觉, 我居然貌似仿佛好像一直没用过 0 前缀的格式化字符串.. =_=