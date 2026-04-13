---
title: 云风的 BLOG
url: https://blog.codingnow.com/2011/04/
published: '2011-04-12'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

GC 中最繁杂的 mark 部分已经谈完了。剩下的东西很简单。今天一次可以写完。

sweep 分两个步骤，一个是清理字符串，另一个是清理其它对象。看代码，lgc.c 573 行：

case GCSsweepstring: {
lu_mem old = g->totalbytes;
sweepwholelist(L, &g->strt.hash[g->sweepstrgc++]);
if (g->sweepstrgc >= g->strt.size) /* nothing more to sweep? */
g->gcstate = GCSsweep; /* end sweep-string phase */
lua_assert(old >= g->totalbytes);
g->estimate -= old - g->totalbytes;
return GCSWEEPCOST;
}
case GCSsweep: {
lu_mem old = g->totalbytes;
g->sweepgc = sweeplist(L, g->sweepgc, GCSWEEPMAX);
if (*g->sweepgc == NULL) { /* nothing more to sweep? */
checkSizes(L);
g->gcstate = GCSfinalize; /* end sweep phase */
}
lua_assert(old >= g->totalbytes);
g->estimate -= old - g->totalbytes;
return GCSWEEPMAX*GCSWEEPCOST;
}

在 GCSsweepstring 中，每步调用 sweepwholelist 清理 strt 这个 hash 表中的一列。理想状态下，所有的 string 都被 hash 散列开没有冲突，这每一列上有一个 string 。我们可以读读 lstring.c 的 68 行：

if (tb->nuse > cast(lu_int32, tb->size) && tb->size <= MAX_INT/2)
luaS_resize(L, tb->size*2); /* too crowded */

当 hash 表中的 string 数量(nuse) 大于 hash 表的列数(size) 时，lua 将 hash 表的列数扩大一倍。就是按一列一个元素来估计的。

值得一提的是，分布执行的 GC ，在这个阶段，string 对象是有可能清理不干净的。当 GCSsweepstring 步骤中，step 间若发生以上 string table 的 hash 表扩容事件，那么 string table 将被 rehash 。一些来不及清理的 string 很有可能被打乱放到已经通过 GCSsweepstring 的表列里。一旦发生这种情况，部分 string 对象则没有机会在当次 GC 流程中被重置为白色。在某些极端情况下，即使你调用 fullgc 一次也不能彻底的清除垃圾。

关于 string 对象，还有个小地方需要了解。lua 是复用相同值的 TString 的，且同值 string 绝对不能有两份。而 GC 的分步执行，可能会导致一些待清理的 TString 又复活。所以在它在创建新的 TString 对象时做了检查，见 lstring.c 86 行：

if (ts->tsv.len == l && (memcmp(str, getstr(ts), l) == 0)) {
/* string may be dead */
if (isdead(G(L), o)) changewhite(o);
return ts;
}

相同的问题也存在于 upvalue 。同样有类似检查。

此处 GCSWEEPCOST 应该是一个经验值。前面我们知道 singlestep 返回的这个步骤大致执行的时间。这样可以让 `luaC_step`

这个 api 每次执行的时间大致相同。mark 阶段是按扫描的字节数确定这个值的。而每次释放一个 string 的时间大致相等（和 string 的长度无关），GCSWEEPCOST 就是释放一个对象的开销了。

GCSsweep 清理的是整个 GCObject 链表。这个链表很长，所以也是分段完成的。记录遍历位置的指针是 sweepgc ，每次遍历 GCSWEEPMAX 个。无论遍历是否清理，开销都是差不太多的。因为对于存活的对象，需要把颜色位重置；需要清理的对象则需要释放内存。每趟 GCSsweep 的开销势必比 GCSsweepstring 大。大致估算时间为 GCSWEEPMAX*GCSWEEPCOST 。

真正的清理工作通过 lgc.c 408 行的 sweeplist 函数进行。

static GCObject **sweeplist (lua_State *L, GCObject **p, lu_mem count) {
GCObject *curr;
global_State *g = G(L);
int deadmask = otherwhite(g);
while ((curr = *p) != NULL && count-- > 0) {
if (curr->gch.tt == LUA_TTHREAD) /* sweep open upvalues of each thread */
sweepwholelist(L, &gco2th(curr)->openupval);
if ((curr->gch.marked ^ WHITEBITS) & deadmask) { /* not dead? */
lua_assert(!isdead(g, curr) || testbit(curr->gch.marked, FIXEDBIT));
makewhite(g, curr); /* make it white (for next cycle) */
p = &curr->gch.next;
}
else { /* must erase `curr' */
lua_assert(isdead(g, curr) || deadmask == bitmask(SFIXEDBIT));
*p = curr->gch.next;
if (curr == g->rootgc) /* is the first element of the list? */
g->rootgc = curr->gch.next; /* adjust first */
freeobj(L, curr);
}
}
return p;
}

后半段比较好理解，当对象存活的时候，调用 makewhite ；死掉则调用 freeobj 。sweeplist 的起点并不是从 rootgc 而是 sweepgc （它们的值可能相同），所以对于头节点，需要做一点调整。

前面的 sweep open upvalues of each thread 需要做一点解释。为什么 upvalues 需要单独清理？这要从 upvalue 的储存说起。

upvalues 并不是放在整个 GCObject 链表中的。而是存在于每个 thread 自己的 L 中（openupval 域）。为何要这样设计？因为和 string table 类似，upvalues 需要唯一性，即引用相同变量的对象只有一个。所以运行时需要对当前 thread 的已有 upvalues 进行遍历。Lua 为了节省内存，并没有为 upvalues 多申请一个指针放置额外的链表。就借用 GCObject 本身的单向链表。所以每个 thread 拥有的 upvalues 就自成一链了。相关代码可以参考 lfunc.c 53 行处的 `luaF_findupval`

函数。

但也不是所有 upvalues 都是这样存放的。closed upvalue 就不再需要存在于 thread 的链表中。在 `luaF_close`

函数中将把它移到其它 GCObject 链中。见 lfunc.c 106 行：

unlinkupval(uv);
setobj(L, &uv->u.value, uv->v);
uv->v = &uv->u.value; /* now current value lives here */
luaC_linkupval(L, uv); /* link upvalue into `gcroot' list */

另，某些 upvalue 天生就是 closed 的。它们可以直接通过 `luaF_newupval`

构造出来。

按道理来说，对 openvalues 的清理会增加单次 **sweeplist 的负荷，当记入 singlestep 的返回值。但这样会导致 sweeplist 接口变复杂，实现的代价也会增加。鉴于 thread 通常不多，GC 开销也只是一个估算值，也就没有特殊处理了。


GC 的最后一个流程为 GCSfinalize 。

它通过 GCTM 函数，每次调用一个需要回收的 userdata 的 gc 元方法。见 lgc.c 的 446 行：

static void GCTM (lua_State *L) {
global_State *g = G(L);
GCObject *o = g->tmudata->gch.next; /* get first element */
Udata *udata = rawgco2u(o);
const TValue *tm;
/* remove udata from `tmudata' */
if (o == g->tmudata) /* last element? */
g->tmudata = NULL;
else
g->tmudata->gch.next = udata->uv.next;
udata->uv.next = g->mainthread->next; /* return it to `root' list */
g->mainthread->next = o;
makewhite(g, o);
tm = fasttm(L, udata->uv.metatable, TM_GC);
if (tm != NULL) {
lu_byte oldah = L->allowhook;
lu_mem oldt = g->GCthreshold;
L->allowhook = 0; /* stop debug hooks during GC tag method */
g->GCthreshold = 2*g->totalbytes; /* avoid GC steps */
setobj2s(L, L->top, tm);
setuvalue(L, L->top+1, udata);
L->top += 2;
luaD_call(L, L->top - 2, 0);
L->allowhook = oldah; /* restore hooks */
g->GCthreshold = oldt; /* restore threshold */
}
}

代码逻辑很清晰。需要留意的是，gc 元方法里应避免再触发 GC 。所以这里采用修改 GCthreshold 为比较较大值来回避。这其实不能完全避免 GC 的重入。甚至用户错误的编写代码也可能主动触发，但通常问题不大。因为最坏情况也只是把 GCthreshold 设置为一个不太正确的值，并不会引起逻辑上的错误。


后记：

终于把这个系列写完了。接下来的工作，我想做一些分析，看能否以最小代价（尽量少用锁）改造出一个多线程版本的 GC 。