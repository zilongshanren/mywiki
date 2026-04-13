---
title: 云风的 BLOG
url: https://blog.codingnow.com/2021/06/
published: '2021-06-11'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

最近在尝试做一个类似异星工厂的游戏原型。由于最终希望在内存有限的手机上运行，所以不得不考虑内存如何有效利用的问题。

这是因为，我在玩异星工厂（加上一些 mod ）时，发现 PC 内存能占到 10G 以上，且这些内存大部分都不是图像资源，是实打实的逻辑数据。我稍微估算了一下，在一些内容丰富的 mod 中，游戏内的对象能够达到数十万，甚至上百万之多。用传统方法使用的内存势必以 G 计算。

如果希望同样的逻辑跑在手机上，我希望把逻辑数据控制在 500M 之下。除了从游戏玩法做做一些限制外，还需要对逻辑占用的内存精打细算。

在 C 中实现一个 ECS 模型是一个不错的选择。

每个 Entity 仅包括必须持久保存的数据。很多数据都只在同一个 tick 计算中间使用，并不需要一直保存在对象中。

例如：每个机器的实时功率，就是可以通过当前 tick 的上下文状态计算出来的。功率这个数值只在电网计算的环节（一个特定 system ）被计算出来，当机器工作阶段后，在做信号模块和物流模块中就是不必要的。如果按传统的 OO 模式，通常会在对象中增加一个功率属性。这就永久的占用了内存；而如果用 ECS 模型去处理，所有单位的功率属性就可以聚合在一起，放在一块临时内存中，当到了不再需要这个属性的 system 计算环节，整块临时内存就可以挪作它用。

在 ECS 模型中，还是很多节省内存的技巧。比如，我们可以完全避免指针（在 64 位系统下会占 8 个字节）的使用，改用计算好的 id （通常不会超过 4 个字节，甚至 2 或 3 字节就够）做相互引用。由于 ECS 模型中，每个 System 都针对特定有限的组件整体做处理，很多在传统 OO 中，为了加速相互访问用的引用也是不必要的。我们可以把引用降到最少。

理论上来说，我们可以设计出一个完全没有冗余的数据结构。当 A B 数据相互关联时，若在 A 中引用 B ，就不必在 B 中引用回 A 。因为，你总可以在遍历处理 A 的集合时临时建立起引用关系，任务结束后就可以清除它们之间的关联。这在传统 OO 模型中通常难以做到，因为 OO 模型中，业务处理是针对对象本身的，如果你需要在处理 A 对象的时候用 O(1) 的复杂度找到 B ，最简单的方法就是在 A 的内部保留一个 B 的指针；同时，如果处理 B 的时候还需要找回 A ，那就还需要在 B 中保存 A 的指针。这个 A 和 B 的关联数据就在内存中出现了两次。这会多消耗内存，且让同样的数据在内存中重复，这通常还是 bug 的滋生之所。

这篇 Blog 我暂时不想展开这个问题。只写写我最近遇到了一个类似的实作问题：

当 A 和 B 分处 C 内存和 Lua 内存时，引用将更加难建立，索引成本也会更高。我最近找到一个方法解决这个问题。

具体问题是这样的：

我在编写电网模块时，电力设备的基础数据是紧凑的放在 C 内存中的。我给电力设备设计了一个硬上限（例如 10 万个），每个单元是一个固定大小的紧凑 C struct ，所有单元放在一块连续内存中。先用 mmap 预留好足够的地址空间，实际分配时再申请够用的内存页使用。

如果我们有 10 台相同的发电机，并不会把发电机的参数记录 10 次。而是记录了一个 16bit 的 prototype id ，表示这个东西是什么类型的发电机。这样，每个电力设备实际占用的内存是非常小的（只有十几个字节），但在处理他们时需要根据 prototype id 去索引那些机器共享的数据。

在我现在的设计中，所有的 prototype 都是放在 Lua 中的，这样方便配置。如果我们在遍历这数以万计的对象时，每次都通过 prototype id 去 Lua 虚拟机中读取配置，可想而知性能会非常的差。

最容易想到的方法是在 C 中建立一个 prototype 对象的副本，也就是在 C 代码中定义一个同样类型的结构，然后把 Lua 的配置表加载到 C 结构中。我不喜欢这个方案。因为 prototype 是一个很动态的东西，在设计过程中会经常修改。而一个模块可能只聚焦在配置表中很少的几项。另外，为了这个需求再引入一个繁杂的反射模块也不符合我的设计感觉。

我最终采用的方案是实现了一个非常简单的 cache 模块，所有 Lua 到 C 的映射都在一个模块（ System ）运行过程中临时 cache 起来，模块结束就销毁掉 Cache 。Cache 保证了大部分对 Lua 中数据的查询都只做一次，减少 C 到 Lua 的边界。

接口是这样的：

// mersenne prime number
#define CACHE_SIZE 8191
//#define CACHE_SIZE 127
#define PROTOTYPE_INVALID 0xffff
#define PROTOTYPE_MASK 0x8000
#define PROTOTYPE_INT 0
#define PROTOTYPE_FLOAT 1
#define PROTOTYPE_BOOLEAN 2
#define PROTOTYPE_STRING 3
struct prototype_field {
const char *key;
int type;
};
struct prototype_lua {
lua_State *L;
int index;
};
struct prototype_cache {
struct prototype_lua lua;
struct prototype_field *f;
int stride;
void *data; // sizeof data == CACHE_SIZE * stride
type_t p[CACHE_SIZE];
};
void prototype_cacheinit(struct prototype_cache *c);
void* prototype_read(struct prototype_cache *c, type_t prototype);

这个 cache 是一个固定大小的 C 结构，不做任何堆内存分配。所以我们可以轻松的在 C stack 上使用它，不用释放，不必考虑异常结束的问题。它是一个非常简单的 hash 表。我们只缓存 4 类数据：整数、浮点数、布尔量、字符串。它们保存在 Lua 表中，每项都是用字符串 key 索引。我们预留的 slot 有 8191 个，这通常远超同一个模块所需访问的 prototype 总数，cache 建立好后，访问几乎是 O(1) 的。

这个模块的实现也很简单：

#define CACHE_STEP 7
#define CACHE_COLLIDE 8
void
prototype_cacheinit(struct prototype_cache *c) {
int i;
for (i=0;i<CACHE_SIZE;i++) {
c->p[i] = PROTOTYPE_INVALID;
}
int stride = 0;
for (i=0;c->f[i].key;i++) {
switch (c->f[i].type) {
case PROTOTYPE_INT:
stride += sizeof(int);
break;
case PROTOTYPE_FLOAT:
stride += sizeof(float);
break;
case PROTOTYPE_BOOLEAN:
stride += sizeof(int);
break;
case PROTOTYPE_STRING:
stride += sizeof(const char *);
break;
}
}
if (stride != c->stride) {
luaL_error(c->lua.L, "Stride mismatch : %d != %d", stride , c->stride);
}
}
static inline int
inthash(type_t p) {
int h = (2654435761 * p) % CACHE_SIZE;
return h;
}
static inline int
check_field(struct prototype_cache *c, int index, type_t prototype, const char *key, int ltype) {
lua_State *L = c->lua.L;
int t = lua_getfield(L, -1, key);
if (t != ltype) {
if (t == LUA_TNIL) {
c->p[index] = prototype & PROTOTYPE_MASK;
return 1;
}
luaL_error(L, ".%s is not a %s (%s)", key, lua_typename(L, ltype), lua_typename(L, lua_type(L, -1)));
}
return 0;
}
static void *
insert_prototype(struct prototype_cache *c, int index, type_t prototype) {
lua_State *L = c->lua.L;
struct prototype_field *f = c->f;
c->p[index] = prototype;
if (lua_geti(L, c->lua.index, prototype) != LUA_TTABLE) {
luaL_error(L, "Prototype %d not found", prototype);
}
int i;
char *output = (char *)c->data + c->stride * index;
void *ret = (void *)output;
int vd;
float vf;
const char *vs;
for (i=0;f[i].key;i++) {
switch (f[i].type) {
case PROTOTYPE_INT:
if (check_field(c, index, prototype, f[i].key, LUA_TNUMBER))
return NULL;
if (!lua_isinteger(L, -1)) {
luaL_error(L, ".%s is not an integer", f[i].key);
}
vd = lua_tointeger(L, -1);
memcpy(output, &vd, sizeof(int));
output += sizeof(int);
break;
case PROTOTYPE_FLOAT:
if (check_field(c, index, prototype, f[i].key, LUA_TNUMBER))
return NULL;
vf = lua_tonumber(L, -1);
memcpy(output, &vf, sizeof(float));
output += sizeof(float);
break;
case PROTOTYPE_BOOLEAN:
if (check_field(c, index, prototype, f[i].key, LUA_TBOOLEAN))
return NULL;
vd = lua_toboolean(L, -1);
memcpy(output, &vf, sizeof(int));
output += sizeof(int);
break;
case PROTOTYPE_STRING:
if (check_field(c, index, prototype, f[i].key, LUA_TSTRING))
return NULL;
vs = lua_tostring(L, -1);
memcpy(output, &vs, sizeof(const char *));
output += sizeof(const char *);
break;
}
lua_pop(L, 1);
}
return ret;
}
void *
prototype_read(struct prototype_cache *c, type_t prototype) {
assert(prototype != PROTOTYPE_INVALID);
int hash = inthash(prototype);
int h = hash;
int i;
for (i=0;i<CACHE_COLLIDE;i++) {
int cp = c->p[h];
if (cp == prototype) {
char * ptr = (char *)c->data + c->stride * h;
return (void *)ptr;
} else if (cp == (prototype | PROTOTYPE_MASK)) {
return NULL;
} else if (cp == PROTOTYPE_INVALID) {
return insert_prototype(c, h, prototype);
} else {
h += CACHE_STEP;
if (h >= CACHE_SIZE) {
h -= CACHE_SIZE;
}
}
}
// replace prototype in cache
return insert_prototype(c, hash, prototype);
}

它在需要的时候从 Lua 表中读入需要的 key/value 对，缓存在 C 结构中。第二次访问 cache 时避免从 Lua 中再次读取。

当我们计算一个燃烧发电机时，只关心它的功率 power ，热电转换性能 efficiency ，工作优先级 priority 。那么在 C 代码中，可以一开始初始化好这个 cache 。

struct burner_prototype {
float power;
float efficiency;
int priority;
};
static struct prototype_field burner_s[] = {
{ "power", PROTOTYPE_FLOAT },
{ "efficiency", PROTOTYPE_FLOAT },
{ "priority", PROTOTYPE_INT },
{ NULL, 0 },
};
struct prototype_cache burner;
struct burner_prototype buffer[CACHE_SIZE];
burner.f = burner_s;
burner.stride = sizeof(struct burner_prototype);
burner.data = buffer;

在业务处理中，就可以用 `struct burner_prototype *b = prototype_read(&burner, prototype_id);`

读到 prototype_id 对象中的三条属性了。