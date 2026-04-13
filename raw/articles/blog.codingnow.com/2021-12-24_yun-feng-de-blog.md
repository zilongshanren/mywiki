---
title: 云风的 BLOG
url: https://blog.codingnow.com/2021/12/
published: '2021-12-24'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

### 难产的 Lua 5.4.4

2021 年 12 月 21 日，Lua 发布了 Lua 5.4.4 rc2 。

Lua 5.4.4 这个版本相当难产。之前几个小版本从 rc1 到正式发布最多只有十几天，而这次这个版本已经过去一个月，看起来还不能正式发布。

因为，就在 rc2 发布几个小时后，在邮件列表的讨论中，有人就发现了一个 bug 。有趣的是，这个 bug 并不是 Lua 5.4.4 引入的，而已经存在了 10 年以上。

在 Lua 5.4.4 rc1 发布后，也曾发现 bug ，同样也不是新版本引入的。似乎最近两年，给 Lua 做测试的人群多了起来，新的测试方法找到了很多过去未曾发现的 bug 。这些隐藏颇深的 bug 几乎都和 GC 有关。GC 的 bug 难以通过单元测试的方式提前找到，即使被定位到，也很难理解，彻底修复更加困难。

在 Lua 5.4 刚发布不久，[新引入的分代 gc 中的一个 bug 就被讨论了很久才彻底解决](http://lua-users.org/lists/lua-l/2020-07/msg00071.html) 。Bug 发布两天后，[Lua 的作者表示对彻底解决 bug 还没有线索](http://lua-users.org/lists/lua-l/2020-07/msg00098.html) 。

Until now, I have no clues about this one. It seems to be a real problem in the GC, but it is hard to reproduce. Applying the previous fixes makes it disappear, but I cannot see how they could solve the bug.


我当时也饶有兴趣的分析了很久。拨茧抽丝般理解这种复杂 Bug 能带来极大的愉悦感，同时也深感彻底避免出问题是多么的不易。

Lua 5.4.4 这次遇到的问题不那么难，但也有 gc 有关。主要有两个，都和 finalizer 有关。

在 Lua 的 finalizer ，即 gc 元方法里调用 gc 的 api 有可能引发重入，而 Lua 的 gc 被设计成不能重入的。我相信这是一个正确的设计选择。gc 已经够复杂了，如果设计一个允许重入的 gc 会更难不出问题。

这个问题最终的解决方案是彻底禁止在 gc 元方法里调用 collectgarbage 。

gc 无法重入这一点，很多人都没有意识到。实际上，如果你在 finalizer 里使用内存，是退出 finalizer 前，是无法被回收的。也不可能在 finalizer 运行过程中，触发另一个 finalizer 的运行。从实现角度上讲，这个限制理所当然。但对使用者来说，限制似乎难以理解。在公布解决方案时，很多人质疑说，一旦在 finalizer 里禁止 gc ，会不会导致更容易发生 oom 错误？实际上，Lua 从加入 finalizer 特性开始到现在，已经是这样的。

另一个问题是在 finalizer 里构造了新对象，并添加了新的 finalizer 后，新添加的 finalizer 会排在已经在准备运行但尚未运行的其它 finalizer 之后运行。

如果你在 Lua 虚拟机关闭过程中，让这个新的 finalizer 运行 C 动态库中的函数，就可能因为 C 动态库先被 unload 而出错。这是因为，C 动态库是由最开始注册的 finalizer 负责卸载的。原本 finalizer 遵循先入后出次序运行，卸载 C 动态库通常是最后，就相安无事。但在关闭虚拟机的最后阶段，新对象在全部老对象释放之后生成了，它引用了被卸载的 C 动态库中的代码。

而 C 函数本身是一个 light C function ，实现上就是一个指针，是无法 mark 动态库对象的。

目前的解决方案是在虚拟机关闭的最后阶段，忽略新创建的 finalizer 。我认为可能还可以有更好的解决方案：比如，在最后阶段，新创建出来的 finalizer 不要等新一轮的 mark sweep 再进入 finalizer 链表，而直接串在finalizer 链表的最前面，这样也能保证最初创建用来卸载 C 动态库的 finalizer 最后运行。

目前 Lua 5.4.4 尚未正式发布，不知道还会不会进一步改动。

我认为这件事说明了几个道理：

从直接的方面说，我们在使用 finalizer 时，应该保证只在里面做非常简单的事情，除了释放 C 代码管理的资源外，什么都别做。这个原则不仅仅针对 Lua ，我想对其它带 GC 的语言也同样适用。对象的构建和释放往往是系统中最复杂的部分，Bug 的滋生之所，简单是对付复杂性的唯一良药。

从更宽泛的意义上讲，软件保持健壮是一件非常难的事情。对于基础设施，我们应保持足够简单，并尽量争取更多人的目光。正如 Eric S.Raymond 在《大教堂与集市》中提出的 [Linus 定律](https://en.wikipedia.org/wiki/Linus%27s_law)："given enough eyeballs, all bugs are shallow”。我觉得这里的 eyeballs 不是指绝对意义上的人数，毕竟程序员的水平可以差上数个数量级。在特定领域上找出特定问题的潜在人选，一共可能也没几个，只有在软件的用户有庞大基数的情况下，才偶尔能吸引那么几个重要的眼球过来看。

这里引用一下去年学到的草台班子理论：“我工作以后才发现，大家都是草台班子。政府草台，企业草台，我也草台，大家都草台，凑合赚钱过日子。一个企业，看着像一台奔驰在高速公路上的豪华轿车，里面其实是几个人蹬着自行车顶个壳。路上的车都是这样，大家谁都不戳破。”

对于大多数开发团体来说，都是草台班子构成的。你几乎不要指望他们不犯错误。这就是为什么我认为软件基础设施必须开源的原因：我们需要为那些最优秀的人提供机会，让他们能分出一些精力来对草台班子搭出来的草台修修补补。

恰巧前两天有网易的老同事来访，谈及新创业的游戏项目。我建议他们新的服务器基于 skynet 来做。倒不是说 skynet 设计的有多好，而是它已经被搭建了 10 年，已经拥有了很多很多不同的团队的眼球。它已经很久没有加新的特性、但已有的那些代码中，不断有发现新的问题。每解决一个 bug ，就增添一份信心。这是闭门造车的服务器框架很难取代的。