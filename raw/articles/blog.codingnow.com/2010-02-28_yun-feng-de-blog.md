---
title: 云风的 BLOG
url: https://blog.codingnow.com/2010/02/
published: '2010-02-28'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

最近想把 engine 做一个简单 C++ 封装，结合 QT 使用。engine 本身是用纯 C 实现的，大部分应用基于 lua 开发。对对象生命期管理也依赖 lua 的 gc 系统。关于这部分的设计，可以参考我以前写的一篇 [为 lua 封装 C 对象的生存期管理问题](http://blog.codingnow.com/2009/03/lua_c_wrapper.html) 。

当我们把中间层搬到 C++ 中时，遇到的问题之一就是，C++ 没有原生的 gc 支持。我也曾经[写过一个 gc 库](http://blog.codingnow.com/2008/06/gc_for_c.html)。但在特定应用下还不够简洁。这几天过年休息，仔细考虑了一下相关的需求，尝试实现了一个更简单的 gc 框架。不到 200 行代码吧，我直接列在这篇 blog 里。

这些尚是一些玩具代码，我花了一天时间来写。有许多考虑不周的地方，以及不完整的功能。但可以阐明一些基本思路。

首先我需要一个标记清除的 gc 系统，用来解决引用记数不容易解决的循环引用问题。它的实现不想比引用记数复杂太多，并有相同甚至更高的性能。

我不想使用复杂的 template 技术，利用太多的语法糖让使用看起来简单。如果需要让这些 C++ 代码看起来更现代，更有“品味”，我想也不是很难的事情。

接口和实现希望尽量分离，对用的人少暴露细节。但不拘泥于教条，强求做成类似 COM 那样的通用 ABI 。还是尽量利用 C++ 语言本身提供的机制，不滥用。

使用尽量简单，不要让使用人员有太大负担。

功能满足最低需求即可。代码容易阅读，使用人员可以很快理解原理，不至于误用。也方便日后扩展以适应新的需求。

代码如下：（[可打包下载](http://blog.codingnow.com/file/cppgc0.1.zip)）

/*
* filename: i_gcobject.h
* Copyright (c) 2010 ,
* Cloud Wu . All rights reserved.
*
* http://www.codingnow.com
*
* Use, modification and distribution are subject to the "New BSD License"
* as listed at .
*/
#ifndef interfacce_gcobject_h
#define interfacce_gcobject_h
#define interface struct
interface i_gcobject {
virtual ~i_gcobject() {}
virtual void touch() {}
virtual void mark() = 0 ;
virtual void grab() = 0 ;
virtual void release() = 0 ;
static void collect();
};
#endif
所有支持 gc 管理的接口都继承至 `i_gcobject`

，提供三个方法，

mark 可以把这个对象打上标记，被标记的对象将不会被 collect 回收。

grab 将对象挂接到一个被称呼为 root 的特殊 gcobject 上。

release 将对象从 root 上取掉。


另提供 touch 的模板方法供 mark 回调，用来标记同一对象中的不同部分。

mark 方法一般在 touch 方法中使用，另外，collect 方法将主动调用 root 的 mark 。


/*
* filename: i_gcholder.h
* Copyright (c) 2010 ,
* Cloud Wu . All rights reserved.
*
* http://www.codingnow.com
*
* Use, modification and distribution are subject to the "New BSD License"
* as listed at .
*/
#ifndef interfacce_gcholder_h
#define interfacce_gcholder_h
#include "i_gcobject.h"
interface i_gcholder : virtual i_gcobject {
virtual void hold(i_gcobject *) = 0;
virtual void unhold(i_gcobject *) = 0;
static i_gcholder * create();
};
#endif
`i_gcholder`

为 root 的接口，提供 hold 和 unhold 方法来挂接需要持久保留的 gcobject 。


/*
* filename: gcobject.h
* Copyright (c) 2010 ,
* Cloud Wu . All rights reserved.
*
* http://www.codingnow.com
*
* Use, modification and distribution are subject to the "New BSD License"
* as listed at .
*/
#ifndef gc_object_h
#define gc_object_h
#include "i_gcobject.h"
class gcobject : virtual i_gcobject {
bool marked;
public:
gcobject();
virtual void mark();
virtual void grab();
virtual void release();
struct f_unmarked;
};
#endif
/*
* filename: gcobject.cpp
* Copyright (c) 2010 ,
* Cloud Wu . All rights reserved.
*
* http://www.codingnow.com
*
* Use, modification and distribution are subject to the "New BSD License"
* as listed at .
*/
#include "gcobject.h"
#include "i_gcholder.h"
#include
#include
static bool gc_trigger;
static std::vector gc_pool;
static i_gcholder * gc_root = i_gcholder::create();
struct gcobject::f_unmarked {
bool operator() (gcobject * value) {
bool unmarked = value->marked != gc_trigger;
if (unmarked) {
delete value;
}
return unmarked;
}
};
gcobject::gcobject() : marked(!gc_trigger)
{
gc_pool.push_back(this);
}
void
gcobject::mark()
{
if (marked != gc_trigger) {
marked = gc_trigger;
touch();
}
}
void
gcobject::grab()
{
gc_root->hold(this);
}
void
gcobject::release()
{
gc_root->unhold(this);
}
void
i_gcobject::collect()
{
gc_root->mark();
gc_pool.erase(remove_if(gc_pool.begin(), gc_pool.end() , gcobject::f_unmarked()), gc_pool.end());
gc_trigger = !gc_trigger;
}
gcobject 为具体的 gc 实现，实现了 mark 、grab、release 和 collect 方法。

mark 采用的直接向一 bool 变量设置标记。这个标记利用了 trigger 这个乒乓开关，每次 collect 都会切换状态。

grab 和 release 可以把对象挂接到 root 上，或从上取掉。

collect 会主动从 root 开始 mark ，并释放那些没有 mark 的对象。



/*
* Copyright (c) 2010 ,
* Cloud Wu . All rights reserved.
*
* http://www.codingnow.com
*
* Use, modification and distribution are subject to the "New BSD License"
* as listed at .
*/
#include "i_gcholder.h"
#include "gcobject.h"
#include
#include
#include
class gcholder : public virtual i_gcholder, virtual gcobject {
std::vector hold_set;
std::vector unhold_set;
bool set_changed;
bool hold_set_sorted;
bool unhold_set_sorted;
void combine_set();
virtual void touch();
virtual void hold(i_gcobject *obj) {
hold_set.push_back(obj);
hold_set_sorted = false;
set_changed = true;
}
virtual void unhold(i_gcobject *obj) {
unhold_set.push_back(obj);
unhold_set_sorted = false;
set_changed = true;
}
struct f_mark {
void operator() (i_gcobject *obj) {
obj->mark();
}
};
public:
gcholder() :
set_changed(false),
hold_set_sorted(true) ,
unhold_set_sorted(true) {}
};
void
gcholder::combine_set()
{
if (!hold_set_sorted) {
std::sort(hold_set.begin(),hold_set.end());
hold_set_sorted = true;
}
if (!unhold_set_sorted) {
std::sort(unhold_set.begin(),unhold_set.end());
unhold_set_sorted = true;
}
if (!unhold_set.empty()) {
std::vector::iterator iter1 = hold_set.begin();
std::vector::iterator iter2 = unhold_set.begin();
while (iter1 != hold_set.end() && iter2 != unhold_set.end()) {
if (*iter1 == *iter2) {
*iter1 = NULL;
++iter1;
++iter2;
}
else {
assert(*iter1 < *iter2);
++iter1;
}
}
i_gcobject * null = NULL;
hold_set.erase(std::remove(hold_set.begin(),hold_set.end(),null) , hold_set.end());
unhold_set.clear();
}
}
void
gcholder::touch()
{
if (set_changed) {
combine_set();
set_changed = false;
}
std::for_each(hold_set.begin(), hold_set.end(), f_mark());
}
i_gcholder *
i_gcholder::create()
{
return new gcholder;
}
gcholder 理论上可以有多个实例，并相互挂接。（否则不需要继承至 `i_gcobject`

）这个设计可以用来模拟多级的堆栈。但实际上并不需要这么复杂。因为在大部分应用里，如果你的程序有一个周期性的主循环，就可以不在 gc 系统里模拟出一个多级的堆栈。我们只用在循环之外做 collect 即可。再堆栈调用的较深层次触发 collect 反而效果不佳，会导致许多临时 gc 对象无法回收。


最后来看一个玩具代码，用 stl 里的 mutliset 实现了一个简单的树接口。可能没有什么使用价值，但它演示了一个较复杂的对象相互引用的关系。并可以展示 gc 如何正确工作。

/*
* filename: test.cpp
* Copyright (c) 2010 ,
* Cloud Wu . All rights reserved.
*
* http://www.codingnow.com
*
* Use, modification and distribution are subject to the "New BSD License"
* as listed at .
*/
#include "gcobject.h"
#include
#include
#include
interface i_tree : virtual i_gcobject {
virtual void link(i_tree *p) = 0;
static i_tree * create();
};
class tree : public virtual i_tree , virtual gcobject {
tree *parent;
std::multiset children;
struct f_mark {
void operator() (tree *node) {
node->mark();
}
};
virtual void touch() {
if (parent)
parent->mark();
std::for_each(children.begin(), children.end(), f_mark());
}
void unlink();
virtual void link(i_tree *parent);
public:
tree() : parent(NULL) {
printf("create node %p\n",this);
}
~tree() {
printf("release node %p\n",this);
}
};
void
tree::unlink()
{
if (parent) {
parent->children.erase(this);
parent = NULL;
}
}
void
tree::link(i_tree *p)
{
unlink();
if (p) {
tree * cp = dynamic_cast(p);
cp->children.insert(this);
parent = cp;
}
}
i_tree *
i_tree::create()
{
return new tree;
}
int
main()
{
i_tree *root = i_tree::create();
root->grab();
i_tree *node;
node = i_tree::create();
node->link(root);
node = i_tree::create();
node->link(root);
i_gcobject::collect();
printf("collected\n");
node->link(NULL);
i_gcobject::collect();
printf("finalize\n");
root->release();
i_gcobject::collect();
return 0;
}

我们在实现一个基于 gc 的对象时，可以先定义出需要的接口，让接口从 `i_gcobject`

继承。例如上例中的 `i_tree`

。

然后在实现这个接口时，可以虚继承 gcobject 。例如上例中的 `tree`

。

如果有需要，就重载 touch 方法，在 touch 方法中 mark 相关的 gcobject 。对于 tree 这个例子，就是调用父亲和孩子节点的 mark 。

对象依然可以写析构函数，相当于对象的 finalize 。在析构函数中，不要再释放和它相关的 gcobject ，那些留给 gc 系统去完成。（例如在 tree 里，就不要在 ~tree 中 delete children 容器中的变量，也不需要把自己从父亲节点上摘掉）


如果仅仅只是使用那些接口，则不需要再包含 gcobject.h ，因为 gcobject 的细节只供实现 `i_gcobject`

时使用。