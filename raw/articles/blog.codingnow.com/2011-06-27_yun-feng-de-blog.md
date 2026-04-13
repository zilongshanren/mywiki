---
title: 云风的 BLOG
url: https://blog.codingnow.com/2011/06/
published: '2011-06-27'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

最近 Lua 社区非常活跃。6 月 22 日发布了 Lua 5.2.0 (beta-rc2) 。今天(6 月 24 日) 发布了 LuaJIT-2.0.0-beta8 。

虽然 luajit 和 lua 5.2 还有点小矛盾，luajit 没有完全支持 lua 5.2 的迹象。不过，这些对 Lua 社区都是好消息啦。可能对于 lua 用户会有点小纠结，到底是追随官方的 5.2 版呢，还是去用性能更好的 luajit2 。我比较在意性能，暂时先投靠 luajit 了。反正和 5.2 区别也不大。更重要的是，luajit2 提供的 ffi 库相当之好用，极大的减少了我们写 C 库的 lua binding 的负担。从某种角度可以看到另一个问题，为基础设施模块设计出良好的 C 接口（而不是 C++ 的）是多么的重要。

zeromq 是用 C++ 实现的，但它提供的是简洁纯粹的 C 接口。这让它相当利于 binding 到其它语言中使用。之前，已经有了成熟的 [lua-zmq](https://github.com/Neopallium/lua-zmq) 可供使用。它分别实现了 ffi 和不带 ffi 的版本。不过也正因为此，封装层包裹的很淡疼。如果只支持 ffi 版本的话，其实这个工作可以做的非常简洁。

出于实践 luajit ffi 库的目的，也为了让这部分代码看起来清爽一点。我花了半个下午自己封装了一下 zeromq 。所用时间比在 windows 下配置安装那个现成的 lua-zmq 所用时间看起来更少（不需要装 msys ，cmake 等等淡疼的玩意）。谁再下面留言说不要重复造轮子了，我也不打算跟它急了。吵架的时间都比写代码时间长。我们从来不会把写一遍 hello world 看成重新制造轮子不是么？使用 ffi 去 binding C 库实在是太容易了，不比写 hello world 更复杂。

为了鼓励各位同学自己造轮子，我就不把我的实现完整列出来了。希望在 lua 下使用 zeromq 却懒的学习的同学请自己下载上面提到 binding 库好了。

说说我的体会：

zeromq 在 windows 下用 gcc 编译挺麻烦的，我是找一个装了 vc 的同学帮我利用官方的 vs 工程编译出的 dll 文件使用。因为都是 C 接口，所以可以直接 link 到 gcc 项目里。

zeromq 的 api 设计的很精巧合理。总数量扳着手指都数的过来。不过我们对其做适当改造会做起来更轻松一点。

比如：

`void *zmq_init (int io_threads);`


它返回的是一个 context 对象，出于 C API 设计方便，所以使用的是 void * 。

后面的

`void *zmq_socket (void *context, int type);`


接受参数正是这个 context 对象，并返回一个 socket 对象，这里依然是 void * 。

我做了一点小修改，把这两个 api 改为了：

typedef struct {} context;
context *zmq_init (int io_threads);
typedef struct {} socket;
socket *zmq_socket (context *context, int type);

就是说，给它们起了专门的类型名。这样做有什么好处呢？在 lua 代码中，我们可以利用 ffi.metatype 给它们加方法了。虽然 lua 本身的 table 也可以有 metatable 。但利用 ffi.metatype 可以少一个间接层，性能更好，代码更简洁。

我是这样写的：

local context = {}
function init(io_threads)
return newobj(libzmq.zmq_init(io_threads or 1))
end
function context:term()
return check(libzmq.zmq_term(self))
end
-- Socket types
PAIR = 0
PUB = 1
SUB = 2
REQ = 3
REP = 4
DEALER = 5
ROUTER = 6
PULL = 7
PUSH = 8
XPUB = 9
XSUB = 10
local socket = {}
function context:socket(type)
return newobj(libzmq.zmq_socket(self, type))
end
ffi.metatype("context", { __index = context } )

这里 newobj 函数检查返回值是不是 NULL ，如果返回空指针，就利用 strerror 取得错误信息。

local function strerror()
return ffi.string(libzmq.zmq_strerror(libzmq.zmq_errno()))
end
local function newobj(obj)
if ffi.cast("void *",obj) > nil then
return obj
else
return false , strerror()
end
end

我在 ffi 文档中没有找到明确的，判断一个指针是不是 NULL 的方法，琢磨了一下，应该是用 `ffi.cast("void *",obj) > nil`

不知道是不是惯例。

msg 对象我做的时候保留了完全一致的 C api ，但实际在高层使用的时候不太方便，所以做了进一步的 lua 层封装。类似这样的：

function socket:send_string(str)
local m = msg(str)
local err = self:send(m)
m:close()
return err
end
function socket:recv_string()
local m = msg()
local err = self:recv(m)
if err == nil then
local ret = m:tostring()
m:close()
return ret
else
return false, err
end
end

不过我认为性能会有点小问题，如果用 lua 做比较底层的设施，我认为还是用更直接的 msg api 比较好。我想，zeromq 的应用场合偏中低层。应该能够定义出明确需求。使用 luajit 开发，我们在这个层次上应多从 C 的角度去思考（良好使用的 luajit 可以达到 C 的性能级别，但需要多理解和推敲，jit 也不是免费的午餐）。做出更好的封装后，再提供更高层次的接口供上层调用。不大有必要在下面的层次考虑便利性。

setsockopt 和 getsockopt 从 C 接口的角度上看，提供了足够多的灵活性。但表现为 lua 的 api 我认为不宜照搬。因为 C 接口不宜扩展，但 lua 却不一样。这个最好还是根据需要，封装更具体的功能。这些也不是性能敏感的接口，可以多做一些类型检查。


最后正经点说，没有全部公开源代码，其实是因为我觉得根据我的个人需求，我希望将 zeromq 和 google protobuf 做更紧密的结合。放在一起做成一个完整的功能模块。[我之前为 lua 定制了一个 protobuf 库](http://blog.codingnow.com/2010/08/proto_buffers_in_lua.html) 同样也没有开源，也是因为我认为其功能不完整。

所以更进一步的工作是把它们做深度的整合。

ps. 真的想要我写的这个玩意的同学（虽然我觉得也就是 2 小时的工作而已），可以私下找我要。