---
title: 云风的 BLOG
url: https://blog.codingnow.com/2013/04/
published: '2013-04-17'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

### Lua 5.2.2 中的一处 Bug

前几天, Lua 5.2.2 发布了, 主要是修复了 4 个 Lua 5.2.1 中已知的 bug . 其中包括前段时间一个同学和我在 email 交流中讨论的一个问题.

我把 Lua 5.2.2 更新到公司项目的主干上，同时需要对我的那本 《[Lua 源码欣赏](http://www.codingnow.com/temp/readinglua.pdf)》做一些更新，需要把这次的代码更改同步到书里去。这个工作很繁琐，但有它的价值。比如我发现了 Lua 5.2.2 比 5.2.1 的更改远不只官方宣布了 4 处 bugfix ，还有一些小调整，让 Lua 的源码更规整一些。

阿楠同学因为这段时间一直在维护 [UniLua](https://github.com/xebecnan/UniLua) 这个 C# 版的 Lua 项目，我就随便和他通告了一下这次的一些代码变更，方便他同步到 UniLua 项目中去。

讨论之中，他提到 `luaD_precall`

函数的实现有些诡异之处，没有看明白。我顺着他指出的位置又仔细阅读了一下，果然发现这里存在一个隐藏很深的 Bug 。

准确说，这不是 Lua 5.2 引入的新 Bug ， 至少在 Lua 5.1 年代就存在了。只不过很难触碰到触发条件。

理解了代码后，我构造了一小段 Lua 代码，可以让 Bug 暴露出来。

function f(p1,p2,p3,p4,p5,p6,p7,p8,p9,...) local a1,a2,a3,a4,a5,a6,a7 local a8,a9,a10,a11,a12,a13,a14 end f()

运行这段 Lua 代码会让 Lua 虚拟机崩溃。我的修复 patch 如下：

diff --git a/src/ldo.c b/src/ldo.c index aafa3dc..a901e6c 100644 --- a/src/ldo.c +++ b/src/ldo.c @@ -324,7 +324,7 @@ int luaD_precall (lua_State *L, StkId func, int nresults) { case LUA_TLCL: { /* Lua function: prepare its call */ StkId base; Proto *p = clLvalue(func)->p; - luaD_checkstack(L, p->maxstacksize); + luaD_checkstack(L, p->maxstacksize + p->numparams); func = restorestack(L, funcr); n = cast_int(L->top - func) - 1; /* number of real arguments */ for (; n < p->numparams; n++)

已经提交到 lua mailling list 里去了。Bug 的成因是：在 Lua 函数执行时，先按编译时统计出来的需要的寄存器个数扩展了堆栈。但是，如果函数有不定个数的参数，且调用者没有给完固定参数个数，会触发一个边界条件复制传入参数，结果是让预留的栈空间有可能不够。

4 月 18 日补充:

由于这是因为内存写越界造成的 bug , 所以是否会立即导致程序崩溃和编译环境有关.

我使用的是 mingw32 ，且打开了 -g 选项。

如果想确保看到问题，可以在 luaconf.h 里加上

#include "assert.h" #define lua_assert assert

这样就会触发定义好的 assert 条件。

4 月 19 日:

这个 bug 终于在 lua mailling list 上被 Roberto 确认了. 英文不好是个问题, 前后写了好几篇才说清楚.

不过这个修复方案还需要斟酌. 因为可以有更好的方法去掉那次加法带来的额外开销.

"we can avoid this little overhead in the common case (non-vararg functions). We can either add p->numparams in the parser (so that the final maxstacksize of vararg functions already reflect this extra need) or check for numparams inside adjust_varargs, only for vararg functions. "