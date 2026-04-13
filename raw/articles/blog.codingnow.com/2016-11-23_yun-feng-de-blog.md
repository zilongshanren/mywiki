---
title: 云风的 BLOG
url: https://blog.codingnow.com/2016/11/
published: '2016-11-23'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

### 如何让 lua 做尽量正确的热更新

很多项目采用 lua 的一大原因是 lua 可以方便的做热更新。

你可以在不中断进程运行的情况下，把修改过的代码塞到进程中，让随后的过程运行新版本的代码。这得益于 lua 的 function 是 first class 对象，换掉代码不过是在让相应的变量指向新的 function 对象而已。

但也正因为 lua 的这种灵活性，想把热更新代码这件事做的通用，且 100% 做对，又几乎是不太可能的。

首先，你很难准确的定义出，什么叫做更新，哪些数据需要保留，哪些需要替换成新版本。光从源代码和运行时的元信息上去分析是远远不够的。

lua 只有一种通用数据结构 table ，这方便了我们做数据更新；但同时也制造了一些模糊性难题。比如，如果在代码中有一些常量配置数据表，写死在源代码中，通常你是希望跟着新版本一起更新的；而有一些表，记录着运行时的状态，你又不希望在代码更新后状态清空。

所以一般做热更新方案的时候，都会人为加一些约束，在遵循约束条件的前提上，尽量让更新符合预期。

最近在给公司的项目做一些技术指导，同时也做一些工具来提高开发效率。对于开发期（而不是生产环境），或许提供一个更灵活的热更新方案更方便一些。我们不太需要结果 100% 正确，但是需要减少一些约束。

在开发期，最好就是改两行代码，能立刻让进程刷新成新版本的代码，并不中断运行。如果更新结果和预期不符，最坏的后果也不过是关掉程序重新来而已。但是如果仅仅是改两行代码，或加几行 log ，则基本不会出错，但开发效率却可以极大的提高。

下面来讨论一下，在约束条件足够少的情况下，如何设计一个尽量完备的热更新方案。

热更新的关键是：找到更新的代码模块和在内存中运行的对应模块，到底有什么差异，以及如何处理这些差异。

如果我们以模块为单位来更新，第一步就是要把要处理的数据约束在一个足够小的范畴，而不能扩大到整个虚拟机。

所以我先实现了一个沙盒，让 require 新模块的过程在沙盒中运行。我们只给沙盒注入有限的几个不会产生副作用的函数，比如 print ，require，pairs 等；只允许在模块初始化流程中调用这些无副作用的函数。那么，当模块初始化好之后，整个模块内部的数据（函数也是数据），都不会溢出沙盒（不会有引用指向沙盒外）。

由于 lua 的数据结构很简单，所以我们可以认为沙盒中放着一张只有 function 和 table 两种复杂数据类型构成的图。这是因为 coroutine.* setmetatable io.* 等这些可能产生其它类型数据的函数都不能在初始化阶段调用，这是一个合理的限制条件。

这个限制条件同样也能规范模块的开发方法。比如若有复杂的初始化流程必须提供一个模块的初始化函数，由外部驱动，而不能直接写在模块的加载流程中，这也回避了更新模块代码时的重复初始化过程。

在制作沙盒时，可以建立一个访问全局变量和其它模块内容的 dummy 方法。一些 lua 常用写法就可以支持，比如：

local debug = require "debug" local tinsert = table.insert local getinfo = debug.getinfo

这类常见的写法是可以支持的，只不过这些 local 变量在沙盒中运行时，指向的是一个 dummy 对象；当更新模块成功后，可以后续替换成真正的变量。但是，在模块初始化过程调用它们会失败。

第二步，我们可以分析沙盒中的数据图。为了简化实现，我们要求数据图的初始状态 key 都必须是 string 或 number 等值类型。这应该也算一个合理的要求。虽然 key 是 table 或 function 也能实现，但代码会复杂很多，不值得放宽这个限制。

接下来，沙盒中每个 table 和 function 都可以表达为一个简单值类型序列索引到的东西。

我们可以根据每条路径去对比内存中同样路径上的对象，找到它的老版本。对于 function 变成 table 或 table 变成 function 这种情况，通通认为是有二义性的，可以简单拒绝热更新。我们的原则是，在约束条件下尽量不出错，如果做就做对。

这样，问题就变简单了：找到了对象之间的新老版本对后，就是怎么替换的问题。如果新版本中有对象不存在，那么不用删除老版本，因为如果老版本无人使用，那么就随它去好了；如果新版本对老版本有新增，直接加入新对象。

对于同类对象替换：函数当然是用新版本替换老版本，但是要小心的处理 upvalue ，这个下面展开说；对于 table ，我的建议是直接把新版本的 k/v 插入老版本的 table ，取并集。这种合并 table 的规则最为简单。

upvalue 如何合并呢？

upvalue 其实是 lua 中的一个隐式类型，大致相当于 C++ 的引用类。比如：

local a = {} function foo() return a end

a 是 foo 的一个 upvalue ，在 lua 中 a 的类型是 table ，但 upvalue 的实际类型却不是。因为你可以在别处修改 a ，foo 返回值也会跟着改变。

lua 提供了两个 api ：debug.upvalueid 和 debug.upvaluejoin 来操作 upvalue 。

我建议的规则是，当我们需要把 f1 替换成 f2 时，应该取出 f2 的所有 upvalue ，按名字 join 给 f1 。不过这里存在的问题是， f1 如果新增了 upvalue 该怎么办？。

我们不能简单的保留 f1 新增的 upvalue ，比如：

--老版本 local a,b function foo() return a end function foo2() return b end -- 新版本 local a,b function foo() return a,b end function foo2() return b end

这里老版 foo 只有一个 upvalue a ，但新版 foo 有两个 a 和 b 。我们在处理 foo 更新的时候，可以把老版的 a 关联给新版的 foo ；但在老版的 foo 中，却无法找到 b 。

如果我们不理会新增的 b 让其保留在 foo 上，那么接下来就会出现 foo2 的 b 被关联走；结果在新版本中， foo 和 foo2 原本共享的 b 变成了两个。

所以正确的做法是，把一个模块中所有的函数对象一起处理，所有处理过的 upvalue 以upvalueid 为索引记录在一起，这样在推导 upvalue 的归属时，可以保持同一版本中的关联性。

如果推导产生了歧义，例如新版本中两个函数共享一个 upvalue ，而老版中是分离的，那么都认为代码有二义性，拒绝更新。

再考虑这种情况：

local mod = {} local pool = {} function mod.foo() return function() return pool end end

这里，mod.foo() 返回一个函数，引用了 pool 。这点，在初始化 mod 的时候，该函数是不存在的，所以无法被分析到。所以在合并对象，处理 upvalue 的时候，必须将新版 upvalue 的值合并到老版 upvalue 中，再将新版 function 的 upvalue join 到老版的 upvalue ；不可以反过来做。

注意：这里返回的那个匿名函数 function() return pool end ，如果一旦被持有，旧版本是无法被更新成新版本的。

由于我们可以先在沙盒中尽量把有效性检查全部做完，所以不会出现更新了一半的状态出错，让内存中的状态处于中间状态的情况。

最后，我们只需要遍历整个 VM ，把所有引用老版本函数的地方，修改为新版本对应函数。整个工作就完成了。

说起来容易，做起来还是很麻烦的。我花了两天的时间才把实现基本完成。[放在 github 上](https://github.com/cloudwu/luareload/)。

目前还没有仔细测试，有时间我会再 review 一遍。正如文章前面所说，在我们的应用场合（用于开发期调试），正确性暂时没有太高的要求，所以可以先将就着用用吧。 :) 如果你想在你的项目利用它做更多的事情，欢迎使用，但请留意可能出现的 bug 。欢迎修正 bug 后提交一个 pull request 。

11 月 25 日补：

关于前面提到的限制，如果旧有模块中有函数返回了一个函数，这个返回的函数虽然属于这个模块，但是却是无法更新的。只能做到，新的版本再调用函数生成它时，新的版本被更新，已有的的函数则只能保持原样。

这个限制的根源在于，重新加载的模块新版本，在加载完成后，对应的函数并不存在。因为对于 lua ，function 是 first class 的。过去的运行中，可能已构建了很多这样的函数对象，每个都是不同的（如果 upvalue 不同），而如果更换成新版本的函数，必须通过调用已有的函数才能构建出来，而且每调用一次才能生成一个新对象。

如果想解决这个问题，需要给 lua 增加一种能力：可以根据一个函数的 prototype 来直接构建出 function 对象。

prototype 是 lua 内部的一种数据类型，可以简单理解成一个函数去掉 upvalue 后的部分。当你写：

function foo(a) return function() return a end end

时，每次对 foo(a) 的调用都会生成一个不同的匿名函数对象，它们引用的 a 都是不同的（每个分别指向不同的 a ）。但是这些不同的匿名函数对象拥有相同的 prototype 对象。

如果使用 lua 的内部 c api 可以实现这样一组 api ，根据一个函数的 prototype 来构建新的函数，构建的函数的 upvalue 全部为 nil ，但你可以再使用 debug.upvaluejoin 来连接到正确的 upvalue 上。

#include#include #include #include #include static int lclone(lua_State *L) { if (!lua_isfunction(L, 1) || lua_iscfunction(L,1)) return luaL_error(L, "Need lua function"); const LClosure *c = lua_topointer(L,1); int n = luaL_optinteger(L, 2, 0); if (n < 0 || n > c->p->sizep) return 0; luaL_checkstack(L, 1, NULL); Proto *p; if (n==0) { p = c->p; } else { p = c->p->p[n-1]; } lua_lock(L); LClosure *cl = luaF_newLclosure(L, p->sizeupvalues); luaF_initupvals(L, cl); cl->p = p; setclLvalue(L, L->top++, cl); lua_unlock(L); return 1; } static int lproto(lua_State *L) { if (!lua_isfunction(L, 1) || lua_iscfunction(L,1)) return 0; const LClosure *c = lua_topointer(L,1); lua_pushlightuserdata(L, c->p); lua_pushinteger(L, c->p->sizep); return 2; } int luaopen_clonefunc(lua_State *L) { luaL_checkversion(L); luaL_Reg l[] = { { "clone", lclone }, { "proto", lproto }, { NULL, NULL }, }; luaL_newlib(L, l); return 1; }

以上，clone 这个 api 可以接收两个参数，第一个必须为一个 lua function ，第二个参数为 0 时，复制自身；为 1~n 时，以内部定义好的 prototype 来构建新的函数副本。

proto 可以返回函数的内部prototype 的指针，和 debug.upvalueid() 类似，它可以帮助你判断两个不同的函数是否有相同的 prototype 。

有了这两个新 api 的帮助，我们就可以完善前面的 reload 库了。我将实现放在里 proto 这个分支上。同时希望这组新的 api 可以进入 lua 下个版本的标准中去。

如果只想更替函数 prototype ，如果我们限制新老模块的 prototype 接口必须完全相同，那么利用我上面提供的 api 可以更简单的实现更新。见 proto 分支上的 hardreload.lua 。