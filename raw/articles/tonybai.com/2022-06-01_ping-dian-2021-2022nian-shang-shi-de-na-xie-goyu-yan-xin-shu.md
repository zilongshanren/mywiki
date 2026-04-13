---
title: 评点2021-2022年上市的那些Go语言新书
url: https://tonybai.com/2022/06/01/reviewing-those-new-go-language-books-coming-out-in-2021-2022/
published: '2022-06-01'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 评点2021-2022年上市的那些Go语言新书

![](../../assets/81138aec753343ee.png)


[本文永久链接](https://tonybai.com/2022/06/01/reviewing-those-new-go-language-books-coming-out-in-2021-2022) – https://tonybai.com/2022/06/01/reviewing-those-new-go-language-books-coming-out-in-2021-2022

计算机科学与技术这个工业大类与传统工业类别相比还很“年轻”，并且由于历史原因，整个计算机科学与技术学科的奠基都是由欧美人完成的，因此但凡诞生一门新IT技术或新编程语言，我们首先参考的都是来自欧美的外文技术书籍(影印或翻译)。

以Go为例，笔者最先接触的Go技术书籍资料是[《The Way To Go》](https://book.douban.com/subject/10558892/)：

![](https://tonybai.com/wp-content/uploads/reviewing-those-new-go-language-books-coming-out-in-2021-2022-5.png)


这也是笔者早期学习Go语言时最喜欢翻看的一本书，也是我目前见到的、最全面详实的讲解Go语言的书籍了，可以说是Gopher们的第一本“Go语言百科全书”。可能是由于这本书出版太早了，等国内出版社意识到要引进Go语言方面的书籍的时候，这本书使用的Go版本已经太老了。不过，这本书中绝大部分例子依然可以在今天最新的Go编译器下通过编译并运行起来。

另外一本不得不提的就是由K&R C中的K：[Brian W. Kernighan老爷子](https://www.cs.princeton.edu/~bwk/)参与编写的[《The Go Programming Language》](http://www.gopl.io)：

![](../../assets/7a6f077cc933f81e.jpeg)


这本书模仿并致敬[《The C Programming Language》](http://en.wikipedia.org/wiki/The_C_Programming_Language)的经典结构，从一个”hello, world”示例开始带领大家开启Go语言之旅。作者行文十分精炼，字字珠玑，这与《The C Programming Language》的风格保持了高度一致。而且，书中的示例在浅显易懂的同时，又极具实用性，还突出Go语言的特点（比如并发web爬虫、并发非阻塞的缓存系统等）。读完这本书后，你会有一种爱不释手，马上还要从头再读一遍的感觉，这也许这就是“Go语言圣经”的魅力吧！

不过，随着[Go语言在国内的扎根和广泛应用](https://tonybai.com/2022/01/16/the-2021-review-of-go-programming-language)，国内接纳Go较早的一批Gopher以及国内大厂“身经百战”的Gopher开始将Go语言沉淀下来，并陆续上线了自己的作品。从2020年开始，国内作者出版的Go语言相关书籍已经逐渐多了起来，并且质量也在逐渐提升。就像我在[《Go语言第一课》](http://gk.link/a/10AVZ) 的加餐文章[《我“私藏”的那些优质且权威的Go语言学习资料》](https://time.geekbang.org/column/article/468213)中预测的那样：**将有更多Gopher加入Go技术书籍的写作行列，从2021开始的3年，国内Go语言技术书籍也会迎来一波小高峰**。

618购物节前夕，我就来简单评点一下2021年至今出版的口碑还不错的Go语言新书(按出版时间顺序)，大家可以趁打折力度较大的窗口按需从电商平台购买纸版书或电子书渠道购买电子书阅读^_^。

### 1. [《Go语言底层原理剖析》](https://book.douban.com/subject/35556889/) 2021.8

Go语言是带有GC与运行时的语言，这就意味着很多东西不是“表面”看到的那样，比如string、切片、map等类型在运行时的表示与我们在源码中看到的有很大不同。要想玩转Go语言，不下沉到“原理”这一层还真不行。

《Go语言底层原理剖析》这本书显然也是定位了那些对Go原理有述求的这部分gopher群体。书的作者郑建勋老师是滴滴的高级研发工程师。大家知道，滴滴公司内部使用Go技术栈实现的服务比例是很高的，因此这本书也是郑老师在滴滴“摸爬滚打”后的实践检验的沉淀与总结。

这本书从Go编译构建原理起步，然后过渡到Go的几种常见复合类型(数组、字符串、切片、map)的实现原理的讲解，再到对Go核心语法函数、接口、异常处理的原理说明，最后是Go的精华，也是最难啃的部分：goroutine调度、内存分配与GC。如果从覆盖的内容全面性上，应该说基本都包含到了。

笔者在微信读书上对整本书做了阅读，从阅读体验来看，郑老师的技术十分扎实，讲解也很到位。美中不足的是，有些内容刚刚引发你想继续深入的兴趣时，书籍内容却在这里戛然而止了。如果能继续展开就更好了，也许这是基于书籍篇幅上的考量。

✩豆瓣评分：8.5

✩微信读书推荐值：57.7%

本书在豆瓣口碑与微信读书推荐上存在一些分化，原因这个还不得而知。

### 2. [《Go语言设计与实现》](https://book.douban.com/subject/35635836/) 2021.11

《Go语言设计与实现》一书是作者左书祺(Draven)在其同名开源电子书[《Go语言设计与实现》](https://draveness.me/golang/)的基础上进一步系统整理和丰富而成。左老师的开源电子书在国内Gopher圈内有着相当好的口碑，他擅长以精美插图的方式对技术细节进行细致入微的讲解，作者甚至还专门出过一篇[《技术文章配图指南》](https://draveness.me/sketch-and-sketch/)来说明其文章中插图制作使用的工具以及方法。

和《Go语言底层原理剖析》一样，《Go语言设计与实现》同样聚焦在Go编译器、类型系统与运行机制的原理层面，两本书对原理的说明角度和风格各有特点，就看读者喜欢哪种。更好的方法是主题阅读，两个相互参照的看。

编写面向Go底层原理的书是有一定“风险”的，很容易随着时间的流逝而变得“outdated”，这是因为Go语言还在快速演进中，其底层实现也在不断变化，远没有Java那样成熟，所以很难像神作《深入理解java虚拟机》那般“稳定”，需要不断更新。在这一点上，纸板书反倒没有开源电子书优势明显，后者可做到以快速持续的迭代更新。

不过笔者觉得：要想对一个语言机制的底层原理理解透彻，光是掌握其当前的实现机制还不够，了解其实现机制的历史演进过程将大有裨益，而上面的两本书的价值恰恰还可以体现在这个方面，尤其是当书中的实现机制在将来过时的时候。

✩豆瓣评分：8.5

✩微信读书推荐值：未上架

### 3. [《Go语言精进之路》](https://book.douban.com/subject/35720728/) 2021.12.17

写Go语言语法方面的书风险小，Go书籍的寿命都很长，这是因为[Go1兼容性](https://go.dev/doc/go1compat)承诺的存在，这也是Go书籍作者的幸运。

[《Go语言精进之路》](https://item.jd.com/13694000.html)是[笔者的作品](https://tonybai.com/2022/01/15/go-programming-from-beginners-to-masters-is-published)，该作品主要面向一个刚刚Go入门后的Go新手，就像副标题描述的那样，聚焦于告诉一个Go入门新手如何能像Go开发团队那样写出符合Go思维和语言惯例的高质量代码。书中也有一部分底层原理的介绍，但这些介绍也都是为了配合主线的讲解。由于是偏思维、方法与技巧方面的讲解，里面的绝大部分知识点，即使是几年后，依然是有效的。这就像出版于2015年的Go语言圣经《The Go Programming language》目前看毫不过时一样。

笔者自己的书不好自作点评，下面是[近期一位读者在weibo上主动at我的评价](https://weibo.com/7541535351/LuUSQlY58)：

![](../../assets/e90d60b13a7e828c.png)


其他评价/评论大家也可以在书籍的豆瓣页面或微信读书页面上自行查看。

✩豆瓣评分：8.9

✩微信读书推荐值：84.1%

### 4. [《Go语言定制指南》](https://book.douban.com/subject/35852237/) 2022.2.1

《Go语言定制指南》是国内Go技术专家柴树衫老师既[《Go语言高级编程》](https://book.douban.com/subject/34442131/)后的又一力作，这次内容更加聚焦：围绕Go语法分析树学习Go词法分析、语法分析、语义分析以及中间代码生成的原理，并基于Go语法树对Go语言进行二次改造，基于Go语言语法裁剪出一个极小子集——凹语言，并实现其的解释执行。

更具体来说，书中主要讲解的是go/ast和go/types等Go编译器相关包的用法，比如：结合[Go语言的文法、语法](https://tonybai.com/2022/05/24/an-example-of-implement-dsl-using-antlr-and-go-part1)与go/ast包输出的语法树的对应关系；使用go/types进行语义检查的方法等。

这也是目前国内第一本以Go编译器前端为中心的Go语言技术书籍，即便放眼全世界，这也是稀有的。如果你对Go编译器的工作原理、对定制Go语言十分感兴趣，那么此书是你的不二之选。

不过编译器和语言开发是门槛较高的领域，不免会出现“曲高和寡”的境遇，这本书注定是本已是小众的Go社区中的小众群体的菜。

✩豆瓣评分：暂无

✩微信读书推荐值：暂无

### 5. 引进版新书简评

在豆瓣图书搜索Go技术书籍，看到下面几本刚刚出版不久(可能尚未上架)以及即将出版的几本引进版的新书，这里顺便说说。

[《Go语言学习指南：惯例模式与编程实践》](https://book.douban.com/subject/35902219/)2022.4.29

这是O’Reilly出版社于2021年3月出版的《Learning Go: An Idiomatic Approach to Real-World Go Programming》的中译版，中文版我还没有来得及读，不过原版我是粗略读过的。这本书面向Go入门群体，同时结合一些实战的例子，与《The Go Programming Language》的受众群体相似度很高。

这本书(原版)整体质量很高，语言精炼，讲解全面，更重要的是它似乎也是第一个包含Go泛型内容的Go入门书，只不过出版时，Go泛型尚未正式发布。今年3月份[Go 1.18泛型落地](https://tonybai.com/2022/04/20/some-changes-in-go-1-18)后，该书作者还对泛型章节做了修订，并在网上提供电子版供读者下载。

[《用Go语言自制解释器》](https://book.douban.com/subject/35909085/)和[《用Go语言自制编译器》](https://book.douban.com/subject/35909089/)2022.6.1

这两本都是索斯藤·鲍尔（Thorsten Ball）在2018年自出版的书！作者使用Go语言手把手教你实现了一门类C语法的Monkey语言，从词法分析、语法分析、建立语法树并进行语法分析，到生成字节码，并实现可以执行该字节码的虚拟机，实现Monkey语言的真实执行。这本书在国外颇受好评。

作者在书中采用的是手写词法分析器和语法分析器的方式，而不是借助[像ANTLR这样的parser生成工具](https://tonybai.com/2022/05/10/introduction-of-implement-dsl-using-antlr-and-go)，这可以让读者更加深刻的理解和认知一门编程语言的实现过程，酷感十足。

### 6. 小结

我们看到，2021年来出品的Go技术书籍都获得了不错的口碑，这也说明国内Go语言的整体水准在提升，对于刚刚加入Go社区的小伙伴们，这是真金白银般的好消息，**看好书可以避免走弯路**，节省大量时间与精力！

挑一本适合你的，该出手时就出手吧！


注意：以上豆瓣评分与微信读书推荐值都是2022.5.31的快照值，不代表后续不会发生变化。

[“Gopher部落”知识星球](https://wx.zsxq.com/dweb2/index/group/51284458844544)旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！2022年，Gopher部落全面改版，将持续分享Go语言与Go应用领域的知识、技巧与实践，并增加诸多互动形式。欢迎大家加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/。smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。2020年4月8日，中国三大电信运营商联合发布《5G消息白皮书》，51短信平台也会全新升级到“51商用消息平台”，全面支持5G RCS消息。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

- 微博：https://weibo.com/bigwhite20xx
- 博客：tonybai.com
- github: https://github.com/bigwhite

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2022, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

老师，您好，请问一下，微信读书上的电子版《Go 语言精进之路》是最新的正式版本吗？可以放心购买吗？

是的，是机械工业正版上传的。不过因为微信读书的平台问题，可能有一些代码存在html字符转义的错误（有读者发现的）。不过不影响阅读。

好的，谢谢。

请问， 《精通Go语言》书怎么样？

如果你说的是packt出版社的那本“ Mastering Go 3rd”，可以说它是packt出版社出的所有Go书里面还算比较不错的一本，可以一读。