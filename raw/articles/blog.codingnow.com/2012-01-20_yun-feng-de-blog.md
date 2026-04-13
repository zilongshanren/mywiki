---
title: 云风的 BLOG
url: https://blog.codingnow.com/2012/01/
published: '2012-01-20'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

### libuv 初窥

过年了，人都走光了，结果一个人活也干不了。所以我便想找点东西玩玩。

今天想试一下 libev 写点代码。原本在我那台 ubuntu 机器上一点问题都没有，可在 windows 机上用 mingw 编译出来的库一个 backend 都没有，基本不可用。然后网上就有同学推荐我试一下 libuv 。

libuv 是 node.js 作者做的一个封装库，在 unix 环境整合的 libev ，而在 windows 下用 IOCP 另实现了一套。看起来挺满足我的玩儿的需求的。所以就试了一下。

这东西没有文档，暂时没看出来作者有写文档的打算，恐怕他是自己用为主。我 google 了一下，就是 github 上有[源代码](https://github.com/joyent/libuv)，.h 文件里有还算比较详细的注释。当然最主要是有些 test 程序，可以大概浏览其设计思路。

编译倒挺顺利，照着 test 写点小东西也不复杂。所以我也就逐步开始了解这个东东了。

老实说，对于一个别人写的库，我爱用不爱用主要是考察其 API 设计。也就是该怎么用，设计的好不好，有没有冗余设计。文档什么的其实不太所谓，反正有代码可以看嘛。

libuv 大体上我还算满意，用 C 实现可以加很多分。不过有些小细节我觉得还是有点小遗憾的。(这个遗憾是指，如果我自己来设计，绝对不会像这个样子）

最关键就是接口对 C 结构体布局的依赖性。这点我曾经因为 hiredis windows 版的缘故[吐槽过一次](http://blog.codingnow.com/2011/11/dev_note_2.html)了。以我自己的经验，似乎大多数 Windows 出身的程序员都有一点这种坏习惯。好吧，我也不知道怎么把这点和 windows 联系起来的，纯粹感觉而已。因为我自己以前做设计也有这个习惯。

为什么我觉得这样不好？

因为我觉得一个库，若想被人当成黑盒子去使用，以后也作为黑盒子来维护，甚至可以用别的盒子去替代它。关键的一点就是接口简单。这个简单包括了使用最少的概念、需要最少的知识去理解它。

文档通常是对接口无法自描述所需知识的一种补充。对一些例外的说明。而这些当然是越少越好。

我倾向于不在对外接口（对于 C 库来说，就是 .h 文件）中定义所用数据结构的具体布局。通常只需要一个名字即可。这个名字是用来做强类型约束的。

过多的结构定义导致了过多的概念，增加了接口复杂度。

接口的最小知识表达就是用一致的 C 函数调用约定。有明确的输入参数、输出参数。对于接口函数，应该是无全局相关状态的。这不仅仅是为了线程安全，而是可以保证没有隐式约定（额外的知识）。

如果某些行为需要用户设置或读取某个结构体的一个特定域，我觉得就是在 C 函数调用这一方式外，增加了一种改变模块行为的接口形式。或许这样做的成本比 C 函数调用要来的低，但我以为得不偿失。

尤其是、你的模块如果相当依赖这种形式：直接对结构体的特定域赋值的形式来交换信息。这种依赖可能来至于你对性能的追求。那我觉得一般都是整个模块的需求定义出了什么问题。一个独立模块需要解决的问题，通常对外界的信息交换应该是低频的，它应该是可以独立工作解决更复杂的问题的。而不应该是不断的要求外部告知它新的状态变换。

ps. 对于接口中的结构体定义问题。有另一种情况需要区分开。就是有大量的输入参数或输出参数需要一次性交换时，可以考虑定义一个结构体来做。这样比在 C 函数调用前压一大堆的数据去堆栈里要干净的多。

写了这么多，我是想说说我初步阅读 libuv 代码的感受。我碰到的第一个问题就是：libuv 用了大量 callback 机制来完成异步 IO 的问题。而这些 callback 函数通常都带有一个参数 `uv_stream_t`

或 `uv_req_t`

等。这个数据表示这次 callback 绑定的数据 。

我们知道， C 语言是没有原生 closure 支持的。若有的话，closure 应是 callback 机制最佳解决方案。而 C 语言模拟 closure 的方法是用一个 C Function 并携带一个 void * ud 。此 ud 即原本应该在 closure 中绑定的数据块。

这里，libuv 用的 `uv_stream_t`

大致上等同于这个 ud 。

问题出来了。用户在用这类异步 IO 库的时候，每次 IO 事件都需要绑定的行为需要的数据不仅仅是一个 stream 。还需要一些围绕这个 stream 做的动作所需要的一些其它数据。

我在阅读 `test/echo-server.c`

时看到这么一段：

static void after_write(uv_write_t* req, int status) { write_req_t* wr; if (status) { uv_err_t err = uv_last_error(loop); fprintf(stderr, "uv_write error: %s\n", uv_strerror(err)); ASSERT(0); } wr = (write_req_t*) req; /* Free the read/write buffer and the request */ free(wr->buf.base); free(wr); }

这里用了一次强制转换，把 `uv_write_t`

转换为 `write_req_t`

。为什么可以这样干，是因为 `write_req_t`

被定义成：

typedef struct { uv_write_t req; uv_buf_t buf; } write_req_t;

这里根据 C 结构布局，req 是第一个域，所以排在最前面。

这样做有点晦涩，我只能说感觉不太好。因为如果约定了 `uv_write`

接口传递的是一个 `uv_write_t`

类型的数据，这就明显是利用 C 语言特性来夹带私货了。

如果这是作者推荐的惯用法的话，我则这样理解：

libuv 其实在 API 上有个隐含约定。即回调函数的参数指向的地址偏移量为某个数值以后的数据是用户数据。这个数值为类型的尺寸。这类似 c++ 的继承。数据类型尺寸数值是编译时通过编译器来约定的。

而且，单就现在的用法，我认为更严谨的做法应该是类似 socket API ，显式的把传递的结构尺寸在函数接口表达出来（参考 socket connect 的接口定义中的第三个参数 addrlen）。 这样对库的接口稳定有好处。库可以知道用户有可能扩展数据，长度信息提示了库，传入数据体的真实大小。

btw, C++ 在用继承来完成类似设计时，则依靠了语言对 cast 的约定。C++ 语言的知识概念太多，很难完成简洁的模块接口约定。在我看来，这直接导致了 C++ 很难设计通用库，而只能设计专有框架。

我着一些疑惑阅读了不少 libuv 里的实现代码，尤其是 uv.h 的细节。我发现这样一个结构定义。

#define UV_HANDLE_FIELDS \ /* read-only */ \ uv_loop_t* loop; \ uv_handle_type type; \ /* public */ \ uv_close_cb close_cb; \ void* data; \ /* private */ \ UV_HANDLE_PRIVATE_FIELDS /* The abstract base class of all handles. */ struct uv_handle_s { UV_HANDLE_FIELDS };

注意这里有一个 data 域。从我的经验判断，这个域应该就是用来在一个 handle 上夹带用户数据的。由于没有文档确认，我只能从有限的代码阅读中来确认我的判断。我很奇怪没有定义一个明确的 api 出来绑定用户数据。因为在库的实现代码中也确实库自己用到过这个域，所以估计也不是库的使用者可以自由使用的。

当然对应的还有几处类似设计：

#define UV_REQ_FIELDS \ /* read-only */ \ uv_req_type type; \ /* public */ \ void* data; \ /* private */ \ UV_REQ_PRIVATE_FIELDS /* Abstract base class of all requests. */ struct uv_req_s { UV_REQ_FIELDS };

还有

struct uv_loop_s { UV_LOOP_PRIVATE_FIELDS /* list used for ares task handles */ uv_ares_task_t* uv_ares_handles_; /* Various thing for libeio. */ uv_async_t uv_eio_want_poll_notifier; uv_async_t uv_eio_done_poll_notifier; uv_idle_t uv_eio_poller; /* Diagnostic counters */ uv_counters_t counters; /* The last error */ uv_err_t last_err; /* User data - use this for whatever. */ void* data; };

这个 `struct uv_loop_s`

的 data 域倒是明确的注释可以随便使用了。

话说回来，这个绑定用户数据的需求我在早年阅读 Windows 的 MFC 实现时倒是见过另外一种解决方案。

Windows 的窗体有一个 SetWindowLong 的 API 可以让用户去设置一个用户数据。这样可以方便用户在用 C++ 封装的时候把一个 C++ 对象指针绑定在窗体 Handle 上。这样在窗口消息回调函数中就可以取回这个对象指针。

MFC 封装这些系统 API 时，可能是为了更通用，没有占用这个内置域，而是自己建立了一个全局的映射表。每次窗体消息回调时，查表来找到对应的窗体对象。这种非侵入式的方案，也凑合用吧。就是对于用 C/C++ 编写代码的追求性能的同学来说，或许有些小小不爽。

这就是我初步阅读 libuv 代码的一些简单看法。当然，我觉得 libuv 是个很不错的东西，不然我也不会饶有兴致的玩了一晚上。只是由于在这块投入时间精力不多，错误难免。有行家看到，一笑了之吧。