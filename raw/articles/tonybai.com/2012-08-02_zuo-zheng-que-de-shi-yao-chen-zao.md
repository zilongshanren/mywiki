---
title: 做正确的事要趁早
url: https://tonybai.com/2012/08/02/do-right-things-early/
published: '2012-08-02'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 做正确的事要趁早

最近闲暇时间在策划实施两件事儿：一是产品的[自动化回归测试](http://en.wikipedia.org/wiki/Regression_testing)；二是尝试在项目中使用一些静态代码语义分析工具。我觉得这两件事是应该做的正确的事，对提升产品质量，提前发现产品中潜在的缺陷都大有裨益。但在做的过程中才感觉到：现在做有些晚，正确的事要趁早做。

去年自动化测试组发布了自动化测试框架的第一个版本，我们的产品参加了试点。但经过自动化测试组大半年的投入，效果十分有限，根本没有达到我的预期。最主 要的问题是使用他们提供的框架编写和维护test case都十分困难，工作量投入很大，这很打击大家的积极性。今年大家决定将自动化测试框架换成nokia开源的[robotframework](http://code.google.com/p/robotframework)。经过预 研，robotframework完全可以满足我们的测试需求，并且robotframework的用例编写和维护效率太高了，编写门槛却很低。

虽然换成了robotframework，但我们应用的时机还是有些晚了。试点项目已经接近开发尾声，这时候如果要加上自动化测试，势必就要在短时间进行 大量测试用例开发。如果在项目初期，增量的用例添加相信会达到更好的效果。但即便是“亡羊补牢”，我们也还是要做的，还好这个产品版本的生命周期才刚刚开 始，后续可能还会持续很多年，加上自动化回归测试还是有重大意义的。

不过鉴于之前的教训，我们调整了自动化测试的切入点。之前自动化测试组只是闷头写用例，并未太多考虑自动化测试框架与被测目标如何配合的问题：比如没有考 虑自动化测试在哪个环节应用、谁来驱动、谁来执行以及测试环境如何生成等。这次我们先绕过用例编写，先从“基础设施”搭建开始。我们的目标是将自动化测试 与我们的[持续集成](http://tonybai.com/2012/02/15/intergating-on-multiple-platforms-simultaneously-using-jenkins/)流程集成在一起，也就是说我们将通过[jenkins](http://tonybai.com/2012/02/14/install-and-configure-jenkins/)这样的ci平台来作为自动化回归测试的驱动。我们首先就是要将这个驱动流程run起 来，即便测试用例库中一条用例也没有。一旦run起来后，我们再将关注点集中在用例的编写和调试上，我想这才是正确的思路。

第二件感觉做得有些晚的正确的事儿就是为项目增加静态代码检查环节。之前项目静态代码检查仅停留在打开[GCC编译器](http://tonybai.com/2006/03/14/explain-gcc-warning-options-by-examples/)的-Wall选项这个层次。就是否有必 要引入第三方静态代码分析工具对代码进行缺陷检查，大家一直没有统一意见。质量部门希望我们引入，但关键问题是我们没有找到一款适合的开源工具(for C)，在维基提供的[C语言静态分析工具列表](http://en.wikipedia.org/wiki/List_of_tools_for_static_code_analysis#C.2FC.2B.2B)中，我感觉似乎只有[splint](http://www.splint.org)符合我们的要求 – 开源、功能强大且支持linux/unix。不过splint似乎已经停止开发了，最新版本停留在3.1.2。

使用类似splint这样的工具对代码进行检查时总是能给出大量的warning，如果不加以控制，那么屏幕就会被warning淹没。因此正式使用之 前，需要一个“磨合期”。先确定打开或关闭哪些检查规则开关，原则只有一个，即尽量避免误警告，又不能漏掉真实的隐患。splint对[C99](http://tonybai.com/2011/08/31/simplify-coding-in-c99/)新增语法的支 持不是很好。splint碰到下面这种语法时会提示parse error，并且无法recover：

struct foo {

int a;

int b;

};

int main() {

struct foo f = {.a = 1, .b = 2}; /* Parse Error */

printf("%d %d\n", f.a, f.b);

return 0;

}

这类静态代码检查的基础设施在项目初期搭建起来是最佳的，开发人员可以增量的对代码进行语义检查，并修正缺陷。但如果在代码开发即将结束的阶段加入，即使 是设置了一套合理的检查规则组合，你也可能困惑于工具产生的大量Warning。不过“有胜于无”，在没有找到更好的工具前，我将splint加入到工程 中，建议组员适当时机使用，并随时对check rules组合开关进行调整和优化。也许经过一段时间的磨合后，可以实现在ci job中加入自动代码静态检查这个环节，当然目前肯定不是适宜时间。

正确的事，你会发现早做和晚做效果是截然不同的。但“亡羊补牢“的工作也不能不做。既然是你认为正确的事，从长远来看，还是能带来很大价值的。

© 2012, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

我有点没看明白。1) robotframework和jenkins有什么区别？我只用过jenkins。2) 看到robotframework的介绍是一个ATDD的framework。也就是说为了要做TDD，引入了一个framework？

1、jenkins是持续集成工具，robotframework是自动化测试框架。两者没有必然联系。这里所说的是用jenkins作为执行自动化测试的驱动平台。

2、用robotframework当然不是为了TDD。robotframework上跑的测试用例多为验收测试用例，非单元测试用例。

听说华为公司软件编码要求是：首先必须使用静态代码检测工具pc-lint对提交的代码进行检查，要求无任何告警信息…，对于合入代码库中的程序，编译程序运行之前又会自动进行pc-lint检查，发现产生告警的代码时会给项目组带来严重的影响。