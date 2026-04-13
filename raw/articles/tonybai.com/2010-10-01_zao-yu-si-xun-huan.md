---
title: 遭遇“死循环”
url: https://tonybai.com/2010/10/01/encounter-endless-loop/
published: '2010-10-01'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 遭遇“死循环”

昨天看了“[外刊IT评论](http://www.aqee.net)”上的一篇名为《[软件编程21法则](http://www.aqee.net/2010/09/30/21-laws-of-computer-programming/)》的文章，文章中提到的一条法则是：“软件直到被变成产品运行至少6个月后，它最严重的问题才会被发现”，当时表示认同。不过仅仅相隔一天，这条法则就变成了眼前的现实。

今天上午我们的某版本系统在某省出现了故障，该版本在这个省上线恰好将近6个月^_^，系统上线以来一直运行良好，直到这次故障。故障现象为"挂死":所有进程都挂死在某一把锁的lock上。以前出现这种情况多为某个进程加锁后，在锁内异常退出，未能释放锁而导致其他进程挂死。这种"挂死"多是代码中[访问非法内存地址](http://tonybai.com/2006/09/06/be-careful-of-the-trap-of-overflow/)导致的，一般都会有core文件dump出来。不过这次出现挂死后，我们并未找到core文件的影子。查看系统运行日志也无果。通过脚本将所有该应用的子进程的运行栈快照收集到一个文件中，然后对这个数据庞大的文件进行分析，以试图找到一些蛛丝马迹。

分析发现绝大多数子进程都挂起了，其运行栈栈顶多为：

lwp_mutex_timedlock (f1444c28, 0)

不过只有一个进程与众不同，它的[栈顶](http://tonybai.com/2005/11/24/assembly-series-review-stack-operation/)是一个我们自己实现的函数，这里暂且称这个函数为foo_func吧。迅速查看foo_func的源码实现，发现一个while循环，第一时间想到:是不是foo_func进入while死循环了？在故障应用主机上用top查看一下系统运行状态，发现确有一个进程占用cpu很高，而且持续很高。pstack一下这个进程，栈顶端果真就是foo_func，“死循环”的推论是正确的。 即使这个进程死循环了，怎么会连累其他进程也停止工作了呢？原因就在于这个死循环是在这个子进程获得锁之后发生的，因为死循环了，导致无法释放这把锁，其他子进程干着急也无可奈何！

foo_func为何能进入死循环？仔细斟酌一下foo_func的代码也不难得出：代码中混用了int和unsigned char，导致数组下标值变为负数，数组访问溢出，读取到的值是随机值，所以死循环也是随机发生的（之前几个月运行都良好也是因为这个原因）。 C语言不是[强类型](http://en.wikipedia.org/wiki/Strong_typing)的，int和unsigned char两个宽度不同的类型可以放在一起使用。C编译器帮你做隐式转换，转换规则虽不十分复杂（[C99](http://en.wikipedia.org/wiki/C99)引入了rank概念后，转换规则略就显复杂了），但也很容易犯错，这也是我们常说的C陷阱之一。另外foo_func代码本身的功能逻辑也有漏洞，这里就不细说了。

© 2010, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论