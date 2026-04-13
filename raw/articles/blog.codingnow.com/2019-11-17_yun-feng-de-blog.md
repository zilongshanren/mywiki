---
title: 云风的 BLOG
url: https://blog.codingnow.com/2019/11/
published: '2019-11-17'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

在 2017 年的时候，[我对 skynet 网络层的写操作做了一些优化](https://blog.codingnow.com/2017/06/skynet_socket.html) ，优化点是：如果 socket 并不繁忙，就不必把数据转达到网络线程写，而是直接写入 socket 。这可以减轻单线程网络层的负担，对于写操作频繁的场景会有极大的提升。

最近两天我想起来，如果大部分场合都可以通过直接写入 socket 而不必转发到网络线程发送数据的话，其实我们可以进一步的减少一次内存拷贝。

原来的设计是这样的：

所有待发送的数据由发送者打包成一个数据对象，转发给网络线程。网络线程真正把数据发送走了以后，再将这个对象销毁掉。

这个数据对象一开始只支持 malloc 分配出来的内存块。所以，api 的约定就是一个 `void *`

指针和一个 `size_t`

的长度。要求使用者遵循指针必须用 malloc 分配的约定。

后来，有不少同学希望在同一个数据块发送给多个 socket 的场景下，不用将数据复制成多份。通常的做法是给数据对象加一个引用计数。为了满足这类需求，我扩展了网络数据对象，允许支持自定义格式。方法是调用 `socket_server_userobject`

这个 api ，把 userobject 的接口传给网络层。

为了兼容过去的接口（保持一致的 abi ），我当时用了一个取巧的方法扩展接口。因为用户自定义对象是不需要长度的（用户对象接口中可以取到长度），而原始内存对象的长度必然大于等于 0 。所以就约定在发送接口中，长度传 -1 表示是用户对象。

这不是一个好的接口扩展的方法，这次想做进一步的扩展时，我想重新规范一下。所以就加了 `socket_buffer.h`

这样一个头文件，里面定义了新的网络发送的数据包的结构。目前是这样的：

#define SOCKET_BUFFER_MEMORY 0
#define SOCKET_BUFFER_OBJECT 1
#define SOCKET_BUFFER_RAWPOINTER 2
struct socket_sendbuffer {
int id;
int type;
const void *buffer;
size_t sz;
};

现在用 type 字段明确定义了数据类型。`SOCKET_BUFFER_MEMORY`

对应之前的 malloc 内存块；`SOCKET_BUFFER_OBJECT`

对应之前的用户定义数据对象；新增了 `SOCKET_BUFFER_RAWPOINTER`

用于 raw 指针。

raw 指针类型是告诉 skynet ，这个指针指向的数据可以直接使用，但是不能保存下来。如果需要缓存到之后再使用（通常是转发给网络层），需要自行拷贝。

有了新的数据类型，对 lua 层的 skynet.socket.send 这个 api 来说，如果发送的是一个 lua string ，那么就不必像之前那样，必须用 malloc 分配一块内存，把内容复制进去了。而只需要把 lua string 的内存地址传给 skynet ，如果 skynet 发送可以直接发送走，那么就不用额外拷贝。

新的 patch 在 sendbuffer 分支上，有兴趣的同学可以 review 一下这个 [patch](https://github.com/cloudwu/skynet/commit/41c77ba5cd2150265712735cb5457266951ae646) ，过几天我再合并到主干。

因为还是要兼容之前的接口，所以这次我新增了一组 api 取代旧 api 。用 `skynet_socket_sendbuffer`

代替之前的 `skynet_socket_send`

，等等。就有的 api 名字全部保留，改为用宏实现：

static inline void sendbuffer_init_(struct socket_sendbuffer *buf, int id, const void *buffer, int sz) {
buf->id = id;
buf->buffer = buffer;
if (sz < 0) {
buf->type = SOCKET_BUFFER_OBJECT;
} else {
buf->type = SOCKET_BUFFER_MEMORY;
}
buf->sz = (size_t)sz;
}
static inline int skynet_socket_send(struct skynet_context *ctx, int id, void *buffer, int sz) {
struct socket_sendbuffer tmp;
sendbuffer_init_(&tmp, id, buffer, sz);
return skynet_socket_sendbuffer(ctx, &tmp);
}


多说一点 skynet 网络层的设计想法。

我认为，skynet 网络层的设计目的是，把操作系统层面的 socket 数据从系统内核复制到用户空间，然后再把用户空间的数据地址交给各个不同的服务使用，同时也把用户空间需要发送的数据转移到系统内核中。

设计之初，我认为 skynet 会用于一个瓶颈不在网络传输层的场合。也就是说，网络 IO 收发的数据，传输所用的 cpu 开销是原小于处理这些数据的 cpu 开销的。所以，使用一个单独的唯一线程完成所有网络连接的收发，我认为是绰绰有余的。假定你只有一块网卡，那么单核的 cpu 处理能力，它所能达到的数据吞吐量，我认为是超过网卡的数据吞吐量的。

后来实际发现还有优化的余地，所以我把读写分离，大部分的写操作可以从网络线程移出。

下一步是否需要把读操作也移出？我目前的想法是还没有必要。或许有一天会增加多个线程读数据，把读操作从网络线程中分离出来，让网络线程只做 poll 操作。但我还是想把读操作保持在模块内部，也就是不把读操作的职责分离到外面去。

不过，lua 对 socket 的封装层我认为还有很大的改进空间。或许我们应该把网络层从内核里搬出来到用户空间中的数据，再次转移到 lua vm 内部的这个过程优化一下。

socket 的封装库可以实现一个线程安全的 buffer 统一管理所有读出的数据（而不是现在这样，每个 vm 的 socket 库都独立分开的拼装网络输入）。lua 的接口上，把输入数据生成 lua 的 string 这个过程，改成分析数据、消费数据两个阶段。分析数据可以直接针对 C 层的 buffer 直接进行，而不一定要复制成 lua string 。而分析使用完数据后，再调用消费接口，通知下层说，已经用掉了这些数据。

如果不调用消费接口，就可以在分析完数据后，若发现该数据不该自己处理，就直接转移交别的服务。因为数据并没有消费，其它服务就能直接重新从 C 层分析使用。