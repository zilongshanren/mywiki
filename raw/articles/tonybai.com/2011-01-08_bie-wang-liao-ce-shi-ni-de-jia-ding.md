---
title: 别忘了测试你的假定
url: https://tonybai.com/2011/01/08/do-not-forget-to-test-your-assumption/
published: '2011-01-08'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 别忘了测试你的假定

周四下午，收到同事的一封mail，他告诉我他的业务代码中使用的一个库接口的行为与预期不同，并在mail中给出了测试代码和测试结果。而这个接口是之前由我封装实现的。

这个库仅仅是对[libevent](http://monkey.org/~provos/libevent)做了一层薄薄的封装，目的是使其接口的使用方式符合部门的一贯风格。虽说封装简单，但[单元测试](http://tonybai.com/2005/11/08/the-design-and-implementation-of-c-unittest-framework/)也是一应俱全，不敢马虎，必要的地方[mock](http://tonybai.com/2008/04/12/mock-test-in-c-unit-test/)也一并上阵，总体来说我个人还是比较满意的。

不过还是出现了问题，问题出在libevent提供的timer的行为上。这是我们第一次使用libevent，我基于以前对timer的事件处理机制的理解作出了错误的假定：libevent提供的timer是PERSIST的。同事的测试结果却表明这个timer设定是一次性的：只运行一次便失效了，除非在timer的callback handler中重新添加timer事件。

《[程序员修炼之道](http://book.douban.com/subject/1152111/)》中在介绍如何深思熟虑而不是靠巧合编程时说过：要测试你的假定。我恰恰是在这块儿犯了错误。尚没有明确libevent的行为就做出了假定而且没有对这个假定做细致测试，最终导致了这个问题的发生。

这个问题最终是这么解决的：了解了一下，libevent 1.x.x版本确实不支持persist timer事件处理，但是在libevent 2.x.x版本中，作者增加了对persist timer的支持。我们原本使用的是1.4.10的libevent，为了支持persist timer，我将库升级到2.0.10(已经是stable版了)。不过仅仅是升级库版本还是不行的。我们不能直接使用libevent提供的evtimer_set接口，因为使用该接口后，我们得到的依旧是一次性的timer。这里需要用event_set(e, -1, EV_PERSIST, eh, arg)替代evtimer_set(e, eh, arg)，这样设置后得到的timer才是persist的。

© 2011, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

您好，我需要升级 libevent 从 1.4 到 2.0, 下载文件，config, make, make install 安装到了 /usr/local/lib 下

软连接到 /usr/lib 不成功

删除 /usr/lib/libevent*

copy /usr/local/lib/libevent* 到 /usr/lib 还不行

新手请教，应该如何升级，盼回复，谢谢。