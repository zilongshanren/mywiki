---
title: 偿还N年前的一笔技术债
url: https://tonybai.com/2011/07/21/pay-for-a-tech-debt-of-several-year-ago/
published: '2011-07-21'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 偿还N年前的一笔技术债

记得刚来公司时曾参与过一个项目，项目中用到了部门基础库中的一个[B+树](http://en.wikipedia.org/wiki/B%2B_tree)接口。不过在程序调试过程中我们发现可执行程序总是dump core（在sparc [solaris](http://tonybai.com/2009/09/10/something-about-installing-solaris-10/)上），经初步分析，断定问题就出在B+树接口处，但一时又找不到问题原因。还好这个B+树的实现者就坐在我的旁边。他分析后告诉我：这个B+树接口要求用户自定义的索引结构体的size应该为4的整数倍。按照他的说法，我为结构体打了padding，以满足结构体size为4的整数倍的要求。修改后果然不再dump core了。当时项目进度紧，我也没有求甚解，这件事也就过去了。

一晃N年过去了。今天在做程序的64位移植过程中我再次遇到了这个问题。问题的表象就是程序运行时dump core，通过[gdb](http://tonybai.com/2006/01/08/debug-multiple-process-program-using-gdb/)或pstack查看core的内容，发现程序是在B+ Tree初始化时出的core。显然这又是一个内存违规访问的问题，且在Sparc上出现（x86 Linux上运行正常）十有八九与[内存对齐](http://tonybai.com/2005/08/09/also-talk-about-memory-alignment/)有关。

B+ Tree出问题首先让我想到了N年前的那个解决方法。我先查看了自定义的索引结构体(usr_idx)：

struct usr_idx {

unsigned int usr;

};

不过sizeof(usr_idx)无论是32bit编译还是64bit编译，其值都是4。那按照B+树原作者的说法，这显然不足以让B+树出现问题。事实也的确如此，32bit编译的程序在Sparc Solaris下运行良好，只是目前改为了64bit编译，才dump core，那问题到底出现在哪呢？

到这里，我也只能从代码着手了，把N年前没弄清楚的原因找出来，顺便也把这个存在了N年的Bug彻底解决掉，把这笔[技术债](http://en.wikipedia.org/wiki/Technical_debt)还了。pstack的输出告诉我问题出在一个名为bptree_create_node的函数中，嫌疑最大的一处代码大致是这样的：

for (i = 0; i rank; i++) {

(elem_base(tree, tmp_bn, i))->key = key_base(tree, tmp_bn, i);

(elem_base(tree, tmp_bn, i))->pointer = NULL;

}

直觉告诉我问题出在elem_base这个宏里，elem_base的定义如下：

#define elem_base(tree, eb, index) ((xx_bptree_elem*)((char *)&(eb)->e_base.mw_cp + ((SIZEOF_bptree_elem + (tree)->keysize))*(index)))

很显然这个定义最终是想得到一个xx_bptree_elem*类型的指针。从内存地址角度来说，我们会得到了一个内存地址，且这个地址被认为是一个xx_bptree_element元素的起始地址。那么是否所有地址作为xx_bptree_element元素的起始地址都合法呢？答案是不一定，至少在Sparc平台上不是所有地址都可以作为xx_bptree_elem的起始地址的。

那么什么样地址可以作为xx_bptree_element的起始地址呢？在Sparc上这取决于结构体的对齐系数。xx_bptree_elem结构的定义如下：

union mem_word {

void *mw_vp;

void (*mw_fp)(void);

char *mw_cp;

long mw_l;

double mw_d;

};

typedef union mem_word mem_word;

#define SIZEOF_mem_word (sizeof(mem_word))

struct xx_bptree_elem {

void *key;

void *pointer;

mem_word base;

};

typedef struct xx_bptree_item xx_bptree_item;

#define SIZEOF_bptree_elem (sizeof(xx_bptree_elem)-sizeof(mem_word))

在32bit编译的情况下，系统默认对齐系数为4(参见/usr/include/sys/isa_defs.h中的宏_MAX_ALIGNMENT)，则该结构体的对齐系数 = min(max(sizeof(key), sizeof(pointer), sizeof(base)), 4) = 4。这样xx_bptree_elem在32bit下的有效起始地址为可被4整除的内存地址。

而在用64bit编译时，系统默认的对齐系数为16（同参见isa_defs.h），但由于xx_bptree_elem中size最大的字段(base)的size为8，则结构体的对齐系数就等于8。即xx_bptree_elem元素的有效起始地址为可被8整除的地址。

好了，我们再回过头来看看elem_base宏在不同编译情况下能否总是返回合法的地址。

#define elem_base(tree, eb, index) ((xx_bptree_elem*)((char *)&(eb)->e_base.mw_cp + ((SIZEOF_bptree_elem + (tree)->keysize))*(index)))

这个宏中有三个元素决定返回地址，分别是"基址"：&(eb)->e_base.mw_cp、偏移量SIZEOF_bptree_elem和(tree)->keysize。其中基址是另外一个结构体xx_bptree_node中一个mem_word类型字段的地址，你知道的，mem_word这种手法可以保证其起始地址严格按照其内部最大字段的对齐系数对齐的，也就是说mem_word的对齐系数与double的对齐系数一致，即无论是32bit编译还是64bit编译，其对齐系数都是8，也就是说我们可以确保这个”基址“是可以被8整除的；至于偏移量SIZEOF_bptree_elem，我们可以直接可以得出其大小：

32bit下，SIZEOF_bptree_elem = 8

64bit下，SIZEOF_bptree_elem = 16

可以看出无论是32bit还是64bit编译，SIZEOF_bptree_elem的值都是8的倍数；显然这两个值都不会影响elem_base最终返回地址的合法性。

现在剩下的就是(tree)->keysize了。keysize是由xx_bptree_init接口传进来的，它在上层实际上就是用户自定义的索引结构体的大小，显然这个大小不一定就是8的倍数。在我们的系统中，keysize = sizeof(usr_idx) =

4。这个keysize在32bit编译下是没有问题的，因为32bit编译只需要elem_base返回的地址可以被4整除即可，这也是为什么我们的程序在32bit编译下运行正常的原因。回想一下N年前的那个问题，其真正原因也就在这里：当时我定义的索引结构体的大小无法被4整除。在64bit编译下，keysize显然不能满足被8整除的要求，导致elem_base返回的地址只能被4整除。而xx_bptree_elem这个结构体的地址是严格要求必须可被8整除的。将一个只能被4整除而不能被8整除的地址强制转换为xx_bptree_elem元素地址并通过该强制类型转换后的地址访问xx_bptree_elem内部的元素显然就会导致core的出现了。

现在看来当初我的同事并未真正理解该B+ tree为何要求用户自定义结构体的大小必须为4的整数倍了，他只是通过现象得到了那条经验罢了，这笔技术债务也就从那时留了下来。

解决该问题并不难，作为基础库，我们无论如何都不应该依赖用户的自觉，我们在接口实现中增加一个转换就可以解决这一隐藏了若干年的Bug，将外面传入的keysize经align_word转换后再赋给tree->keysize，这样就可以保证elem_base始终返回合法的地址了。

突然想起了那句话：”出来混，总是要还的“，我们欠的[技术债务](http://en.wikipedia.org/wiki/Technical_debt)也不例外。

© 2011 – 2013, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论