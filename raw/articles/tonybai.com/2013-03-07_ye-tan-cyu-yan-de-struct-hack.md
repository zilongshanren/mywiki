---
title: 也谈C语言的Struct Hack
url: https://tonybai.com/2013/03/07/struct-hack-in-c/
published: '2013-03-07'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 也谈C语言的Struct Hack

今天在浏览网友[huangz](http://huangz.me)编写的“[Redis源码分析](https://right-track-wrong-train.readthedocs.org/en/latest/storage/redis_code_analysis/index.html)”时，看到如下[redis](http://redis.io)中的代码：

struct sdshdr {

int len;

int free;

char buf[];

};

说实话，这类代码我见过很多，但直到这次我才知道这种coding trick的真实英文称谓是：Struct Hack。

到底什么是Struct Hack？其实倒也没有什么明确定义。首先它是一种coding trick；其次一定是与struct相关的；关键是struct中要仅有一个变长的字段，且该字段是struct中最后的一个字段，就像上面 sdshdr中的buf那样。这样的coding trick到底有何作用呢？

我们来看看redis中是如何利用这种coding trick的。sds是redis string的一种实现，全称是[Simple Dynamic Strings](http://redis.io/topics/internals-sds)，从字面意义来看，这是一种动态字符串，是可以在运行时确定其大小并创建的。我们来看看其创建代码：

typedef char *sds;

sds sdsnewlen(const void *init, size_t initlen) {

struct sdshdr *sh;

if (init) {

sh = zmalloc(sizeof(struct sdshdr)+initlen+1);

} else {

sh = zcalloc(sizeof(struct sdshdr)+initlen+1);

}

if (sh == NULL) return NULL;

sh->len = initlen;

sh->free = 0;

if (initlen && init)

memcpy(sh->buf, init, initlen);

sh->buf[initlen] = '\0';

return (char*)sh->buf;

}

sdsnewlen在分配内存时，一次分配的内存大小不仅仅是sizeof(struct sdshdr)，而是加上了真正存储字符串的buf的大小，并将buf作为返回值返回，sds就是buf，buf就是sds。这样通过sdshdr实例， 我们可以直接获得其对应的sds，也就是buf。更为关键的一点是，如果我已知sds，我们还可以获得其对应的sdshdr（huangz在文中称 sdshdr是sds handler的缩写，我倒是觉得hdr更像是header的缩写），见下面代码：

static inline size_t sdslen(const sds s) {

struct sdshdr *sh = (void*)(s-(sizeof(struct sdshdr)));

return sh->len;

}

这种trick给代码带来的极大的效率。想象一下如果redis的sdshdr定义是这样的：

struct sdshdr {

int len;

int free;

char *buf;

};

/* sdsnewlen */

struct sdshdr *sh;

sh = zmalloc(sizeof(struct sdshdr));

memset(sh, 0, sizeof(*sh));

sh->buf = zmalloc(initlen+1);

…

看起来似乎也能在运行时实现buf的动态size指定，但sdshdr与sds之间的纽带就被彻底割裂了（当然你也可以在 malloc sh时将buf内存也一并分配出来，然后手工将buf指向struct外的内存首地址，不过一旦这么做，就显得不那么tricky了）。

另外这里要探讨的是最后那个字段buf，是声明为buf[]好，还是buf[0]好，又或是buf[1]呢？redis使用的是buf[]，在[C99](http://en.wikipedia.org/wiki/C99)中这 是绝对合法的，这种定义被称为variable-length arrays(变长数组)。由于下标为空，这里的buf就好像是一个占位符，只有符号意义，但却并不实际占用空间。32bit平台下 sizeof(struct sdshdr) = 8，显然没有buf的份儿。不过在C99以前的标准中，是不允许变长数组出现的，你的Gcc很可能出现如下警告：“ISO C90 不允许可变数组成员”。不过C99以前很多编译器的扩展默认都是支持变长数组的，这也是这种trick之前就大行其道的原因之一，只不过是在C99之后变 得名正言顺了罢了。

如果将buf[]改为buf[0]呢？在C99以及支持变长数组扩展的编译器下也都是等同于buf[]的，不过C99以前的标准编译器还是会警告：ISO C 不允许大小为 0 的数组‘buf’ [-pedantic]。

用buf[1]替代buf[]则是一个兼容性最好的方案。在一些其他开源代码中，你也会常见buf[1]这种情形，如果以redis hds代码为例，我们用buf[1]替代buf[0]：

struct sdshdr {

int len;

int free;

char buf[1];

};

相应的，sdsnewlen的代码以及sdslen中通过sds获取sdshdr的代码就应该做相应的修改了，简要修改如下：

/* sdsnewlen */

…

sds sdsnewlen(const void *init, size_t initlen) {

struct sdshdr *sh;

if (init) {

**sh = zmalloc(sizeof(struct sdshdr) – 1 + initlen + 1);**

} else {

**sh = zcalloc(sizeof(struct sdshdr) – 1 + initlen + 1);**

}

if (sh == NULL) return NULL;

sh->len = initlen;

sh->free = 0;

if (initlen && init)

memcpy(sh->buf, init, initlen);

sh->buf[initlen] = '\0';

return (char*)sh->buf;

}

…

static inline size_t sdslen(const sds s) {

struct sdshdr *sh = **(void*)(s-(offsetof(struct sdshdr, buf)));**

return sh->len;

}

注意：使用这种coding trick为的就是获得一种运行时的动态行为，struct的大小也是动态的（这种struct的声明是一种incomplete type），所以这种struct都是在堆上分配内存的，在栈上分配显然是没有标准可移植的方法的；同样，由于是size不确定的incomplete type，这种struct一般不用于声明struct数组。

© 2013, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论