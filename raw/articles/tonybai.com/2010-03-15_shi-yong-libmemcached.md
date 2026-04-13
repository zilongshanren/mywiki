---
title: 试用Libmemcached
url: https://tonybai.com/2010/03/15/try-libmemcached/
published: '2010-03-15'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 试用Libmemcached

近期一直在做一个项目架构演化的讨论交流，为了解决产品中存在的某些问题，我们有意引入某种类[Memcached](http://memcached.org/)的开源产品，但我们的应用场景并非经典Memcached的“Cache”场景，这里也不详述细节了，大致就是这么一件事儿。

我们的第一选择是日本小伙儿[Mikio Hirabayashi](http://www.1978th.net/)实现的[Tokyo Tyrant](http://www.1978th.net/tokyotyrant/)，主要基于三点原因：

-> 支持数据的持久化

-> 快！（性能数据来自于网上的第三方资料）

-> 无商业许可证束缚

关于Tokyo Tyrant，其实网上是褒贬不一的，特别是在[这个网友的博客](http://hi.baidu.com/ah__fu)中谈到的Tokyo Tyrant的各种问题还是让人不免有些担心的。我们的产品应用场合对系统的稳定性有着及其严格的要求，所以不管开源产品本身宣传的有多么好多么稳定，我们在设计架构方案时还是要有自己的确保系统稳定运行的方案的。

一定的冗余是个简单而有效的保证系统稳定可靠的方案。Tokyo Tyrant本身支持主备运行方案，支持在主备Server之间近实时的同步数据，但方案带来的资源消耗开销以及不稳定的因素让我们不得不放弃了这种由服务端来完成冗余的方案。我们改由客户端来完成这件事。

Tokyo Tyrant兼容Memcached Protocol，使用常见的Memcached客户端即可完成对Tokyo tyrant的访问和各种数据操作。Memcached客户端中，我们首选人气最旺、使用者最多的[Libmemcached](http://tangent.org/)包。Libmemcached包目前还未发布1.0版，依旧处于积极开发阶段，代码在各个版本之间变动较大(你可比对一下0.34和0.38这两个版本)，Bug也就不可避免。在第一次试用过程中就发现了0.38版的一个BUG，大致是这样的：

模仿Libmemcached官方例子写了一个简单测试程序：

/* mctest.c */

[...]

memc = memcached_create(NULL);

servers = memcached_server_list_append(NULL, "10.10.0.1", 20001, &rc);

servers = memcached_server_list_append(servers, "10.10.0.2", 20001, &rc);

rc = memcached_server_push(memc, servers);

memcached_server_free(servers);

strcpy(value, "This is c first value");

rc = memcached_set(memc, "key1", 4, value, strlen(value), (time_t)180, (uint32_t)0);

[...]

return_value = memcached_get(memc, "key1", 4, &return_value_length, &flags, &rc);

[...]

rc = memcached_delete(memc, "key1", 4, (time_t)0);

[...]

memcached_free(memc);

编译执行该程序，程序执行到memcached_free时停了下来，并一直在wait。通过pstack查看进程栈：

ff2457c8 pollsys (ffbfb6b0, 1, 0, 0)

ff1e1d24 poll (ffbfb6b0, 1, ffffffff, 1, 3, 2db48) + 7c

00014800 io_wait (ffbfb6b0, ffffffff, 0, 0, ff26e308, 0) + 5c

00014980 memcached_io_read (36690, ffbfb7b8, 2004, ffbfb79c, ff390100,

2db48) + e4

00015aec memcached_quit_server (36690, 2000, 0, ff27333a, ff26e308, 19)

+ 130

00015b5c memcached_quit (2db48, ffbff9b4, ffbff9bc, 2db3c, ff390100,

ff390140) + 30

000153e8 memcached_free (2db48, ff27331c, 0, ff27333a, ff26e308, 19) + 4

000127fc main (1, ffbff9b4, ffbff9bc, 2db3c, ff390100, ff390140) + 2c0

000123d4 _start (0, 0, 0, 0, 0, 0) + 5c

程序一直在空Poll而无法退出。跟踪Libmemcached源代码，发现在memcached_quit_server的实现中有一处调用memcached_do时传入的参数似乎有问题：

rc= memcached_do(ptr, "quit\r\n", sizeof("quit\r\n"), true);

我翻看对比了0.34版代码，发现这块儿的sizeof("quit\r\n")用错了，应该使用strlen("quit\r\n")或者使用sizeof("quit\r\n")-1。修改并重新build后再执行a.out，一切OK! 看来我的判断是没错的。

我们希望产品运行过程中，任意TT server实例因异常的退出都不会影响到业务的正常运行。如何做？Libmemcached自带一种机制，针对同一份数据可在多个Server间Set多个复制品，同样在Get数据时也不用担心某一个实例异常退出。

验证这一方案也着实费了一些功夫：要使用replicas set，则客户端必须设置采用memcached binary协议：

rc = memcached_behavior_set(memc, MEMCACHED_BEHAVIOR_BINARY_PROTOCOL, 1);

rc = memcached_behavior_set(memc, MEMCACHED_BEHAVIOR_NUMBER_OF_REPLICAS, 2);

strcpy(value, "This is c first value");

rc = memcached_set(memc, "key1", 4, value, strlen(value), (time_t)180, (uint32_t)0);

但是设置了binary协议后，测试程序在memcached_set处挂起；一开始怀疑还是0.38版本的BUG，尝试换到0.34版本问题依旧；无奈采用抓网卡包的方式来定位问题，这才发现原来Tokyo Tyrant不支持Memcached Binary Protocol，根本没有给反馈应答，都怪事先没有细致的读完TT server的文档，走了弯路。

换用[Ubuntu](http://tonybai.com/2009/11/16/upgrade-to-ubuntu-9-10/)上运行的Memcached Server测试这一方案，结果依然不成；到Memcached官方去寻找答案，发现1.4以上的Memcached才支持Memcached Binary Protocol，而我的Ubuntu上的Memcached是1.2版本的；升级Memcached后，再测试，Set操作果然好用了。Get操作在Master Server完好的情况下是成功的，但是一旦手工停掉Master Server，则测试程序仍旧无法读取其他Replicas数据，这让我很疑惑。

又细想了一下，Libmemcached是一个通用的实现，对于满足我们特定业务的要求还有一定距离。Replicas机制不能直接使用，在Master Key Server宕掉的情况下，无论Set or Get都不能成功。一个简单的方案是通过“Set数据到”或“Get数据从”两组server list的方式来保证数据的冗余和安全性或在一组server list内部按一定规则做冗余存储，我们要做的只是封装出一个易用的接口罢了！

© 2010, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论