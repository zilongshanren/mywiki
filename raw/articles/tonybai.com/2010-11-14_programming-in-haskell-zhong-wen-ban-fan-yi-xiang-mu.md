---
title: 《Programming in Haskell》中文版翻译项目
url: https://tonybai.com/2010/11/14/the-chinese-translation-project-for-programming-in-haskell/
published: '2010-11-14'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 《Programming in Haskell》中文版翻译项目

*"A language that doesn't affect the way you think about programming， is not worth knowing".*

— [Alan Perlis](http://en.wikipedia.org/wiki/Alan_Perlis)(ACM 第一任主席，图灵奖得主，1922-1990)

《[程序员修炼之道](http://book.douban.com/subject/1152111/)》这本书建议程序员每年应至少学习一门新的语言，以拓宽思维，避免墨守成规。今年我选择了函数式编程语言[Haskell](http://www.haskell.org)。选择Haskell的理由正如Alan Perlis所说的那样，Haskell是一门可以影响程序员编程思维的语言，我也期望通过学习Haskell来拓宽我的思维。

开始接触Haskell后，我才发现它在国内是如此的小众(其实在国际上也很小众)，国内居然没有正式出版过Haskell相关的中文书籍，唯一可参考的像样的中文资料就是网上流传的一本免费的由乔海燕翻译的《[Yet Another Haskell Tutorial](http://www.cs.utah.edu/~hal/htut/)》，国内出版的影印版书籍似乎也只有《[真实世界的Haskell](http://book.douban.com/subject/4214143/)》(英文名：Real World Haskell)这一本。

我开始学习Haskell时用的就是那本曾获得过[Jolt Award](http://www.realworldhaskell.org/blog/2009/03/12/we-won-a-jolt-award/)大奖的《[Real World Haskell](http://www.realworldhaskell.org/)

》影印版，书很厚，是本Haskell大全。但后来发现似乎不太适合初学者。随后又在网上搜索资料，找到了[Graham Hutton](http://www.cs.nott.ac.uk/~gmh)编写的《[Programming in Haskell](http://www.cs.nott.ac.uk/~gmh/book.html)》这本教程。与《Real World Haskell》比起来，《Programming in Haskell》这本书就显得“单薄”了许多，加起来总共不到200页。不过这本书却非常适合函数式编程和Haskell的初学者，因为这本书是基于英国诺丁汉大学课程讲义编制而成，经过了多年实际教学检验，并且在这本书的官方主页上还可以下载到与书配套的讲义幻灯片和习题答案。

同样是也是在这本书的[主页](http://www.cs.nott.ac.uk/~gmh/book.html)上，我发现了这本书在2009年就已经出版了日文版和韩文版，这个让我很是受触动，为什么在好书引进方面我们也落后于日韩呢！突然脑中迸发出一个念头：要不我来试试翻译一下这本书，也算是为Haskell在中国的发展做出一些自己的贡献。

于是在Google Code上建立了这个[《Programming in Haskell》中文版翻译项目](http://code.google.com/p/programming-in-haskell-cn/)。

最初尝试使用[tiddlywiki](http://tonybai.com/2010/08/30/learn-tiddlywiki/)来做中文内容的载体，后来发现使用tiddlywiki非译书之正道。为此，我还特意花了一些时间学习了一下[TeX](http://tonybai.com/2010/10/18/hello-tex/)，并做了一个非专业的[中文TeX模板](http://tonybai.com/2010/11/02/a-tex-template-based-on-xetex-and-xecjk/)，用于自己翻译之用。

到目前为止，自己边学Haskell，边尝试翻译《Programming in Haskell》，并已经完成了序言以及前三章的初译。由于自己之前没有任何函数式编程语言的知识和英文翻译的经验，所以翻译起来甚感吃力。另外Graham Hutton的偏学术派的写作风格也让翻译的难度陡增不少。对于已经翻译的三个章节，自己并不甚是满意，总觉得在术语翻译，原意把握以及行文方面欠缺较多。不过经过这段时间的翻译，对Haskell以及函数式编程的理解却加深了不少，所以后续计划对已翻译的三个章节进行回顾，形成中英文对照表，纠正术语翻译错误、作者原意把握不准确的地方以及行文不通顺的地方。

真诚的欢迎大家提出建议和意见，帮助我来审校翻译中存在的问题，共同完成这个项目。

另外这里需声明一点：自己仅是一个Haskell爱好者和初学者，非Haskell牛人。请大家读译稿后谨慎拍砖！

附：《Programming in Haskell》中文版翻译项目地址：http://code.google.com/p/programming-in-haskell-cn

微软C9 函数式编程基础(使用《Programming in Haskell》这本教程)视频地址：在[这里](http://channel9.msdn.com/Shows/Going+Deep/Lecture-Series-Erik-Meijer-Functional-Programming-Fundamentals-Chapter-1)。

© 2010, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

人人都说haskell需要大量时间精力 我觉得您出于每年1新语言的目的 翻译也许不是好的方式 而且敢玩haskell 英文读的能力应该也过关了吧

翻译总是个吃力不讨好的活 您也知道 不同语言本就不是完全一一对应的 有些地方/词语用某语言表达很给力用另种就很乏力 所以常出现直接读原版挺顺翻译反倒拗口

albert_lee先生今年4月已完成RWH的翻译只是不知为何一直未出版：

http://blog.csdn.net/albert_lee/archive/2010/04/12/5475306.aspx

CU的FP版有人曾联系好了出版社然后组织版友自己写中文版的教程 不过好像响应的不多 最后貌似也搁浅了

那天猛然发现manatee（haskell+Gtk2hs，功能是"伪操作系统“，像emacs那样）

http://www.flickr.com/photos/48809572@N02/5154125200/in/photostream/ 的作者是国人 而他说自己现在完全haskell 并相信haskell可以做更好 如同RWH中的那句话

Code you can believe

现在是七年后，我怎么都搜不到原作者自己搞的中文版。虽然现在haskell中文教材也有一些了，但是看了介绍。还是想把这个作为入门的……

可惜当年原书作者不给授权，否则当年就翻译完毕了，还有很多志愿者想一同翻译。不过那个事情最终还是促成了我参与了《七周七语言》的翻译。现在转移到Go了。Haskell基本不碰了。