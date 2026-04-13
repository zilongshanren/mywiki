---
title: Memcached CAS应用一例
url: https://tonybai.com/2013/11/01/a-case-of-applying-memcached-cas/
published: '2013-11-01'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Memcached CAS应用一例

近期收到客户一个需求，我将该需求转述为下面这个等价的问题。

**【问题】**

* 有一个产品包装系统*S*，为某种产品*P*提供产品包装服务;

* 系统*S*由若干个处理节点组成，每个节点都可以单独处理组件;

* 产品*P*的一个可出厂的**成品**由包装盒+N个产品组件组成，包装盒与产品组件上都贴有一个标签，该标签上包含该成品的唯一编号ID（一定时间范围内有效）、每个组件自己的序号(unit-num)以及成品的组件总个数(unit-total)。每个成品只有一个包装盒，该包装盒的组件序号为0。其中unit-num <= unit_total == N <= 32;

* 某个成品的诸多组件是乱序到达*S*并由*S*送到产品包装工位的；当系统*S*第一次接收到一个成品的某个组件时，*S*会将一个包装盒贴上该组件对应的成品ID，并将其放在传送带上，传送给对应的组装工位；当系统*S*接收到同一成品的其他组件时，不再重新发放包装盒了；

* 系统*S*具有剔除冗余组件的功能，如果某个成品的某个组件（序号为n）已经被S接收并送到指定包装位，后续若再出现同一成品的相同序号组件（可能是因为标签贴错导致），*S*将会将该冗余组件剔除出包装线;

* 当某个成品的最后一个组件被*S*处理后，该成品的ID即告无效了，可以被后续成品重复使用了。

**【解决思路】**

这个问题中有几个关键功能点：

* 每个成品只分配一个包装盒；

* 支持剔重；

* 当最后一个组件被处理后，成品**ID**被从系统中删除，可被后续成品重复使用。

这是一个典型的多个节点并发操作的一致性问题，我们初步考虑基于开源的[Memcached](http://memcached.org/)的[CAS](http://en.wikipedia.org/wiki/Compare-and-swap)服务去解决该问题，解决思路如下：

a) *S*系统中的某个节点收到某成品的某个组件(unit_num = n)后，以ID为Key尝试获取成品的Value(以及item_cas值)；如果索引尚未在系统建立，那么创建索引，以ID为Key，Value为一整型字符串，初值为1<<(n-1)；并分配包装盒；

b) 如果以成品ID为Key的索引已经建立，系统节点将组件的(1<<n)与Value进行“与操作”以判断该组件是否为重复组件，如果为1，则为重复组件；否则以(Value + 1 << (n-1))的值以及获得的item_cas发起cas操作；

c) 如果cas操作成功，则数一下((Value + 1 << (n-1)) 中置位（=1）的bit个数，如果个数==unit-total，则删除索引；否则继续处理下一个组件；

如果cas操作失败，则回到步骤a)。

**【Demo代码】**

/* pack_sys.c */

… …

#include <libmemcached/memcached.h>

static const char *product_id = "nexus5";

static const int component_in_total = 5;

static const int component_order[] = {2, 3, 1, 2, 5, 4};

//code from <Algorithms.for.Programmers.Ideas.and.Source.Code>

static inline unsigned long long

bit_count(unsigned long long x)

{

x = (0x5555555555555555UL & x) + (0x5555555555555555UL & (x >> 1));

x = (0x3333333333333333UL & x) + (0x3333333333333333UL & (x >> 2));

x = (0x0f0f0f0f0f0f0f0fUL & x) + (0x0f0f0f0f0f0f0f0fUL & (x >> 4));

x = (0x00ff00ff00ff00ffUL & x) + (0x00ff00ff00ff00ffUL & (x >> 8));

x = (0x0000ffff0000ffffUL & x) + (0x0000ffff0000ffffUL & (x >> 16));

x = (0x00000000ffffffffUL & x) + (0x00000000ffffffffUL & (x >> 32));

return x;

}

int

main(int argc, char *argv[])

{

memcached_st *memc;

memcached_return_t rc = MEMCACHED_SUCCESS;

memcached_server_st *server = NULL;

memc = memcached_create(NULL);

if (NULL == memc) {

printf("memcached_create error\n");

return -1;

}

… …

rc = memcached_behavior_set(memc, **MEMCACHED_BEHAVIOR_SUPPORT_CAS**, 1);

if (rc != MEMCACHED_SUCCESS) {

printf("memcached_behavior_set support cas error: %s\n",

memcached_strerror(memc, rc));

return -1;

}

/* pack the component one by one */

int ret = 0;

int i = 0;

for (i = 0; i < sizeof(component_order)/sizeof(component_order[0]); i++) {

ret = pack_component(memc, component_order[i]);

if (ret == 0) {

printf("pack component [%d] ok\n”, component_order[i]);

} else if (ret == 1) {

printf("pack component [%d] exists\n”, component_order[i]);

} else {

printf("other error occurs\n");

return -1;

}

getchar();

}

return 0;

}

int

pack_component(memcached_st *memc, int i)

{

memcached_return_t rc = MEMCACHED_SUCCESS;

uint32_t mask = 1 << (i – 1);

uint32_t value_added = 1 << (i – 1);

char value_added_str[11] = {0};

uint32_t value = 0;

char *pvalue = NULL;

size_t value_len = 0;

uint32_t flags = 0;

while(1) {

pvalue = memcached_get(memc, product_id, strlen(product_id),

&value_len, &flags, &rc);

if (!pvalue) {

if (rc == MEMCACHED_NOTFOUND) {

printf("componet [%d] – memcached_get not found product key: [%s]\n",

i, product_id);

memset(value_added_str, 0, sizeof(value_added_str));

sprintf(value_added_str, "%u", value_added);

rc = memcached_add(memc, product_id, strlen(product_id), value_added_str,

strlen(value_added_str), 1000, 0);

if (rc == MEMCACHED_DATA_EXISTS) {

printf("componet [%d] – memcached_add key[%s] exist\n", i, product_id);

pvalue = memcached_get(memc, product_id, strlen(product_id),

&value_len, &flags, &rc);

if (!pvalue) return -1;

} else if (rc != MEMCACHED_SUCCESS) {

printf("componet [%d] – memcached_add error: %s, [%d]\n",

i, memcached_strerror(memc, rc), rc);

return -1;

} else {

printf("componet [%d] – memcached_add key[%s] successfully,"

" its value = %u, cas = %llu\n",

i,product_id,

value_added, (memc->result).item_cas);

return 0;

}

} else {

printf("componet [%d] – memcached_get error: %s, %d\n",

i, memcached_strerror(memc, rc), rc);

return -1;

}

}

value = atoi(pvalue);

printf("componet [%d] – memcached_get value = %u, cas = %llu\n",

i, value, (memc->result).item_cas);

if (value & mask) {

free(pvalue);

return 1;

} else {

uint64_t cas_value = 0;

cas_value = (memc->result).item_cas;

memset(value_added_str, 0, sizeof(value_added_str));

sprintf(value_added_str, "%d", value_added + value);

rc = memcached_cas(memc, product_id, strlen(product_id),

value_added_str, strlen(value_added_str),

1000, 0, cas_value);

if (rc != MEMCACHED_SUCCESS) {

printf("componet [%d] - memcached_cas error = %d, %s\n",

i, rc, memcached_strerror(memc, rc));

free(pvalue);

} else {

printf("componet [%d] - memcached_cas ok\n", i);

free(pvalue);

if (bit_count(value_added + value) == component_in_total) {

rc = memcached_delete(memc, product_id, strlen(product_id), 0);

if (rc != MEMCACHED_SUCCESS) {

printf("memcached_delete error: %s\n",

memcached_strerror(memc, rc));

return -1;

} else {

printf("memcached_delete key: %s ok\n", product_id);

}

}

return 0;

}

}

getchar();

}

return 0;

}

代码看起来较多，主要是要考虑各种异常情况。

我们可以通过先后启动两个pack_sys来验证程序逻辑的正确性：

窗口1：

$> pack_sys

componet [2] – memcached_get not found product key: [nexus5]

componet [2] – memcached_add key[nexus5] successfully, its value = 2, cas = 0

pack component [2] ok

窗口2：

$> pack_sys

componet [2] – memcached_get value = 2, cas = 54

pack component [2] exists

若两个窗口继续交替执行，一种可能的结果如下：

窗口1：

$> pack_sys

componet [2] – memcached_get not found product key: [nexus5]

componet [2] – memcached_add key[nexus5] successfully, its value = 2, cas = 0

pack component [2] ok

componet [3] – memcached_get value = 2, cas = 54

componet [3] - memcached_cas ok

pack component [3] ok

componet [1] – memcached_get value = 6, cas = 55

componet [1] - memcached_cas ok

pack component [1] ok

componet [2] – memcached_get value = 23, cas = 57

pack component [2] exists

componet [5] – memcached_get not found product key: [nexus5]

componet [5] – memcached_add key[nexus5] successfully, its value = 16, cas = 0

pack component [5] ok

componet [4] – memcached_get value = 16, cas = 59

componet [4] - memcached_cas ok

pack component [4] ok

窗口2：

$> pack_sys

componet [2] – memcached_get value = 2, cas = 54

pack component [2] exists

componet [3] – memcached_get value = 7, cas = 56

pack component [3] exists

componet [1] – memcached_get value = 7, cas = 56

pack component [1] exists

componet [2] – memcached_get value = 7, cas = 56

pack component [2] exists

componet [5] – memcached_get value = 7, cas = 56

componet [5] - memcached_cas ok

pack component [5] ok

componet [4] – memcached_get value = 23, cas = 57

componet [4] - memcached_cas ok

memcached_delete key: nexus5 ok

pack component [4] ok

全部Demo代码已经上传到[github](https://github.com/bigwhite/experiments/tree/master/memcached_cas_examples)上了，感兴趣可以去下载。

**【其它】**

* 我用的是[libmemcached](http://libmemcached.org) 1.0.17版本，memcached 1.4.15版本。

* libmemcached启用cas后，只能在ascii模式下工作，在binary下会得到如下错误，应该是libmemcached的bug；

memcached_cas error, SERVER END, 21

* libmemcached的官方文档中某些内容似乎已经落伍了，与代码的实际行为已经不一致了，参考manual的时候要小心，最好能对着源码看。

* 关于问题调试，可以考虑通过-vv命令行选项打开memcached的详细日志，这样你就可以看到memcached的一举一动，特别是涉及到[binary protocol](http://code.google.com/p/memcached/wiki/MemcacheBinaryProtocol)时，这样调试更有效率。

© 2013, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论