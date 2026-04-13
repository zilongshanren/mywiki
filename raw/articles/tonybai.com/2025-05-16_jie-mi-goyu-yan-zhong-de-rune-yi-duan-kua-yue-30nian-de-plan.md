---
title: 揭秘Go语言中的rune：一段跨越30年的Plan 9往事与UTF-8的诞生传奇
url: https://tonybai.com/2025/05/16/how-rune-came/
published: '2025-05-16'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 揭秘Go语言中的rune：一段跨越30年的Plan 9往事与UTF-8的诞生传奇

![](../../assets/de31415223ac3c83.png)


[本文永久链接](https://tonybai.com/2025/05/16/how-rune-came) – https://tonybai.com/2025/05/16/how-rune-came

大家好，我是Tony Bai。

作为 Gopher，我们每天都在和 rune 打交道。在 Go 语言中，它通常被解释为“一个 Unicode 码点”，官方文档也说引入这个术语是为了“简洁”。但你是否曾好奇，这个略带神秘色彩的词汇，究竟源自何方？仅仅是为了简洁吗？

最近，[Connor Taffe的一篇精彩博文](https://connor.zip/posts/2025-05-03-rune)以及 [Go语言之父 Rob Pike 的亲自确认](https://bsky.app/profile/robpike.io/post/3lokt3qzvos2h)，为我们揭开了一段跨越三十余年，从 Plan 9 操作系统到 UTF-8 编码诞生，再到 Go 语言的历史传奇。今天，就让我们一起，深入 rune 背后的故事。

## 一句“简洁”，一段 Plan 9 往事

Connor文章中引用的Adam Pritchard的关于[限制字符串长度](https://adam-p.ca/blog/2025/04/string-length/)的文章中提到：“请注意，在 Go 中，Unicode 码点通常被称为‘rune’。（Go 似乎是为了简洁而引入了这个术语。）” 而 Go 官方博客《[Strings, bytes, runes, and characters in Go](https://go.dev/blog/strings)》也说：“‘Code point’有点拗口，所以 Go 引入了一个更短的术语：rune。”

![Rob Pike 在 Bluesky 上的发言截图](../../assets/678da863e83750b7.png)


然而，真相远不止于此。Rob Pike 最近在 Bluesky 上澄清(如上图)，rune 这个词实际上是 **Ken Thompson** 在一次为 Plan 9 寻找一个不同于 char（用于字节）的类型名称的头脑风暴中“得意地”提出的，Rob Pike 当即表示赞同。更关键的是，Rob Pike 随后确认，**这个命名发生在 Plan 9 为 UTF 和 ISO 10646 寻找类型名称的时期，具体是1991 年 12 月 8 日的晚上**！远早于 Unicode 和 UTF-8 的广泛应用，也比 Go 语言的诞生早了数十年。

是的，你没看错，rune 的故事，始于 Plan 9，那个由贝尔实验室传奇人物们（包括 Rob Pike, Ken Thompson 等）创造的操作系统。Go 语言深受 Plan 9 的影响，从链接器架构、并发原语 channel、标识符大小写的可见性规则，到对简洁性的极致追求，都带着浓厚的 Plan 9 印记。rune 便是这血脉传承中的一环。

## 餐巾纸上的革命：UTF-8 的诞生传奇

要理解 rune 在 Plan 9 中的意义，就不得不提 UTF-8 的诞生。Connor 的文章中引用了一封 Rob Pike 在 2003 年的邮件，详细披露了这段鲜为人知的历史，纠正了“IBM 设计 UTF-8，Plan 9 实现它”的说法。

故事发生在 1992 年 9 月左右的一个晚上，新泽西一家小餐馆的餐巾纸上：

**缘起：**Plan 9 当时使用 ISO 10646 最初的 UTF（一种16位字符编码）来支持宽字符，但团队对它非常不满。Rob Pike 形容道：“UTF 太糟糕了。它有模192的算术，而且在没有除法硬件的老 SPARC 机器上几乎不可能高效实现。像【/*】这样的字符串可能出现在西里尔字符中间，导致你的俄文文本变成一个 C 语言注释。还有更多问题。它作为一种编码根本不实用。”**契机：**一天下午，X/Open 委员会的一些人（据 Rob Pike 回忆可能来自 IBM 奥斯汀）打来电话，希望 Ken 和 Rob 审查他们的 FSS-UTF (File System Safe UTF) 设计。Ken 和 Rob 意识到这是一个用他们的经验设计一个真正优秀的标准，并让 X/Open 将其推广出去的机会。**餐巾纸上的灵感：**他们接受了挑战，条件是必须快速完成。于是，在那个决定性的晚餐上，**Ken Thompson 在餐巾纸上构想出了 UTF-8 的位打包方案。****闪电般的实现：**晚餐后回到实验室，他们便向 X/Open 解释了新方案，并承诺在周一前（据信是 X/Open 的重要投票日）拿出一个完整的运行系统。当晚，Ken 写了打包和解包代码，Rob Pike 则开始修改 C 库和图形库。到周五的某个时候，Plan 9 已经完全运行在后来被称为 UTF-8 的编码上了。

Rob Pike 在邮件中强调，他们之所以要“另起炉灶”，是因为 FSS-UTF 缺少他们认为至关重要的特性之一：**支持定位到文件或流的中间，并读取有效字符，或处理损坏的字符。** Ken Thompson 设计的 UTF-8 完美地解决了这个问题。

对比 Ken Thompson 当时提出的 UTF-8 方案(如下图)和 FSS-UTF，我们可以看到 UTF-8 的精妙之处：后续字节以 10 开头，与首字节的 110、1110 等模式区分开来，确保了自同步性和对 ASCII 的兼容性。

![](../../assets/278be2241bd650a2.png)


## Rune 的首次亮相与演变

那么，Rune 这个词是什么时候正式与这种新的字符表示方式联系起来的呢？Rob Pike 在其关于 Plan 9 UTF-8 实现的论文《Hello World》中写道：

“在语义层面上，ANSI C 允许（但并未限制）宽字符的概念，并且允许此类字符串和字符常量。我们选择 unsigned short 作为宽字符类型。在库中，Rune 一词由 typedef 定义为等同于 unsigned short，并用于表示 一个Unicode 字符。”


这似乎是 Rune 作为一种特定类型名称，用于指代 Unicode 字符（码点）的最早文献记录。最初在 Plan 9 C 中，Rune 是一个 16 位无符号短整型，足以表示当时的 Unicode 基本多文种平面（BMP）。

而到了 Go 语言，rune 被定义为 int32 的别名。这是因为自 1992 年以来，Unicode 已经扩展，需要更大的空间来表示所有码点（UCS-4 定义了 31 位码空间）。Go 语言标准库中的 unicode/utf8 包也定义了 UTFMax = 4，表明一个 rune 最多可以用 4 个字节的 UTF-8 编码表示。有趣的是，在 Russ Cox 移植的 plan9 port 中，Rune 类型在 2009 年末也被修改为了 unsigned int，同样是为了支持更广的码点范围。

Ken Thompson 在最初的邮件中提到：“4、5 和 6 字节序列只是出于政治原因才存在的。我更愿意删除它们。” 这也印证了早期设计者对编码效率和实用性的极致追求。

## Rune 的足迹：从 Plan 9 到更广阔的世界

Rune 这个术语，并没有止步于 Plan 9。通过 Paul Borman 的贡献，Plan 9 的 rune 功能被整合进了 4.4 BSD。从此，rune 开始在更广阔的 Unix 世界留下足迹：

**FreeBSD**继承了 4.4 BSD 的 rune 函数，尽管后来推荐使用 ISO C99 的宽字符工具。**Apple 的 Darwin 内核**，作为 BSD 的衍生，也包含了 rune_t 类型。- C 标准库实现如
**newlib**也包含了源自 BSD 4.4 的 rune 功能。 **Android**通过 plan9port 移植了 Plan 9 的 libutf，其中自然也包含了 rune。- 甚至，
**微软的 .NET**在引入 System.Text.Rune 类型时，其灵感也明确来自 Go 语言，[这在其 GitHub issue 中由 Miguel de Icaza 提及](https://github.com/dotnet/runtime/issues/23578)。

可见，rune 这个由 Ken Thompson 灵光一闪提出的词汇，承载着一段从贝尔实验室 Plan 9 开始，经由 BSD 社区，最终深刻影响了包括 Go 在内的现代编程语言和操作系统的字符处理历史。

## 小结：rune 不只是简洁

通过Rob Pike的亲自确认，我们应该知道，当我们今天再看到 Go 语言中的 rune 时，它不仅仅是为了“简洁”而对“Unicode code point”的替换。它是一个承载着厚重历史的符号，是 Go 语言设计者们深厚技术底蕴和创新精神的体现，是 Plan 9 简洁哲学与 UTF-8 实用主义的结晶。

理解 rune 的来龙去脉，有助于我们更深刻地体会 Go 语言在文本处理、字符串操作以及 Unicode 支持方面的设计考量，也让我们对这门语言背后的巨匠们多一份敬意。下一次，当你在 Go 代码中写下 rune 时，或许会想起那个在新泽西餐馆餐巾纸上诞生的传奇，以及那段跨越三十余年的 Plan 9 往事。

## 参考文献

[Rune by Connor Taffe](https://connor.zip/posts/2025-05-03-rune)– https://connor.zip/posts/2025-05-03-rune[Rob Pike on Bluesky, re: origin of “rune”](https://bsky.app/profile/robpike.io/post/3lokt3qzvos2h)– https://bsky.app/profile/robpike.io/post/3lokt3qzvos2h[Rob Pike, Email “UTF-8 history”](https://www.cl.cam.ac.uk/~mgk25/ucs/utf-8-history.txt)– https://www.cl.cam.ac.uk/~mgk25/ucs/utf-8-history.txt[Rob Pike, “Hello World” (Plan 9 UTF-8 implementation paper)](https://connor.zip/resources/pdfs/utf8.pdf)– https://connor.zip/resources/pdfs/utf8.pdf

**聊一聊：**

**在了解了 rune 的历史后，你对 Go 语言的设计是否有新的认识？****UTF-8 诞生的故事中，有哪些细节让你印象深刻？****你认为这种对历史渊源的挖掘，对我们理解和使用一门编程语言有何帮助？**

欢迎在评论区分享你的看法！如果你觉得这篇文章有趣且有价值，也请**转发给你身边的 Gopher 朋友们**，让更多人了解 rune 背后的故事。

今天我们一起挖掘了 rune 这个小小术语背后波澜壮阔的历史，感受到了 Go 语言与 Plan 9、UTF-8 的深厚渊源。**真正理解一门语言，往往需要我们深入其“根源”，探究其设计选择背后的“为什么”。**

这里，我邀请你加入我在**极客时间**的专栏 **“TonyBai · Go 语言进阶课”**。

在这门课程中，我们将一起：

**夯实基础，突破语法认知瓶颈：**深入剖析那些看似熟悉却暗藏玄机的核心概念。**设计先行，奠定高质量代码基础：**学习如何进行合理的程序骨架、并发设计、包设计、接口设计以及API设计。**工程实践，锻造生产级 Go 服务：**掌握构建可观测性、性能调优、故障排查等硬核技能。

**理解“过去”是为了更好地走向“未来”。** 就像我们今天了解 rune 的故事一样，在《Go语言进阶课》中，我们将一起探索更多 Go 语言的设计精髓与实践智慧，助你完成从“熟练”到“精通”的蜕变。

**扫描下方二维码或点击[阅读原文]，立即加入，开启你的 Go 语言精进之旅！**

![](../../assets/ab2d7a5176ba4b48.png)


期待与你在极客时间相遇，共同探索 Go 语言的深层魅力！

商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。如有需求，请扫描下方公众号二维码，与我私信联系。

![](../../assets/769fc94e8bba6b65.png)


© 2025, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论