---
title: 云风的 BLOG
url: https://blog.codingnow.com/2013/09/
published: '2013-09-26'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

### Lua 5.2 新增的分代 GC

以前我在 blog 写过 [Lua 5.1 的 gc 代码分析](http://blog.codingnow.com/2011/03/lua_gc_1.html) ，而 Lua 5.2 对这部分代码改动颇多，暂时也没有精力更新这个系列，先挑重点写吧。

Lua 5.2 的 GC 的最大改进是增加了一种叫 generational 的模式，Lua 的官方文档里是这样解释的。

As an experimental feature in Lua 5.2, you can change the collector's operation mode from incremental to generational. A generational collector assumes that most objects die young, and therefore it traverses only young (recently created) objects. This behavior can reduce the time used by the collector, but also increases memory usage (as old dead objects may accumulate). To mitigate this second problem, from time to time the generational collector performs a full collection. Remember that this is an experimental feature; you are welcome to try it, but check your gains.

看起来 Lua 作者并不自信这个模式一定比之前的 incremental 模式更好，所以一再强调它是试验性质的。在邮件列表，几次表示这个特性[有可能在以后的 Lua 版本中移除](http://lua-users.org/lists/lua-l/2012-09/msg00094.html)。主要原因是它增加了 gc 模块的实现复杂度，却很难得到确实证据在实际项目中更有效。

我阅读了 lua 5.2.2 的相关代码，generational 大概是这样实现的。

在 generational 模式下，

清除阶段不再把处理过的黑色对象（不可清除对象）设置回白色（待扫描对象），而是给这个对象增加一个 OLDBIT 标记。由于 Lua 分配新的 GCObject 都是从一头加入对象列表的，所以在清除阶段一旦碰到有 OLDBIT 标记就可以不再遍历这个链表。

清除阶段大致可以只处理上次 gc 到目前新增加的对象，这样就达到了分代的目的。可以极大缩短每次 gc 清理的成本。（过去，比如至少把 VM 中所有对象都遍历一次，把其中的黑色对象变成白色，把白色对象释放）

由于清除阶段不再改变黑色标记，那么在新的一轮扫描的时候，也可以大大减少扫描的对象的数目。这是因为没有被碰过的老对象都是黑色的，而黑色的对象不再遍历。扫描过程只需要处理灰色对象，以及灰色对象引用的新对象（白色）就可以了。这意味着，在两次 gc 间没有被访问过的历史对象都不需要遍历。

generational 模式下，依然会定期触发完整的收集流程，它会比 incremental 模式下单步停留的久，是一个 stop-world 的操作，把所有对象都标记清除一遍。

但是，如果持久内存使用比较稳定，大部分临时对象都是短暂使用的话，触发完整收集的频率是很低的。 而且大部分临时对象都被快速清理过了，所以整体负担要小一些。

我个人认为 generational 模式比较适合在 Lua 程序中大量使用临时 table 或临时 closure 当参数传递的情况。Lua 没有把对象放在 stack 上的概念，所有临时对象都依赖 gc 一个个的回收。在老的 gc 算法下，只要对象增长速度过快，就一定会定期触发 gc ，而每个 gc 循环必须至少访问每个 vm 中的对象两次（一次标记，一次清除或重置标记）。这使得老的 gc 算法的效率严重依赖 vm 中的对象数量。在我们一些对 gc 时间敏感的应用中，都尽量少构造临时对象。这样虽然性能可以提高，却使得代码比较难看。

generational 模式就不太在乎临时对象的构建数量了，只要你不把它挂在老对象上，只在调用过程中临时当参数传递的话，那么 gc 就很廉价。大部分 gc 流程只需要扫描很少的对象，通常是那些从上次 gc 到当前被修改过的而被置灰的对象，以及新创建出来的对象。如果你的程序生成了大量临时对象，用完即弃，就意味着仅仅定期扫描 stack 就可以了。

如果游戏有明显的允许停顿的时刻，比如游戏切换场景，那么在这个时机强制做一次 fullgc 配合 generational 效果会更好。如果是以前的 incremental 模式，定期去做 fullgc 则没有那么明显的帮助。

ps. 在 lua 5.1 以前，用了一个叫 SFIXEDBIT 的标记位专门保护主线程。Lua 5.2 中估计是觉得用一个专门的标记来做这个事情有点多余，所以取消了 SFIXEDBIT 标记，而 OLDBIT 取代了它的位置。相应的改动是不再把 mainthread 和其它对象串在一起，而是在 GCSsweep 流程中对 mainthread 单独处理。