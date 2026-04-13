---
title: 一次函数设计讨论
url: https://tonybai.com/2010/09/02/an-discussion-on-function-design/
published: '2010-09-02'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 一次函数设计讨论

近期在考虑对底层函数库进行一些[重构](http://tonybai.com/2006/03/28/c-refactoring/)，今天下午花了两个小时考量现有的函数库的接口设计，发现目前函数库的实现存在着一个普遍的问题：与特定的内存分配实现耦合的太紧。

我们的应用是多进程结构的，并使用了[共享内存](http://tonybai.com/2005/09/23/apr-shmem/)这种最快捷的IPC机制，鉴于此很多同事在实现一些数据结构或者算法时可能只考虑到了我们常见的应用场景-多进程共享，而对非共享内存分配的情况考虑不足。那如何将目前某些库函数实现与内存分配之间的强耦合解开呢？针对这道题我发起了一次mail讨论。

题目再重述一下：“目前底层库中的一些数据结构，比如xx_tree、xx_hash_table等，在它们的实现中都会有“分配内存空间”的需求，现有的实现多是直接调用已有的xx_shm_malloc和xx_shm_free在共享内存上动态申请和释放内存，但实际上有些场合我们并不需要在共享内存上分配内存，进程私有堆上的内存完全可以满足需求。如果让大家考虑修改目前xx_tree的实现或重新设计xx_tree的接口，以达到让xx_tree支持多种内存分配策略的目的，你是如额考虑的，请谈谈你的设计思路。"

Mail没发出去多久，就收到了同事A的回复。同事A近期正在对一个老应用的底层库做”翻新“，收到我这封Mail后他产生了共鸣，因为他也遇到了类似的问题。他目前的解决方法是：在xx_tree_t结构体里增加一个成员shared来表示是否在共享内存上申请内存，然后将原xx_tree_new接口改名为内部static接口new_tree，new_tree在申请内存时通过判断shared变量的值来决定到底使用哪种具体的内存分配方式。同样释放内存时也要根据shared的值来判断如何释放内存。原xx_tree_new外部接口通过将shared置为1，并调用new_tree实现;另外新增一个外部接口xx_tree_new_private，选择在进程堆上分配内存的实现方式。他对于这种修改的评价是："这种方法的好处是原接口没有变化，其它使用这个接口的程序代码无需修改。"

在某些场合下同事A的这种修改方案确也无可厚非，因为有时的确需要考虑对现有代码的影响。但如果该方案是对于xx_tree的一个全新的设计，那显然它没能很好解决我在题目中提出的耦合问题。xx_tree的创建还是依赖于具体的内存分配实现，虽然目前扩展成支持两种内存分配方式了，但付出了新增一个接口，内部增加若干”if…else“判断逻辑的代价。如果我再提供一种新的yy_malloc内存分配机制，那么这种方案下的xx_tree显然无法很好的应对这种变化。

一转眼间又有几封Mail回来，几位同事的思路居然与同事A的都不谋而合，看来大家对于接口变动带来影响还是心有余悸的。

同事A思维很活跃，很快他的第二种方案又公布出来了。其大致思路就是：可以在多种内存分配接口外面套上一个通用的接口，比如void* common_malloc(size, type)和void common_free(ptr)。xx_tree只需增加一个type字段，并在xx_tree_new中传入相应type，xx_tree内部实现一概使用common_malloc/common_free接口，并将type值传入相应接口。这样xx_tree与具体的内存分配机制实现的耦合就解开了。

这种方案中的common_malloc和common_free则似乎成了一种代理，解除了xx_tree与具体内存分配实现之间的耦合，但是这个代理却需要关心到具体的内存分配机制的实现。如果有新增内存分配方式，common_malloc和common_free依然需要修改，仍未达到理想状态。

同事B的Mail接踵而来。Mail中他谈了他的回调函数方案:

定义两个回调函数指针原型如下，

typedef void* (*hook_malloc)(int size);

typedef void (*hook_free)(void *);

修改xx_tree_new的接口，在接口原型中增加两个参数，一个是hook_malloc malloc_func，一个是hook_free free_func。这样在xx_tree的其他接口实现中只需回调malloc_func和free_func即可，它无须关心这两个指针对应的具体实现。

这个方案其实已经接近我的方案，但是我提出的问题是：如果xx_tree中使用calloc和realloc了怎么办？calloc与realloc从语意上与malloc又不同，函数原型上与malloc也无法兼容？当然了最简单的答案就是再定义两个针对calloc和realloc的函数原型，然后再为xx_tree_new增加两个参数。但这样下来参数数量是不是太多了！如果再增加其他语义的分配行为，xx_tree接口还得修改。

讨论到这里已接近下班时间，这个问题依旧留给大家继续思考。其实这个解耦合问题主要是想要大家知道通过面向接口而不是具体实现的编程可以降低甚至消除一些代码耦合，而C语言中”接口“的概念可以通过函数指针体现出来。

我这里也给出一种看似还不错的方案，(函数设计没有最好只有更好^_^，如果你有更好的想法，欢迎交流)

我定义了一个名为xx_allocator_t的结构体，其成员均为函数指针变量，这个xx_allocator_t就类似于Java里的interface，只定义了接口的行为规范（C的函数指针原型）。所有类似xx_tree需要支持多种内存分配方式的数据结构只要支持xx_allocator_t即可(将xx_allocator_t类型变量作为参数传入)。

/* x_allocator.h */

typedef void* (*x_alloc_func)(size_t size);

typedef void (*x_free_func)(void *ptr);

typedef void* (*x_calloc_func)(size_t nmemb, size_t size);

typedef void* (*x_realloc_func)(void *ptr, size_t size);

struct xx_allocator_t {

x_alloc_func af;

x_free_func ff;

x_calloc_func cf;

x_realloc_func rf;

};

业务层使用xx_tree的方法：

tree = xx_tree_new(&(struct xx_allocator_t){.af = malloc, .ff = free});

这里利用C99中的结构体赋值方式，即使你为xx_allocator_t增加一种新行为，这里的代码也不需要做什么修改。

这次讨论感觉大家都动了脑并参与了进来，达到了预期的效果，大家也很喜欢，我觉得可继续做下去，至于形式上可灵活变通。

© 2010, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

something like std::allocator ~