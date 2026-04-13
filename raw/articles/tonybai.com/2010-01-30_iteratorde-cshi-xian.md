---
title: iterator的C实现
url: https://tonybai.com/2010/01/30/implement-iterator-in-c/
published: '2010-01-30'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# iterator的C实现

这几天一直处于编码状态，也找回了一些对代码的良好感觉。

昨天晚上闲暇时翻阅“[Head First设计模式](http://www.douban.com/subject/2243615/)”，当翻到迭代器模式时，突然有了想法：实现一个iterator。这几天编码时恰好也写了一个简单的带有遍历功能的小数据结构，不妨用iterator改造一下这个数据结构的遍历接口，看是否能成行。

迭代器模式较为简单，网上的文章也多得很，这里就不再贽述了，直接看实现思路和代码吧。

在迭代器模式中，有几个角色不得不说，一就是iterator本身，还有一个就是所谓的“容器类”，容器类三个字显得概念很大，这里不用之。我们换一种轻松的说法，就是带有遍历功能的一类数据结构吧，这里记为类型T。类型T千变万化，iterator则以不变应万变，提供一种在无需知道T内部实现行为前提下的对T实例内各元素的有序遍历的接口。

这样一来iterator的应用场景大致就应该是这样的：

T *t;

T_item_t *ti;

// …

iterator *itor = T_iterator(t);


for ( ; has_next(itor); ) {

ti = (T_item_t*)get_next(itor);

// …

}

iterator_free(itor);

这里我们使用了四个函数has_next, get_next、iterator_free和T_iterator。其中has_next、get_next和iterator_free是iterator提供的函数接口，T_iterator则是需要每个支持iterator的数据结构去实现的接口。

以下是iterator.h的主要代码片段：

/* iterator.h */

#ifndef _ITERATOR_H_

#define _ITERATOR_H_

enum {

FALSE = 0,

TRUE = 1

};

typedef int bool; /* TRUE or FALSE */

typedef struct iterator iterator;

typedef bool (*HAS_NEXT_HOOK_FUNC)(void *collection_instance, void *collection_inner_itor);

typedef void* (*GET_NEXT_HOOK_FUNC)(void *collection_instance, void *collection_inner_itor);

/* 提供给T类型实现T_interator时使用 */

iterator* iterator_new(void *collection_instance,

void *collection_inner_itor,

HAS_NEXT_HOOK_FUNC h,

GET_NEXT_HOOK_FUNC g);

bool has_next(iterator *itor);

void* get_next(iterator *itor);

void iterator_free(iterator *itor);

#endif /* _ITERATOR_H_ */

iterator_new接口主要供类型T实现T_iterator接口时使用，目的是对类型T屏蔽iterator的内部结构实现；collection_instance指向T的实例；collection_inner_itor则是类型T内部实现的一个保存iterator状态的变量，每个类型T都应该有这样一个内部数据；两个callback函数则分别由类型T内部实现，在T_iterator实现中调用iterator_new时传入。iterator对T有一定的侵入性，这在C语言中似乎是不可避免的，即使在[Java](http://bigwhite.blogbus.com/logs/515958.html)中支持iterator接口的类也需要提供一个creatIterator的public接口，另外实现iterator接口的iterator类也需要提供具体的get_next和has_next实现。

以下则是iterator.c的代码，没有太多值得多说的地方，相信大家都可以看懂^_^：

/* iterator.c */

struct iterator {

void *collection_instance;

void *collection_inner_itor;

HAS_NEXT_HOOK_FUNC _has_next;

GET_NEXT_HOOK_FUNC _get_next;

};

iterator* iterator_new( void *collection_instance,

void *collection_inner_itor,

HAS_NEXT_HOOK_FUNC h,

GET_NEXT_HOOK_FUNC g) {

iterator *itor = NULL;

itor = calloc(1, sizeof(*itor));

if (!itor) return NULL;

itor->collection_instance = collection_instance;

itor->collection_inner_itor = collection_inner_itor;

itor->_has_next = h;

itor->_get_next = g;

return itor;

}

void iterator_free(iterator *itor) {

if (itor) {

if (itor->collection_inner_itor) free(itor->collection_inner_itor);

free(itor);

}

}

bool has_next(iterator *itor) {

return itor->_has_next(itor->collection_instance, itor->collection_inner_itor);

}

void* get_next(iterator *itor) {

return itor->_get_next(itor->collection_instance, itor->collection_inner_itor);

}

有了iterator，我们再举一个支持iterator遍历的list的例子，这里就不列出全部代码了，仅将关键的接口实现放出：

/* x_list.c */

struct x_list_inner_itor {

x_list_item_t *item;

};

static bool x_list_has_next(void *collection_instance, void *collection_inner_itor) {

x_list_t *list = (x_list_t*) collection_instance;

struct x_list_inner_itor *p = (struct x_list_inner_itor *)collection_inner_itor;

x_list_item_t *item = p->item;

return (X_LIST_NEXT(item) != X_LIST_DUMMY_HEAD(list));

}

static void* list_get_next(void *collection_instance, void *collection_inner_itor) {

struct x_list_inner_itor *p = (struct x_list_inner_itor *)collection_inner_itor;

x_list_item_t *item = p->item;

p->item = X_LIST_NEXT(item);

return p->item;

}

iterator* x_list_iterator(x_list_t *list) {

struct x_list_inner_itor *p = NULL;

p = calloc(sizeof(*p), 1);

if (!p) return NULL;

p->item = X_LIST_DUMMY_HEAD(list);

return iterator_new(list,

(void*)p,

x_list_has_next,

x_list_get_next);

}

以上只是提供了iterator的C实现的一种思路，大家见仁见智吧。

© 2010 – 2013, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

个人认为没有必要写has_next函数，get_next返回null或者0时迭代器终止就可以了