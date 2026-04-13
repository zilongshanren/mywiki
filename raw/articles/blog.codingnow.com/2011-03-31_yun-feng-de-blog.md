---
title: 云风的 BLOG
url: https://blog.codingnow.com/2011/03/
published: '2011-03-31'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

早期的 Lua GC 采用的是 stop the world 的实现。一旦发生 gc 就需要等待整个 gc 流程走完。如果你用 lua 处理较少量数据，或是数据增删不频繁，这样做不是问题。但当处理的数据量变大时，对于实时性要求较高的应用，比如网络游戏服务器，这个代价则是不可忽略的。lua 本身是个很精简的系统，但不代表处理的数据量也一定很小。

从 Lua 5.1 开始，GC 的实现改为分步的。虽然依旧是 stop the world ，但是，每个步骤都可以分阶段执行。这样，每次停顿的时间较小。随之，这部分的代码也相对复杂了。分步执行最关键的问题是需要解决在 GC 的步骤之间，如果数据关联的状态发生了变化，如果保证 GC 的正确性。GC 的分步执行相对于一次执行完，总的时间开销的差别并不是零代价的。只是在实现上，要尽量让额外增加的代价较小。

先来看 GC 流程的划分。

lua 的 GC 分为五个大的阶段。GC 处于哪个阶段（代码中被称为状态），依据的是 `global_State`

中的 gcstate 域。状态以宏形式定义在 lgc.h 的 14 行。

/*
** Possible states of the Garbage Collector
*/
#define GCSpause 0
#define GCSpropagate 1
#define GCSsweepstring 2
#define GCSsweep 3
#define GCSfinalize 4

状态的值的大小也暗示着它们的执行次序。需要注意的是，GC 的执行过程并非每步骤都拥塞在一个状态上。

GCSpause 阶段是每个 GC 流程的启始步骤。只是标记系统的根节点。见 lgc.c 的 561 行。

switch (g->gcstate) {
case GCSpause: {
markroot(L); /* start a new collection */
return 0;
}

markroot 这个函数所做之事，就是标记主线程对象，标记主线程的全局表、注册表，以及为全局类型注册的元表。标记的具体过程我们后面再讲。

GCSpause 阶段执行完，立刻就将状态切换到了 GCSpropagate 。这是一个标记流程。这个流程会分步完成。当检测到尚有对象待标记时，迭代标记（反复调用 propagatemark）；最终，会有一个标记过程不可被打断，这些操作放在一个叫作 atomic 的函数中执行。见 lgc.c 的 565 行:

case GCSpropagate: {
if (g->gray)
return propagatemark(g);
else { /* no more `gray' objects */
atomic(L); /* finish mark phase */
return 0;
}
}

这里可能需要顺带提一下的是 gray 域。顾名思义，它指 GCObject 中的灰色节点链。何为灰色，即处于白色和黑色之间的状态。关于节点的颜色，马上就会展开分析。

接下来就是清除流程了。

前面我们提到过，string 在 Lua 中是单独管理的，所以也需要单独清除。GCSsweepstring 阶段干的就是这个事情。string table 以 hash 表形式管理所有的 string 。GCSsweepstring 中，每个步骤(step) 清理 hash 表的一列。代码见 lgc.c 的 573 行

case GCSsweepstring: {
lu_mem old = g->totalbytes;
sweepwholelist(L, &g->strt.hash[g->sweepstrgc++]);
if (g->sweepstrgc >= g->strt.size) /* nothing more to sweep? */
g->gcstate = GCSsweep; /* end sweep-string phase */
lua_assert(old >= g->totalbytes);
g->estimate -= old - g->totalbytes;
return GCSWEEPCOST;
}

这里可以看到 estimate 和 totalbytes 两个域，从名字上可以知道，它们分别表示了 lua vm 占用的内存字节数以及实际分配的字节数。

ps. 如果你自己实现过内存管理器，当知道内存管理本身是有额外的内存开销的。如果有必要精确控制内存数量，我个人倾向于结合内存管理器统计准确的内存使用情况。比如你向内存管理器索要 8 字节内存，实际的内存开销很可能是 12 字节，甚至更多。如果想做这方面的修改，让 lua 的 gc 能更真实的反应内存实际使用情况，推荐修改 lmem.c 的 76 行，`luaM_realloc_`

函数。所有的 lua 中的内存使用变化都会通过这个函数。

从上面这段代码中，我们还见到了 GCSWEEPCOST 这个神秘数字。这个数字用于控制 GC 的进度。这超出了今天的话题。留待以后分析。

接下来就是对所有未标记的其它 GCObject 做清理工作了。即 GCSsweep 阶段。它和上面的 GCSsweepstring 类似。

最后是 GCSfinalize 阶段。如果在前面的阶段发现了需要调用 gc 元方法的 userdata 对象，将在这个阶段逐个调用。做这件事情的函数是 GCTM 。

前面已经谈到过，所有拥有 gc 元方法的 userdata 对象以及其关联的数据，实际上都不会在之前的清除阶段被清除。（由于单独做过标记）所有的元方法调用都是安全的。而它们的实际清除，则需等到下一次 GC 流程了。或是在 `lua_close`

被调用时清除。

ps. `lua_close`

并不做完整的 gc 工作，只是简单的处理所有 userdata 的 gc 元方法，以及释放所有用到的内存。它是相对廉价的。


接下来我们看看 GC 标记流程涉及的一些概念。

简单的说，lua 认为每个 GCObject （需要被 GC 收集器管理的对象）都有一个颜色。一开始，所有节点都是白色的。新创建出来的节点也被默认设置为白色。

在标记阶段，可见的节点，逐个被设置为黑色。有些节点比较复杂，它会关联别的节点。在没有处理完所有关联节点前，lua 认为它是灰色的。

节点的颜色被储存在 GCObject 的 CommonHeader 里，放在 marked 域中。为了节约内存，是以位形式存放。marked 是一个单字节量。总共可以储存 8 个标记。而 lua 5.1.4 用到了 7 个标记位。在 lgc.h 的 41 行，有其解释：

/*
** Layout for bit use in `marked' field:
** bit 0 - object is white (type 0)
** bit 1 - object is white (type 1)
** bit 2 - object is black
** bit 3 - for userdata: has been finalized
** bit 3 - for tables: has weak keys
** bit 4 - for tables: has weak values
** bit 5 - object is fixed (should not be collected)
** bit 6 - object is "super" fixed (only the main thread)
*/
#define WHITE0BIT 0
#define WHITE1BIT 1
#define BLACKBIT 2
#define FINALIZEDBIT 3
#define KEYWEAKBIT 3
#define VALUEWEAKBIT 4
#define FIXEDBIT 5
#define SFIXEDBIT 6
#define WHITEBITS bit2mask(WHITE0BIT, WHITE1BIT)

lua 定义了一组宏来操作这些标记位，代码就不再列出。只需要打开 lgc.h 就能很轻松的理解这些宏的函数。

白色和黑色是分别标记的。当一个对象非白非黑时，就认为它是灰色的。

为什么有两个白色标记位？这是 lua 采用的一个小技巧。在 GC 的标记流程结束，但清理流程尚未作完前。一旦对象间的关系发生变化，比如新增加了一个对象。这些对象的生命期是不可预料的。最安全的方法是把它们标记为不可清除。但我们又不能直接把对象设置为黑色。因为清理过程结束，需要把所有对象设置回白色，方便下次清理。lua 实际上是单遍扫描，处理完一个节点就重置一个节点的颜色的。简单的把新创建出来的对象设置为黑，有可能导致它在 GC 流程结束后，再也没机会变回白色了。

简单的方法就是设置从第三种状态。也就是第 2 种白色。

在 Lua 中，两个白色状态是一个乒乓开关，当前需要删除 0 型白色节点时， 1 型白色节点就是被保护起来的；反之也一样。

当前的白色是 0 型还是 1 型，见 `global_State`

的 currentwhite 域。otherwhite() 用于乒乓切换。获得当前白色状态，使用定义在 lgcc.h 77 行的宏：

#define luaC_white(g) cast(lu_byte, (g)->currentwhite & WHITEBITS)

FINALIZEDBIT 用于标记 userdata 。当 userdata 确认不被引用，则设置上这个标记。它不同于颜色标记。因为 userdata 由于 gc 元方法的存在，释放所占内存是需要延迟到 gc 元方法调用之后的。这个标记可以保证元方法不会被反复调用。

KEYWEAKBIT 和 VALUEWEAKBIT 用于标记 table 的 weak 属性，无需多言。

FIXEDBIT 可以保证一个 GCObject 不会在 GC 流程中被清除。为什么要有这种状态？关键在于 lua 本身会用到一个字符串，它们有可能不被任何地方引用，但在每次接触到这个字符串时，又不希望反复生成。那么，这些字符串就会被保护起来，设置上 FIXEDBIT 。

在 lstring.h 的 24 行定义有：

#define luaS_fix(s) l_setbit((s)->tsv.marked, FIXEDBIT)

可以把一个字符串设置为被保护的。

典型的应用场合见 llex.c 的 64 行：

void luaX_init (lua_State *L) {
int i;
for (i=0; itsv.reserved = cast_byte(i+1); /* reserved word */
}
}

以及 ltm.c 的 30 行：

void luaT_init (lua_State *L) {
static const char *const luaT_eventname[] = { /* ORDER TM */
"__index", "__newindex",
"__gc", "__mode", "__eq",
"__add", "__sub", "__mul", "__div", "__mod",
"__pow", "__unm", "__len", "__lt", "__le",
"__concat", "__call"
};
int i;
for (i=0; itmname[i] = luaS_new(L, luaT_eventname[i]);
luaS_fix(G(L)->tmname[i]); /* never collect these names */
}
}

以元方法为例，如果我们利用 lua 标准 api 来模拟 metatable 的行为，就不可能写的和原生的 meta 机制高效。因为，当我们取到一个 table 的 key ，想知道它是不是 `__index`

时，要么我们需要调用 strcmp 做比较；要么使用 `lua_pushlstring`

先将需要比较的 string 压入 `lua_State`

，然后再比较。

我们知道 lua 中值一致的 string 共享了一个 string 对象，即 TString 地址是一致的。比较两个 lua string 的代价非常小（只需要比较一个指针），比 C 函数 strcmp 高效。但 `lua_pushlstring`

却有额外开销。它需要去计算 hash 值，查询 hash 表 (string table) 。

lua 的 GC 算法并不做内存整理，它不会在内存中迁移数据。实际上，如果你能肯定一个 string 不会被清除，那么它的内存地址也是不变的，这样就带来的优化空间。ltm.c 中就是这样做的。

见 lstate.c 的 93 行：

TString *tmname[TM_N]; /* array with tag-method names */

`global_State`

中 tmname 域就直接以 TString 指针的方式记录了所有元方法的名字。换作标准的 lua api 来做的话，通常我们需要把这些 string 放到注册表，或环境表中，才能保证其不被 gc 清除，且可以在比较时拿到。lua 自己的实现则利用 FIXEDBIT 做了一步优化。

最后，我们来看看 SFIXEDBIT 。其实它的用途只有一个，就是标记主 mainthread 。也就是一切的起点。我们调用 `lua_newstate`

返回的那个结构。

为什么需要把这个结构特殊对待？因为即使到 `lua_close`

的那一刻，这个结构也是不能随意清除的。我们来看看世界末日时，程序都执行了什么？见 lstate.c 的 105 行。

static void close_state (lua_State *L) {
global_State *g = G(L);
luaF_close(L, L->stack); /* close all upvalues for this thread */
luaC_freeall(L); /* collect all objects */
lua_assert(g->rootgc == obj2gco(L));
lua_assert(g->strt.nuse == 0);
luaM_freearray(L, G(L)->strt.hash, G(L)->strt.size, TString *);
luaZ_freebuffer(L, &g->buff);
freestack(L, L);
lua_assert(g->totalbytes == sizeof(LG));
(*g->frealloc)(g->ud, fromstate(L), state_size(LG), 0);
}

这是 `lua_close`

的最后一个步骤。
`luaC_freeall`

将释放所有的 GCObject ，但不包括有 SFIXEDBIT 的 mainthread 对象 。见 lgc.c 484 行

void luaC_freeall (lua_State *L) {
global_State *g = G(L);
int i;
g->currentwhite = WHITEBITS | bitmask(SFIXEDBIT); /* mask to collect all elements */
sweepwholelist(L, &g->rootgc);
for (i = 0; i < g->strt.size; i++) /* free all string lists */
sweepwholelist(L, &g->strt.hash[i]);
}

这里 FIXEDBIT 是被无视的，而在此之前，FIXEDBIT 被保护着。见 lstate.c 的 153 行（`lua_newstate`

函数）：

g->currentwhite = bit2mask(WHITE0BIT, FIXEDBIT);

这么做很容易理解，lua 世界的起源，一切根数据都放在这个对象中，如果被提前清理，后面的代码就会出问题。真正释放这个对象不是在 GC 中，而是最后那句：

lua_assert(g->totalbytes == sizeof(LG));
(*g->frealloc)(g->ud, fromstate(L), state_size(LG), 0);

顺带还 assert 了一下，最终，世界上是不是只剩下这个结构。


写累了，待续。