---
title: 云风的 BLOG
url: https://blog.codingnow.com/2015/05/
published: '2015-05-19'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

Lua 作为一门嵌入式语言，提供了完备的 C API 供 Lua 代码和宿主程序交互，当然，宿主语言最好是 C 或 C++ 。如果是其它语言，比如最近两年流行的在 mono 环境嵌入 Lua 另当别论。

正确将 Lua 嵌入是不太容易做对的事情，很多刚接触 Lua 的人都容易犯错误。好在做这种语言桥接工作都是项目开始阶段的设计者做的，不必人人学会，所以只要有熟悉 Lua 的人来搞，犯错误的危害不会太大。而且即使做的有问题，日后修改也比较容易。这篇 blog 主要就是谈谈，最容易做错的位置，和一些正确（但看起来麻烦）的实现方法。

最容易忽略的是 Lua 中 error 的处理。

Lua 中叫 error ，再其它语言中叫 exception ，后面姑且全部称为异常吧。

如果你认真读过 [Lua 的手册](http://www.lua.org/manual/5.3/manual.html)。 就会发现，在所有 C API 那里，都注明了这个 API 是否会抛出异常。比方说 `lua_tostring`

就标注的是 `[-0, +1, e]`

，有可能抛出异常（是不是和你的直觉不同？）；但 `lua_pushlightuserdata`

则不会。

Lua 的异常应该由 `lua_pcall`

或 `lua_resume`

来捕获，所以当你调用 C API 的时候，应该确保在 C 的调用层次上，处于某次 `lua_pcall`

或 `lua_resume`

中。所以，即使是常见的创建 Lua 虚拟机的简单几行代码，都有可能写错。比如：

lua_State *L = luaL_newstate();
if (L) {
luaL_openlibs(L);
}

这样写就是考虑不周的。因为 `luaL_openlibs(L)`

可能抛出异常，这样便没有捕获它。

当 lua 发生了未捕获的异常时，会调用 panic 函数，然后调用 abort() 退出进程。一个补救的方法是在框架的最外层设置一个恢复点：C 语言用 setjmp ，C++ 用 try catch 。在 `lua_atpanic`

设置的 panic 方法中，直接跳转到恢复点（ C 语言用 longjmp ，C++ 用 throw ）让 panic 函数永不返回。但这并非推荐的手法，按 Lua 作者 Roberto 的说法，“The panic mode is only for ill-structured Lua programs.”。

当你只用 C 编写 Lua 的库时，即用一个现成的，考虑完备的宿主程序（比如 Lua 官方的解释器)时，这个问题通常不必考虑。因为你调用 Lua C API 的 C 代码块都是直接或间接被 Lua 调用的。但把 Lua C API 遍布在宿主程序中时却很容易忽视。完善的做法是，你应该把你的业务逻辑写到一个 `lua_CFunction`

中，然后用 `lua_pcall`

去调用它。而这个代码块的参数则应该用 void * 通过 `lua_pushlightuserdata`

来传递。

这就是为什么，之前版本的 Lua 都提供了一个叫 `lua_cpcall`

的 C API 的缘故。而在 Lua 5.2 支持了 light c function 后，对于无 upvalue 的 C function 都可以无额外成本的通过 `lua_pushcfunction`

传入 lua vm ，所以就不再需要一个单独的 `lua_cpcall`

了。

最好的范例是 [Lua 官方的解释器](http://www.lua.org/source/5.3/lua.c.html) 的实现：你现在应该明白，为何主逻辑被写在一个叫 pmain 的函数中，而不是直接在 main 里实现了吧。

前面提到 `lua_pushlightuserdata`

不会抛出异常，同样的其它简单值类型，`lua_pushboolean`

`lua_pushinteger`

等都不会。这是因为这些 api 是不检查 lua 的堆栈容量的，也不会主动按需扩展 Lua 栈。不过 `lua_pushstring`

这种需要构造新对象的 API 则可能引发 OOM （out of memory）异常，需要留意。lua 只保证在从 Lua 进入 C 的边界上提供额外的 `LUA_MINSTACK`

个 slot 。这个值默认为 20 ，一般是够用的。正因为一般够用，反而容易被编写 C 扩展的同学忽视。尤其是在 C 扩展的代码里有 C 层次上的递归时，非常容易在边界情况下栈溢出。因为 Lua 的 stack 实际上又经常留出超过 `LUA_MINSTACK`

的空间，这种 bug 不易察觉。记住：如果你在 C 扩展中做复杂的事情，一定要记得在使用 lua stack 前，用 `luaL_checkstack`

留够你需要的空间。


在用 C 编写 Lua 的 C 扩展库时，由于 C API 有抛出异常的可能，你还需要考虑，每次当你调用 Lua API 时，下一行程序都有可能运行不到。所以一旦你想临时申请一些堆内存使用，要充分考虑你在同一函数内编写的释放临时对象的代码很可能运行不到。正确的方法是使用 `lua_newuserdata`

来申请临时内存，如果被异常打断，后续的 gc 流程会清理它们。`luaL_Buffer`

相关的库就是基于这个做的。或者你自己有办法通过池回收也可以，总之需要考虑这点。

基于同样的理由，如果你构造了一个 C 对象，那么在调用其它 Lua C API 之前，应该把对象中的所有字段都清零（设置成合法的初始值），避免通过 Lua C API 一个个字段设置。比如：

struct foobar {
const char *a;
const char *b;
}
...
struct foobar * f = lua_newuserdata(L, sizeof(*f));
... // 一些其它工作
f->a = lua_tostring(L, 1);
f->b = lua_tostring(L, 2);

这样写就是有风险的。因为，第一次调用 `lua_tostring`

时有可能因为异常而执行不到下一行，导致 f->b 没有被初始化。正确的做法是：

struct foobar * f = lua_newuserdata(L, sizeof(*f));
f->a = NULL;
f->b = NULL;
... // 一些其它工作
f->a = lua_tostring(L, 1);
f->b = lua_tostring(L, 2);

如果你仔细阅读过 lua 的源代码，会发现 Lua 内部实现中也经常用这种惯例写法。这里使用 newuserdata 可以回避大多数初始化失败的问题，但你要确信在 c 对象正确初始化之后才能给将 f 或对应的 lua 对象传递到别处，以及给 userdata 增加 metatable 。


当宿主语言本身支持异常时，让宿主语言的异常机制和 Lua 自身的异常机制协同工作是一个难题。想不侵入 Lua 自身的实现而靠库自身协调两种异常机制是几乎不可能的。为了解决这个问题，Lua 允许你在构建库的时候定义一系列的宏来用宿主语言的异常机制来实现 Lua 的异常传播。

看 [ldo.c](http://www.lua.org/source/5.3/ldo.c.html) 前面的 `LUAI_THROW`

`LUAI_TRY`

等宏就是做的这个事情。所以，如果你用 C++ 做宿主语言，就应该用 C++ 编译器编译 Lua 库。如果你直接用 C 编译出来的库，链接到 C++ 程序中（或共用已编译好的 lua 动态库），那么表面上工作会一切正常。可一旦涉及异常处理，就会有很多未知的问题。

这个问题是这样造成的：

Lua 在内部发生异常时，VM 会在 C 的 stack frame 上直接跳至之前设置的恢复点，然后 unwind lua vm 层次上的 lua stack 。lua stack （CallInfo 结构）在捕获异常后是正确的，但 C 的 stack frame 的处理未必如你的宿主程序所愿。也就是 RAII 机制很可能没有被触发。

btw ，Lua 的 stack frame 并不一一对应 C 的 stack frame ，即并不是一次 Lua 层的函数调用就对应一层 C 函数调用，当你在 Lua 层上 pcall 一个 lua 函数中再 pcall 一个 lua 函数，也不是直觉上的做两层 try catch 。Lua 的这种实现和 Lua 的语言特性，尾递归以及 coroutine 有关。如果想在 pcall 的内部 coroutine.yield 回 C 层，就绝对不能让 Lua 的函数调用对应到 C 函数调用上，否则 coroutine 就无法 resume （因为在 C 层上跳回恢复点，就破坏了 C 层的 stack frame ，无法重建）。这也是为什么不能简单的让 Lua 内部实现的异常机制简单兼容宿主语言的缘故。

换句话说，即使你用 try catch 重新编译了 lua 库。当你在 `lua_pushstring`

这种可能抛出异常的 lua api 外主动 try catch ，这个异常你可以捕获到（因为指定 lua vm 的实现也使用它），但却会破坏 lua vm 本身的工作。

强调：你不能用 throw 代替 `lua_error`

来抛出异常，也不能用 try catch 来取代 `lua_pcall`

。在 Lua VM 实现层面换成 C++ 的异常机制，并不等于 lua 和 C++ 拥有了等价的异常传播系统。当你明白有些 lua api 会抛出异常，并且这个异常是以 C++ 的 throw 抛出的；你同时也应该明白，自行用 C++ 的异常捕获机制来包起这些 lua api 的调用，试图捕获异常是错误的做法。

在 C++ 中嵌入 Lua 后，让 C++ 编写的扩展库正确运作的问题很好解决（单独构建一个 C++ 版的库即可），但当你在多种语言中交互，以 C/C++ 中媒介时，这个问题就复杂的多。比如说，近年来流行用 Unity3D 开发游戏，并在 mono 虚拟机中嵌入 Lua 来编写游戏逻辑，就涉及 lua mono C 三者之间的沟通。mono 本身也有自身的虚拟机，恐怕你很难将 lua 自身实现中用到的 `LUAI_THROW`

`LUAI_TRY`

替换为 mono 的异常实现。所以，当你用 C# 编写代码转换为 Lua 可以调用的函数时，应该避免 C# 的异常漏到 Lua 的 VM 中。反过来，lua 异常也一定要在 lua 层面或 C 层面截获住。这些要实现的非常小心，所以不建议直接把 lua C api 一一映射成 C# 函数，用 C# 来直接操作 lua state ，那样是很难写的完备的。

考虑到 mono 本身就是 C 实现的，Lua API 的异常传播在大部分情况下都可以在 mono vm 里正常工作（如果你把 mono 也看成是 C 编写的模块的话），但当异常发生时（Lua 程序和 C 程序不一样，很多情况下依赖异常传播），即使在 Lua 层捕获，只要中间穿越了 C# 代码，那么一些副作用却是很难察觉的。这是因为 lua 的 VM 实现是直接用 longjmp 做 C 的 stack frame unwind 的，mono vm 并不能感知。危险正在于 99% 的情况下都工作正常，偶尔不正常却很难发觉。

如果完全用 C# 来重新实现一遍 Lua 可以完备的解决这个问题，[UniLua](https://github.com/xebecnan/UniLua) 就是这样一个项目。这样做的缺点是性能堪忧。毕竟同样的事情，C# 比原生代码要慢的多。

如果你在意性能，那么还是可以把 Lua 编译成原生库，然后导出接口给 C# 使用的，这样的项目也很多，就不一一列举了。但使用时应该注意，应该避免在低层次去操作 `Lua_State`

，而应该封装出简单的几个高层接口。直接让 C# 代码去读写 Lua State 中的数据结构就是不可取的。几乎所有的对 Lua State 的 C API 都有异常处理的问题。简单封装这些 C API 成 C# 函数，要么考虑不完备要么效率低下（在过低层次上编码造成的问题）。

让我们把 Lua VM 和 mono VM 交互看成是两个黑盒间的交互，其实这和不同进程，不同机器，不同服务间的交互本质上并没有什么区别。问题是不是变得熟悉起来？其实就是相互发送消息的过程。我们要做的仅仅是讲消息编码，消息传递，让对方处理。不要过于考虑消息传递过程中的性能开销，承认一定的开销，可以提供更大的弹性，和设计接口上的简洁。真正要考虑的其实是怎么尽量减少交互的频率。

其实我们要做的仅仅是把 C# 函数按统一的规格注册到 Lua VM 中供其调用（甚至只有一个单一接口让 Lua 发送消息出来），给 C# 提供一个方法可以调用 Lua 中的函数（或是向 Lua 发送消息，由 Lua 侧将消息转换为函数调用）就可以了。考虑到这个过程其实是在同一进程（甚至同一线程）中进行的。消息的编码不一定是一个连续的字符串，只要是双方都可以编码解码的内存地址即可。

因为写这篇 blog 正是我们自己的项目遇到了此类需求，所以我在写文字的同时也为公司的同事编写了一组示范代码。[代码在 github 上](https://github.com/cloudwu/luabind) 。它只完成了基本的功能，并只是一个 C 库，但通过一些简单的封装就可以包装成 C# 模块在 unity3d 的 mono 环境中使用。


ps. 本文提到的问题并不仅仅出现在 lua 的初学者，一些用户众多的将 lua api binding 到C 之外语言的库在实现的时候都或多或少的有这里谈及的问题。

以 C++ 用户使用较多的 [luabind](https://github.com/luabind/luabind) 为例，它所提供的 "Lua functions in C++" 特性就是不完备的。只是这个 C++ 库实现的极其繁杂，看出并了解其中的问题（设计的局限性）很不容易，而隐患又不容易出现，对使用者来说是个很大的威胁。（当然你非常清楚问题后，是可以从使用上规避容易出问题的用法的）

具体是这样：想让一个 lua 函数从 C++ 中被调用。luabind 提供了一个叫做 `call_function`

的方法，用起来倒是简单，[参看其文档](http://www.rasterbar.com/products/luabind/docs.html) 的 7.3 节。

一般说来，我们会从 host 程序中直接调用它，也就是调用 lua 函数并不在 lua 保护模式中。luabind 的实现考虑了这一点，所以 `call_function`

只会用 `lua_pcall`

而不会使用可能产生异常的 `lua_call`

。

问题出在获得函数对象，处理参数，以及将返回值转换为 C++ 对象上面。

抽丝剥茧理解其实现非常困难，所以我们只看其中明显问题：

`call_function`

的主体实现在 [luabind/detail/call_function](https://github.com/luabind/luabind/blob/master/luabind/detail/call_function.hpp) 中。

如果你提供了一个字符串去定位全局函数， 在 445 行可以看到：

lua_pushstring(L, name);
lua_gettable(L, LUA_GLOBALSINDEX);
return proxy_type(L, 1, &detail::pcall, args);

这里的 `lua_pushstring`

和 `lua_gettable`

都是有可能抛出异常的，但没有在 pcall 的保护中（pcall 是在后面触发的）。

当然，如果你不考虑 oom 错误，也不考虑全局表有可能被人重载了 index 元方法而可能出错。那么这看起来还是个小问题。

ps. 在 pcall 前将参数压入 lua stack 可能引发的 OOM 属于同类问题，也暂时不考虑。

再来看一个更为严重的：

`call_function`

的返回值是等到 pcall 返回了以后，由 template 指定的 Ret 类来转换为 C++ 对象的。

我们在 [198 行](https://github.com/luabind/luabind/blob/master/luabind/detail/call_function.hpp#L198-L215) 可以看到这个过程，是在调用 `m_fun`

也就是 pcall 之后的。即，从 lua 值到 C++ 对象的转换并没有被 pcall 保护起来。

为什么说这个过程隐患很大？因为当你从 lua string 转换为 C++ string 时，其实调用的是 `lua_tostring`

(具体见 [luabind/detail/policy.capp](https://github.com/luabind/luabind/blob/87898f6012d553d7fe783ac1329ca47d45d262a7/luabind/detail/policy.hpp#L748) )

这个 api 除了 oom 异常外，还有很多可能出错。因为 lua 中所有对象都可以附加 tostring 元方法，在转换为 string 时，会执行一段 lua 代码。这在 lua 程序中非常常见。

而正确的封装方法应该是从 C++ 中调用 lua 函数时，参数的传递和返回值的接收和向 host 语言转换都应该包含在一个 `lua_pcall`

下，那个真正的 lua 函数调用使用 `lua_call`

即可。你便可以正确捕获整个过程中 lua 代码里的错误。