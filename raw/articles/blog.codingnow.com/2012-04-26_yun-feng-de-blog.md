---
title: 云风的 BLOG
url: https://blog.codingnow.com/2012/04/
published: '2012-04-26'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

前段时间谈到了 [ringbuffer 在网络通讯中的应用](http://blog.codingnow.com/2012/02/ring_buffer.html) 。有不少朋友写 email 和我探讨其实现细节。

清明节放假，在家闲着无聊，就实现了一个试试。虽然写起来还是挺繁杂的，好在复杂度还在我的可控范围内，基本上也算是完成了。

设想这样一个需求：程序 bind 并listen 一个端口，然后需要处理连接到这个端口上的所有 TCP 连接。当每个连接上要数据过来时，收取这些数据，识别出封包，发送给对应的逻辑层处理。如果数据不完整，则暂时挂起这些数据，直到数据收取完整再行处理。

我写的这个小模块实现了这样一组特性，因为使用了唯一的 ringbuffer 缓存所有的连接，可以保证在程序运行过程中，完全没有额外的内存分配操作。

在编写时，一开始考虑到可能跨平台，想使用 libev, libuv, 或 libevent 来实现。可是仔细思考后，觉得这些库的 callback 模式简直是反人类，完全不符合自然的数据处理流程。使用起来体验非常糟糕。如果考虑到自己做 buffer 管理，想和它们原有的处理框架结合在一起，那实现过程绝对是一个噩梦。

在阅读 redis 的源代码过程中，我发现它并没有实现第三方的连接库，而是自己分别实现了 epoll kqueue select 的处理逻辑。简单清晰。而 epoll 这类 api 原本就相当的简洁，何苦去链接一个近万行的框架库把问题弄复杂呢？

所以，最终我自己定义了一组 API 接口完成需求：

struct mread_pool * mread_create(int port , int max , int buffer);
void mread_close(struct mread_pool *m);
int mread_poll(struct mread_pool *m , int timeout);
void * mread_pull(struct mread_pool *m , int size);
void mread_yield(struct mread_pool *m);
int mread_closed(struct mread_pool *m);
int mread_socket(struct mread_pool *m , int index);

暂时我不处理数据发送，让用户自己用系统的 send api 来完成，只关注 recv 的处理。这组 api 中，使用 create 来监听一个端口，设置最大同时连接处理数，以及希望分配的 buffer 大小就可以了。

库会为这个端口上接入的连接分配一个子连接号，而没有直接用系统的 socket 句柄。这可以方便应用层的处理。如果你设置了最大连接数为 1024, 那么这个库给你的编号就一定是 [0,1023] 。你可以直接开一个数组来做分发。

poll 函数可以返回当前可以接收的连接编号。可以设置 timeout ，所以有可能返回 -1 表示没有连接可读。

在 poll 之后，pull 函数可以用来收取当前激活的连接上的数据。你可以指定收多少字节。这个函数是原子的，要么返回你要的所有字节，要么一个字节都不给你。

由于库内部管理了接收 buffer ，所以不需要外部分配 buffer 传入。库的内部会识别，如果内部数据是连续的，那么直接返回内部指针；如果不连续，会在 ringbuffer 上重新开一个足够大的空间，拼接好数据返回。

buffer 的有效期一直会到下一次 poll 调用或是 yield 调用。

yield 函数可以帮助你正确的处理逻辑包。这是因为库还帮你做了一件事，如果你不调用 yield ，那么如果你 pull 了多少数据，再下一次 poll 调用后，同一个连接上，会重新 pull 到相同的数据。

举例说，如果你的逻辑包有两个字节的包头表示逻辑长度。你完全可以先 pull 两个字节，根据两个字节的内容做下一次 pull 调用。如果实际数据没有全部收到，你不必理会即可。如果手续收齐，那么调用一次 yield 通知库抛弃之前收取的数据即可。

当 pull 返回空指针，有可能是数据还没有收全，也有可能是连接断开。这时用 closed 这个 api 检测一下即可。


写了这么多，一定有同学想找我要源代码了。懒虫们，没问题。我已经提交到 github 上了。你可以从这里拿到 [https://github.com/cloudwu/mread](https://github.com/cloudwu/mread) 。

不过，这个只是我的节日娱乐之作。没有经过仔细测试，用在生产环境请务必小心，它几乎是肯定有 bug 的。另外，我只实现了 epoll 的部分，虽然扩展到 kqueue 或是 select / iocp 并不会太困难，不过假日过完了，也没空完善它了。

我由衷的希望有同学有兴趣有能力可以帮我完善这个库，让它更具有实用价值。写 email 给我，我会尽量配合。


这个东西的特点是什么呢？

我相信它足够高效，至少从 api 设计上说，可以实现的很高效。

因为它几乎就是直接调用 epoll 这些系统 api 了。而且尽量少调用了系统 api 。从实现上，每次 pull 调用，库都尽量多的读取数据并缓存下来，而不是按用户需求去收数据。

空间占用上，它也一点都不浪费，不会为每个独立的连接单独分配缓存。你大概可以根据你的网卡吞吐量和应用程序能处理的带宽，估算出一个合理的 ringbuffer 总量，那么这个库就应该可以正常工作。

就上一篇谈 ringbuffer 的 blog 我说过，当 ringbuffer 用满，它仅需要踢掉最早残留在系统里的挂起的连接。如果 client 是友好的（不发半个逻辑包），它几乎不会被踢掉。

libevent 这类库设计了一个 callback 框架，让你在每个连接可读时，采用 callback 函数来处理即将收到的数据。和这种用法相比，这个库的处理逻辑更加自然，也不需要你定制这定制那。复杂度被藏在里模块内部。外部接口和 socket api 一样简单易用，甚至更易用。因为它可以帮你保证逻辑包的原子性。