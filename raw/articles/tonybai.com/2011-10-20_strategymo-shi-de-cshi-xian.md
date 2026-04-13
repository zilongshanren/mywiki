---
title: Strategy模式的C实现
url: https://tonybai.com/2011/10/20/implement-strategy-pattern-in-c/
published: '2011-10-20'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Strategy模式的C实现

与那些复杂的模式相比，Stragegy Pattern([策略模式](http://zh.wikipedia.org/wiki/%E7%AD%96%E7%95%A5%E6%A8%A1%E5%BC%8F))是一个相对简单的模式，很直观，也易于理解。 同时它也是我们在开发过程中使用最多的模式之一。

问题是设计模式使用的驱动力，只有当我们遇到问题时，设计模式才会向我们伸出援助之手。这里我也想通过对问题以及解决方法演化的阐述来说明策略模式是如何更好地帮助我们的。我们从问题出发！

Tony最近接到了一个新任务，任务的内容是实现一个通用的平衡二叉树数据结构供其他同事使用。接到这个任务后，他十分欣喜，因为在之前的工作中他一直在用C语言编写繁芜复杂的业务逻辑，这让他感觉很烦躁。今天他终于盼到了一个做公共库的机会。为此Tony连夜拜读了《[C语言接口与实现](http://www.douban.com/subject/1230040/)》一书，希望能从书中取点经，做出一个让大家都满意的通用的平衡二叉树。

Tony十分欣赏《C语言接口与实现》中采用的一些原则，比如尽量隐藏细节，只给外部暴露必要的信息等。他也是按照书中的原则来定义平衡二叉树的各个操作接口的。但在定义接口的过程中Tony却遇到了问题，以平衡二叉树的创建和销毁接口为例，Tony最初设计的接口原型是这样的：

/* balanced_binary_tree.h */

… …

struct bb_tree_t;

int bb_tree_create(struct bb_tree_t **tree, …);

int bb_tree_destroy(struct bb_tree_t **tree, …);

… …

/* balanced_binary_tree.c */

struct bb_tree_t {

…

};

… …

很显然，为了隐藏细节，Tony选择了在接口实现内部为tree分配和释放内存空间，但他不确定应该用哪种内存分配方式。他经过一番思维斗争后最终选择了使用标准库中的[malloc](http://bigwhite.blogbus.com/logs/77791357.html)和free，因为他坚定地认为多数人都会使用这套标准的内存管理接口，例外的可能性很小。后续的实现过程很顺利，当这套"设计优美"的平衡二叉树公共库被提交给其他同事使用时，Tony感觉十分地开心。

/* balanced_binary_tree.c */

int bb_tree_create(struct bb_tree_t **tree, …) {

struct bb_tree_t *p = (struct bb_tree_t*)malloc(sizeof(*p));

…

}

int bb_tree_destroy(struct bb_tree_t **tree, …) {

free(*tree);

… …

}

不过墨菲定律告诉我们：事情如果有变坏的可能，不管这种可能性有多小，它总会发生。果然好景不长，这一天一位同事找到了Tony并向他诉苦到："我们需要在共享内存上使用平衡二叉树，但你提供的bb_tree只能在堆上分配内存，无法被多个进程共享，我们真不知道该怎么办了，不知道你能否修改一下你提供的库，让它也支持在共享内存上分配呢"。Tony是个自尊心很强的人，听到自己提供的公共库有缺陷，他的心中只有一个念头：尽快解决这个问题！

Tony回到座位上开始重新审视自己的设计，他满脑子都是"既要支持标准内存分配接口，又要支持在共享内存上分配"的需求。在考量了十几分钟后，他似乎知道该怎么做了，他在屏幕上敲下了如下代码：

/* balanced_binary_tree.h */

… …

struct bb_tree_t;

enum mem_allocator_flag {

STD_ALLOCATOR,

SHM_ALLOCATOR

};

int bb_tree_create(struct bb_tree_t **tree, enum mem_allocator_flag flag, …);

int bb_tree_destroy(struct bb_tree_t **tree, …);

… …

/* balanced_binary_tree.c */

struct bb_tree_t {

…

enum mem_allocator_flag flag;

};

int bb_tree_create(struct bb_tree_t **tree, enum mem_allocator_flag flag, …) {

… …

struct bb_tree_t *p

if (flag == STD_ALLOCATOR)

p = (struct bb_tree_t*)malloc(sizeof(*p));


if (flag == SHM_ALLOCATOR)

p = (struct bb_tree_t*)shm_malloc(sizeof(*p));

p->flag = flag;

… …

}

int bb_tree_destroy(struct bb_tree_t **tree, …) {

… …

if ((*tree)->flag == STD_ALLOCATOR)

free(*tree);


if ((*tree)->flag == SHM_ALLOCATOR)

shm_free(*tree);

… …

}

嗯，这样改后就应该支持在共享内存上分配平衡二叉树了。Tony似乎又恢复了信心,表情也不再那么死板严肃了！他伸伸懒腰，感觉有些疲倦，于是他决定趴在办公桌上小憩一会儿。恍惚中一个同事来到了他的跟前，对他说："Tony，标准内存分配接口使用的内存分配算法效率太低，时间长了又会导致太多的内存碎片，完全不能满足我们的需求，我们希望能在平衡二叉树中使用我们自己实现的一套高性能内存分配接口，你必须尽快做出修改，不然…."。Tony瞬间从梦中惊醒，他努力地回忆了一下刚才梦中的情景，又看了看屏幕上刚刚修改过的代码，心生一丝窃喜，"还好这只是一场梦，否则这份代码又要被人嘲笑了。内存管理的接口有N多种，我总不能每支持一种新分配算法就重新发布一次吧"。Tony又一次陷入了沉思。不过这次沉思显然也没有持续多久，Tony似乎又找到了解决方案，屏幕上的代码发生了变化。

/* balanced_binary_tree.h */

… …

struct bb_tree_t;

int bb_tree_create(struct bb_tree_t **tree,

void (*malloc_func)(size_t size),

void (*free_func)(void *ptr), …);

int bb_tree_destroy(struct bb_tree_t **tree, …);

… …

/* balanced_binary_tree.c */

struct bb_tree_t {

…

void (*malloc_func)(size_t size),

void (*free_func)(void *ptr)

};

int bb_tree_create(struct bb_tree_t **tree,

void (*malloc_func)(size_t size),

void (*free_func)(void *ptr), …) {

struct bb_tree_t *p = (struct bb_tree_t*)malloc_func(sizeof(*p));

p->malloc_func = malloc_func;

p->free_func = free_func;

… …

}

int bb_tree_destroy(struct bb_tree_t **tree, …) {

(*tree)->free_func(*tree);

… …

}

这回Tony把使用何种存储分配机制的权力完完全全地交给了库的使用者，这样纵使内存分配机制有千般变化，这里也依旧可以满足。不过这次Tony还是长了个心眼儿，没有马上将库发布给其他同事，而是从优秀代码设计的角度再次对自己的代码做了一次分析。

Tony暂时抛开了bb_tree，而是从所有类似的公共库的设计和实现角度考虑了许久。他发现如果公共库的设计都遵循将细节隐藏，只暴露必要信息的原则的话，势必都会遇到类似的如何在内部进行存储分配的问题。bb_tree使用到了malloc和free接口，但其他公共库很可能还会用到calloc、realloc等接口。一旦遇到这种情况，按照上面的方案就会出现类似下面的函数原型形式：

int xx_create(…,

void (*malloc_func)(size_t size),

void (*calloc)(size_t nmemb, size_t size),

void (*realloc)(void *ptr, size_t size),

void (*free_func)(void *ptr)…);

Tony意识到这个函数原型参数太多，使用不便，代码味道自然不好！应该重构一下，将变化的事物封装起来。综上来看，目前主要有两点易变的地方：

1) 内存分配接口需支持可替换

2) 不同公共库可能使用不同形式的内存分配接口，有的用符号malloc原型的，有的用符合calloc原型的。

"封装变化！"，Tony潜意识里跳出的第一个想法。于是十几分钟过后他的电脑屏幕上就出现了下面这些代码：

/* mem_allocator.h */

struct mem_allocator_t {

void (*malloc)(struct mem_allocator_t *allocator, size_t size),

void (*calloc)(struct mem_allocator_t *allocator, size_t nmemb, size_t size),

void (*realloc)(struct mem_allocator_t *allocator, void *ptr, size_t size),

void (*free)(struct mem_allocator_t *allocator, void *ptr)

};

/* balanced_binary_tree.h */

#include "mem_allocator.h"

… …

struct bb_tree_t;

int bb_tree_create(struct bb_tree_t **tree,

const struct mem_allocator_t *allocator, …);

int bb_tree_destroy(struct bb_tree_t **tree, …);

… …

/* balanced_binary_tree.c */

struct bb_tree_t {

…

const struct mem_allocator_t *allocator;

};

int bb_tree_create(struct bb_tree_t **tree,

struct mem_allocator_t *allocator, …) {

struct bb_tree_t *p = (struct bb_tree_t*)(allocator->malloc(allocator, sizeof(*p)));

p->allocator = allocator;

… …

}

int bb_tree_destroy(struct bb_tree_t **tree, …) {

struct mem_allocator_t *allocator = (*tree)->allocator;

allocator->free(allocator, *tree);

… …

}

Tony封装出一个接口mem_allocator_t，bb_tree的创建和销毁只依赖于mem_allocator_t。我们可以为bb_tree_create传入不同的mem_allocator_t接口的实现，以支持内存分配机制的更换；另外mem_allocator_t内部封装了所有形式的通用的内存管理原型，可以满足其他公共库实现的需要。

面向对象语言可以通过继承(derive)接口、重写方法(override method)的方式实现一个接口，但在C中，我们只能像下面这样给出mem_allocator_t接口的一个实现 – shm_mem_allocator：

/* shm_mem_allocator.h */

#include "mem_allocator.h"

struct mem_allocator_t* shm_mem_allocator_new();

void shm_mem_allocator_free(struct mem_allocator_t **allocator);

/* shm_mem_allocator.c */

struct shm_mem_allocator_t {

struct mem_allocator_t allocator;

… … /* 其他用于实现shm_mem_allocator所需要的字段 */

};

struct mem_allocator_t* shm_mem_allocator_new() {

struct shm_mem_allocator_t *allocator = (struct shm_mem_allocator_t*)malloc(sizeof(*allocator));

if (!allocator)

return NULL;

memset(allocator, 0, sizeof(*allocator));

allocator->allocator.malloc = shm_mem_alloc;

allocator->allocator.calloc = shm_mem_calloc;

allocator->allocator.realloc = shm_mem_realloc;

allocator->allocator.free = shm_mem_free;


return (struct mem_allocator_t*)allocator;

}

static void* shm_mem_malloc(struct mem_allocator_t *allocator, size_t size) {

struct shm_mem_allocator_t *p = (struct shm_mem_allocator_t*)allocator;

… …

}

static void* shm_mem_calloc(struct mem_allocator_t *allocator, size_t nmemb, size_t size) {

struct shm_mem_allocator_t *p = (struct shm_mem_allocator_t*)allocator;

… …

}

static void* shm_mem_realloc(struct mem_allocator_t *allocator, void *ptr, size_t size) {

struct shm_mem_allocator_t *p = (struct shm_mem_allocator_t*)allocator;

… …

}

static void shm_mem_free(struct mem_allocator_t *allocator, void *ptr) {

struct shm_mem_allocator_t *p = (struct shm_mem_allocator_t*)allocator;

… …

}

void shm_mem_allocator_free(struct mem_allocator_t **allocator) {

struct shm_mem_allocator_t *p = (struct shm_mem_allocator_t*)(*allocator);

free(p);

(*allocator) = NULL;

}

注意shm_mem_allocator本身也涉及到内部实现的内存分配问题，但考虑到其自身的特质：我们无须在共享内存上创建mem_allocator实例对象，也无须为mem_allocator实例对象内部的内存分配算法性能担忧(只是初始化时使用一次)，因此可以无须支持多种内存分配接口，利用标准内存分配接口足矣。

下面是将bb_tree与shm_mem_allocator结合在一起使用的代码：

struct bb_tree_t *tree;

ret = bb_tree_create(&tree, shm_mem_allocator_new(), …);

… …

如果你要更换bb_tree内部的内存分配器，则在调用bb_tree_create时换用你自己的mem_allocator_t接口实现即可：

struct bb_tree_t *tree;

ret = bb_tree_create(&tree, your_mem_allocator_new(), …);

… …

Tony终于找到了一份可以让自己满意的方案了。在发布代码库后，他再也没有收到来自同事们的抱怨之声。在接下来的一个星期里，Tony又用同样的设计方案让产品可以支持从多种数据库(Oracle、MySQL、Sqlite3等)读取数据。

后来，Tony在翻阅《[设计模式](http://book.douban.com/subject/1052241)》一书时，发现自己的解决方法与书中描述的“策略模式”甚为类似，简直就是用C语言实现的策略模式，而且这种模式几乎没有什么缺点，除了每增加一种策略（比如新增一种mem_allocator_t接口的实现），就要多维护一种策略的代码，但这样带来的负担与之前相比几乎是可以忽略不计的。

© 2011, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

为什么不采用类似Linux内核的list.h一样，将内存管理交给用户自己管理？