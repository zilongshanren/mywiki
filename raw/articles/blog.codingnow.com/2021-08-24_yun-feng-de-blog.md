---
title: 云风的 BLOG
url: https://blog.codingnow.com/2021/08/
published: '2021-08-24'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

### 内存对齐问题和编译器优化

昨天在公司内部的“不作不死”（程序员）群里，有同学贴了个[知乎上的帖子](https://www.zhihu.com/question/435258463/answer/1969561682) 。表示这个问题居然关闭 gcc 的 builtin-memset 就解决了，感觉很玄学。

我说，这个感觉才是对的。关于文章中表达的 “**添加编译选项-no-builtin-memset后，一切就正常了。然后大家都如释重负，不但解决了问题，又学到的新知识。**” ，我认为这“如释重负”对于程序员来说才是种不正常的感觉，正常应该是“更加困扰”了才对呀。

到底是怎么回事，文章线索不全，无法判断。不过我直觉上感觉和我前几个月在我们这个“不作不死”群里讨论过的另一个问题非常相似。

我怀疑，问题是内存不对齐造成的。

[当时有同事发现了我给 skynet 写的序列化库在 arm 32 下有机会引起崩溃](https://github.com/cloudwu/skynet/pull/1427) 。由于 skynet 从一开始就有不少基于嵌入式平台的应用，所以实现时特别有注意不同平台的问题。我一度认为使用 memcpy ，而不去直接对地址取值就能回避内存对齐问题。

经过那次后，我仔细阅读了 C 标准，查了许多资料，重新理解了一下 C 语言的内存对齐。在 C1x 标准中，还增加了 stdalign.h 可以用 alignas 去精细控制对齐。

现代 C 编译器会对 C 代码基于标准允许的推断做相当深入的优化。很多看似函数调用的地方都很有可能根据上下文优化为更简单的目标码。比较典型的就是针对 memset memcpy memmove 的优化。

我们知道，当内存非对齐时，即使硬件不报错，也会有很大的性能惩罚，而且一旦引起问题是非常难查的。所以我们要尽量回避对非对齐的内存访问。

Some architectures are able to perform unaligned memory accesses transparently, but there is usually a significant performance cost.

Some architectures raise processor exceptions when unaligned accesses happen. The exception handler is able to correct the unaligned access, at significant cost to performance.

Some architectures raise processor exceptions when unaligned accesses happen, but the exceptions do not contain enough information for the unaligned access to be corrected.

Some architectures are not capable of unaligned memory access, but will silently perform a different memory access to the one that was requested, resulting in a subtle code bug that is hard to detect!


而如果 memcpy 和 memset 这些的标准库函数，如果以函数的形式提供功能，就必须在运行时再检查所操作的内存地址是否对齐，根据是否对齐实现不同的版本。

这里编译器优化的介入，可以根据上下文尽可能的推断出更多信息：传入地址是否对齐？操作长度是否是常量？根据这些信息则可以减少很多运行时不必要的分支判断。

语言本身的规范可以方便编译器做这些判断。例如，虽然 memcpy 本身的定义是 void * ，但如果上下文中这个指针是从 int64 指针转换而来，就能推断出地址一定是 64bit 对齐的。这是符合语言规范的。所以你不可以随意的将两个不同对齐标准的指针相互强制转换。

话说回来，如果真的遇到了编译器优化导致 bug 怎么办？我认为正确的姿势是尽力搞清楚问题的本源。起码应该让编译器输出汇编对比阅读一下。编译器输出了不是自己预期的结果的话，首先还是要怀疑自己的代码是否不够标准，导致编译器错误理解了你的意图。如果真的是编译器优化问题，应该把 issue 投递到编译器的开发社区，协助编译器的开发团队解决问题。而同时选择绕道只应该是个不应该自己软件发布时间的权宜之计。

btw, 最近一年在 lua 5.4 发布之前，lua 社区就发现过 gcc 的不正确优化导致的 bug ，马上就有人把问题同步到 gcc 社区，进而跟进解决了问题。

现代软件开发，上下游其实是一体的。只有每个环节的开发人员都不放过潜在的问题，整体才可以做的更好。