---
title: Go map使用Swiss Table重新实现，性能最高提升近50%
url: https://tonybai.com/2024/11/14/go-map-use-swiss-table/
published: '2024-11-14'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go map使用Swiss Table重新实现，性能最高提升近50%

![](../../assets/1e555b18516032e5.png)


[本文永久链接](https://tonybai.com/2024/11/14/go-map-use-swiss-table) – https://tonybai.com/2024/11/14/go-map-use-swiss-table

在[2024月11月5日的Go compiler and runtime meeting notes](https://github.com/golang/go/issues/43930#issuecomment-2458068992)中，我们注意到了一段重要内容，如下图红框所示：

![](../../assets/3a65a5201d5cf62c.png)


这表明，来自字节的一位工程师在两年多前提出的“[使用Swiss table重新实现Go map](https://github.com/golang/go/issues/54766)”的建议即将落地，目前该issue已经被纳入[Go 1.24里程碑](https://github.com/golang/go/milestone/322)。

Swiss Table是由Google工程师于2017年开发的一种高效哈希表实现，旨在优化内存使用和提升性能，解决Google内部代码库中广泛使用的std::unordered_map所面临的性能问题。[Google工程师Matt Kulukundis在2017年CppCon大会上详细介绍了他们在Swiss Table上的工作](https://www.youtube.com/watch?v=ncHmEUmJZf4)：

![](../../assets/b1ffa603d7a8d079.png)


目前，Swiss Table已被应用于多种编程语言，包括[C++ Abseil库的flat_hash_map(可替换std::unordered_map)](https://abseil.io/about/design/swisstables)、[Rust标准库Hashmap的默认实现](https://github.com/rust-lang/hashbrown)等。

Swiss Table的出色表现是字节工程师提出这一问题的直接原因。字节跳动作为国内使用Go语言较为广泛的大厂。据issue描述，Go map的CPU消耗约占服务总体开销的4%。其中，map的插入（mapassign）和访问（mapaccess）操作的CPU消耗几乎是1:1。大家可千万不能小看4%这个数字，以字节、Google这样大厂的体量，减少1%也意味着真金白银的大幅节省。

Swiss Table被视为解决这一问题的潜在方案。字节工程师初版实现的基准测试结果显示，与原实现相比，Swiss Table在查询、插入和删除操作上均提升了20%至50%的性能，尤其是在处理大hashmap时表现尤为突出；迭代性能提升了10%；内存使用减少了0%至25%，并且不再消耗额外内存。

这些显著的性能提升引起了Go编译器和运行时团队的关注，特别是当时负责该子团队的Austin Clements。在经过两年多的实验和评估后，Go团队成员[Michael Pratt](https://github.com/prattmic)基于Swiss Table实现的internal/runtime/maps最终成为Go map的底层默认实现。

在本文中，我们将简单介绍Swiss Table这一高效的哈希表实现算法，并提前看一下Go map的Swiss Table实现。

在进入swiss table工作原理介绍之前，我们先来回顾一下当前Go map的实现(Go 1.23.x)。

## 1. Go map的当前实现

map，也称为映射，或字典，或[哈希表](https://en.wikipedia.org/wiki/Hash_table)，是和数组等一样的最常见的数据结构。实现map有两个关键的考量，一个是哈希函数(hash function)，另一个就是碰撞处理(collision handling)。hash函数是数学家的事情，这里不表。对于碰撞处理，在大学数据结构课程中，老师通常会介绍两种常见的处理方案：

- 开放寻址法(Open Addressing)

在发生哈希碰撞时，尝试在哈希表中寻找下一个可用的位置，如下图所示k3与k1的哈希值发生碰撞后，算法会尝试从k1的位置开始向后找到一个空闲的位置：

![](../../assets/58a6b0248e5ba11c.png)


- 链式哈希法(拉链法, Chaining)

每个哈希桶(bucket)存储一个链表（或其他数据结构），所有哈希值相同的元素(比如k1和k3)都被存储在该链表中。

![](../../assets/386d5f800b811841.png)


Go当前的map实现采用的就是链式哈希，当然是经过优化过的了。要了解Go map的实现，关键把握住下面几点：

- 编译器重写

我们在用户层代码中使用的map操作都会被Go编译器重写为对应的runtime的map操作，就如下面Go团队成员Keith Randall在GopherCon大会上讲解[map实现原理](https://www.youtube.com/watch?v=Tl7mi9QmLns)的一个截图所示：

![](../../assets/5babfa6ffbd7927d.png)


- 链式哈希

前面提过，Go map当前采用的是链式哈希的实现，一个map在内存中的结构大致如下：

![](../../assets/869c5f652a97388d.png)



我们看到，一个map Header代表了一个map类型的实例，map header中存储了有关map的元数据(图中字段与当前实现可能有少许差异，毕竟那是几年前的一个片子了)，如：

```
- len: 当前map中键值对的数量。
- bucket array: 存储数据的bucket数组，可以对比前面的链式哈希的原理图进行理解，不过不同的是，Go map中每个bucket本身就可以存储多个键值对，而不是指向一个键值对的链表。
- hash seed: 用于哈希计算的种子，用于分散数据并提高安全性。
```


通常一个bucket可以存储8个键值对，这些键值对是根据键的哈希值分配到对应的bucket中。

注：在

[《Go语言第一课》]专栏中，有关于Go map工作原理的系统说明，感兴趣的童鞋可以看看。

- 溢出桶(overflow bucket)

每个bucket后面还会有Overflow Bucket。当一个bucket中的数据超出容量时，会创建overflow bucket来存储多余的数据。这样可以避免直接扩展bucket数组，节省内存空间。但如果出现过多的overflow bucket，性能就会下降。

- “蚂蚁搬家”式的扩容

当map中出现过多overflow bucket而导致性能下降时，我们就要考虑map bucket扩容的事儿了，以始终保证map的操作性能在一个合理的范围。是否扩容由一个名为load factor的参数所控制。load factor是元素数量与bucket数量的比值，比值越高，map的读写性能越差。目前Go map采用了一个经验值来确定是否要扩容，即load factor = 6.5。当load factor超过这个值时，就会触发扩容。所谓扩容就是增大bucket数量(当前实现为增大一倍数量)，减少碰撞，让每个bucket中存放的element数量降下来。

扩容需要对存量element做rehash，在元素数量较多的情况下，“一次性”的完成桶的扩容会造成map操作延迟“突增”，无法满足一些业务场景的要求，因此Go map采用“增量”扩容的方式，即在访问和插入数据时，“蚂蚁搬家”式的做点搬移元素的操作，直到所有元素完成搬移。

Go map的当前实现应该可以适合大多数的场合，但依然有一些性能和延迟敏感的业务场景觉得**Go map不够快**，另外一个常被诟病的就是当前实现的桶扩容后就[不再缩容(shrink)了](https://github.com/golang/go/issues/20135)，这会给内存带来压力。

![](../../assets/487c00051cadeebd.png)



下面我们再来看看swiss table的结构和工作原理。

## 2. Swiss table的工作原理

就像前面提到的，Swiss table并非来自某个大学或研究机构的论文，而是来自Google工程师在工程领域的”最佳实践”，因此关于Swiss table的主要资料都来自[Google的开源C++ library Abseil](https://abseil.io/)以及[开发者的演讲视频](https://www.youtube.com/watch?v=ncHmEUmJZf4)。在Abseil库中，它是flat_hash_map、flat_hash_set、node_hash_map以及node_hash_set等数据结构的底层实现，并且[Swiss table的实现在2018年9月正式开源](https://abseil.io/blog/20180927-swisstables)。

和Go map当前实现不同，Swiss table使用的不是拉链法，而是开放寻址，但并非传统的方案。下面是根据公开资源画出的一个Swiss table的逻辑结构图(注意：并非真实内存布局)：

![](../../assets/d448b03181ecc647.png)


如果用一个式子来表示Swiss table，我们可以用：

```
A swiss table = N * (metdata array + slots array)
```


我们看到：swiss table将所谓的桶（这里叫slot）分为多个group，每个group中有16个slot，这也是swiss table的创新，即将开放寻址方法中的probing(探测key碰撞后下一个可用的位置(slot))放到一个16个slot的group中进行，这样的好处是可以通过一个[SIMD指令](https://tonybai.com/2024/07/21/simd-in-go)并行探测16个slot，这种方法也被称为**Group Probing**。

在上图中，我们看到一个Group由metadata和16个slot组成。metadata中存储的是元数据，而slot中存储的是元素(key和value)。Group probling主要是基于metadata实现的，Google工程师的演讲有对group probing实现的细节描述。

当我们向swiss table插入一个元素或是查找一个元素时，swiss table会通过hash函数对key进行求值，结果是一个8字节(64bit)的数。和Go map的当前实现一样，这个哈希值的不同bit功用不同，下图是一个来自abseil官网的示例：

![](../../assets/19f22c8bedbec913.png)


哈希值的高57bit被称为H1，低7bit被称为H2。前者用于标识该元素在Group内的索引，查找和插入时都需要它。后者将被用于该元素的元数据，放在metadata中存储，用于快速的group probing之用，也被称为**哈希指纹**。

每个Group的metadata也是一个16字节数组，每个字节对应一个slot，是该slot的控制字节。这个字节的8个bit位的组成如下：

![](../../assets/a6cf3f25b3f3b672.png)



metadata中的控制字节有三个状态：

- 最高位为1，其余全零为
**空闲状态(Empty)**，即对应的slot尚未曾被任何element占据过； - 最高位为0，后7位为哈希指纹(H2)，为对应的slot当前已经有element占据的
**已使用状态**； - 最高位为1，其他位为1111110的，为对应的slot为
**已删除状态**，后续可以被继续使用。

下面是Abseil开发者演进slide中的一个针对swiss table的迭代逻辑：

![](../../assets/e9caf9f3247a39c8.png)


通过这幅图可以看出H1的作用。不过这里通过pos = pos + 1进行probing（探测）显然是不高效的！metadata之所以设计为如此，并保存了插入元素的哈希指纹就是为了实现高效的probing，下图演示了基于key的hash值的H2指纹通过SIMD指令从16个位置中快速得到匹配的pos的过程：

![](../../assets/2a42e12d39ed7e09.png)


虽然有两个匹配项，但这个过程就像“布隆过滤器”一样，快速排除了不可能的匹配项，减少了不必要的内存访问。

由此也可以看到：swiss table的16个条目的分组大小不是随意选择的，而是基于SSE2寄存器长度(128bit, 16bytes)和现代CPU的缓存行大小(64字节)优化的，保证了一个Group的控制字节能被单次SIMD指令处理。

此外swiss table也是通过load factor来判定是否需要对哈希表进行扩容，一旦扩容，swiss table通常是会将group数量增加一倍，然后重新计算当前所有元素在新groups中的新位置(rehash)，这个过程是有一定开销的。如果不做优化，当表中元素数量较多时，这个过程会导致操作延迟增加。

最后，虽然多数情况是在group内做probing，但当元素插入时，如果当前Group已满，就必须探测到下一个Group，并将元素插入到下一个Group。这样，在该元素的查找操作中，probing也会跨group进行。

到这里，我们已经粗略了解了swiss table的工作原理，那么Go tip对swiss table当前的实现又是怎样的呢？我们下面就来看看。

## 3. Go tip版本当前的实现

Go tip版本基于swiss table的实现在https://github.com/golang/go/blob/master/src/internal/runtime/maps下。

由于Go map是原生类型，且有了第一版实现，考虑到Go1兼容性，新版基于swiss table的实现也要继承已有的语义约束。同时，也要尽量避免swiss table自身的短板，Go团队在swiss table之上做了局部改进。比如为了将扩容带来的开销降到最低，Go引入了多table的设计，以支持渐进式扩容。也就是说一个map实际上是多个swiss table，而不是像上面说的一个map就是一个swiss table。每个table拥有自己的load factor，可以独立扩容(table的扩容是一次性扩容)，这样就可以**将扩容的开销从全部数据变为局部少量数据，减少扩容带来的影响**。

Go swiss-table based map的逻辑结构大致如下：

![](../../assets/17b1e4e3a37ec23f.png)


我们可以看出与C++ swisstable的最直观不同之处除了有多个table外，每个group包含8个slot和一个control word，而不是16个slot。此外，Go使用了二次探测(quadratic probing), 探测序列必须以空slot结束。

为了实现渐进式扩容，数据分散在多个table中；单个table容量有上限(maxTableCapacity)，超过上限时分裂成两个table；使用可扩展哈希(extendible hashing)根据hash高位选择table，且每个table可以独立增长。

Go使用Directory管理多个table，Directory是Table的数组，大小为2^globalDepth。如果globalDepth=2，那Directory最多有4个表，分为0×00、0×01、0×10、0×11。Go通过key的hash值的前globalDepth个bit来选择table。这是一种“extendible hashing”，这是一种动态哈希技术，其核心特点是通过动态调整使用的哈希位数(比如上面提到的globalDepth)来实现渐进式扩容。比如：初始可能只用1位哈希值来区分，需要时可以扩展到用2位，再需要时可以扩展到用3位，以此类推。

举个例子，假设我们用二进制表示哈希值的高位，来看一个渐进式扩容的过程：

- 初始状态 (Global Depth = 1):

```
directory
hash前缀 指向的table
0*** --> table1 (Local Depth = 1)
1*** --> table2 (Local Depth = 1)
```


- 当table1满了需要分裂时，增加一位哈希值 (Global Depth = 2):

```
directory
hash前缀 指向的table
00** --> table3 (Local Depth = 2) // 由table1扩容而成
01** --> table4 (Local Depth = 2) // 由table1扩容而成
10** --> table2 (Local Depth = 1)
11** --> table2 (Local Depth = 1) // 复用table2因为它的Local Depth还是1
```


- 如果table2也满了，需要分裂：

```
directory
hash前缀 指向的table
00** --> table3 (Local Depth = 2)
01** --> table4 (Local Depth = 2)
10** --> table5 (Local Depth = 2) // 由table2扩容而成
11** --> table6 (Local Depth = 2) // 由table2扩容而成
```


通过extendible hashing实现的渐进式扩容，每次只处理一部分数据，扩容过程对其他操作影响小，空间利用更灵活。

对于新版go map实现而言，单个Table达到负载因子阈值时触发Table扩容。当需要分裂的Table的localDepth等于map的globalDepth时触发Directory扩容，这就好理解了。

除此之外，Go版本对small map也有特定优化，比如少量元素(<=8)时直接使用单个group，避免或尽量降低swiss table天生在少量元素情况下的性能回退问题。

更多实现细节，大家可以自行阅读https://github.com/golang/go/blob/master/src/internal/runtime/maps/下的Go源码进行理解。

注：目前swiss table版的go map依然还未最终定型，并且后续还会有各种优化加入，这里只是对当前的实现(2024.11.10)做概略介绍，不代表以后的map实现与上述思路完全一致。


## 4. Benchmark

目前gotip版本中[GOEXPERIMENT=swissmap默认已经打开](https://github.com/golang/go/commit/99d60c24e23d4d97ce51b1ee5660b60a5651693a)，我们直接用gotip版本即可体验基于swiss table实现的map。

字节工程师zhangyunhao的[gomapbench repo](https://github.com/zhangyunhao116/gomapbench)提供了对map的性能基准测试代码，不过这个基准测试太多，我大幅简化了一下，只使用Int64，并只测试了元素个数分别为12、256和8192时的情况。

注：我基于Centos 7.9，使用Go 1.23.0和gotip(devel go1.24-84e58c8 linux/amd64)跑的benchmark。


```
// 在experiments/swiss-table-map/mapbenchmark目录下
$go test -run='^$' -timeout=10h -bench=. -count=10 > origin-map.txt
$GOEXPERIMENT=swissmap gotip test -run='^$' -timeout=10h -bench=. -count=10 > swiss-table-map.txt
$benchstat origin-map.txt swiss-table-map.txt > result.txt
```


注：gotip版本的安装请参考

[《Go语言第一课》]专栏的第3讲。benchstat安装命令为go install golang.org/x/perf/cmd/benchstat@latest

下面是result.txt中的结果：

```
goos: linux
goarch: amd64
pkg: demo
cpu: Intel(R) Xeon(R) Platinum
│ origin-map.txt │ swiss-table-map.txt │
│ sec/op │ sec/op vs base │
MapIter/Int/12-8 179.7n ± 10% 190.6n ± 4% ~ (p=0.436 n=10)
MapIter/Int/256-8 4.328µ ± 5% 3.748µ ± 1% -13.40% (p=0.000 n=10)
MapIter/Int/8192-8 137.3µ ± 1% 123.6µ ± 1% -9.95% (p=0.000 n=10)
MapAccessHit/Int64/12-8 10.12n ± 2% 10.68n ± 14% +5.64% (p=0.000 n=10)
MapAccessHit/Int64/256-8 10.29n ± 3% 11.29n ± 1% +9.77% (p=0.000 n=10)
MapAccessHit/Int64/8192-8 25.99n ± 1% 14.93n ± 1% -42.57% (p=0.000 n=10)
MapAccessMiss/Int64/12-8 12.39n ± 88% 20.99n ± 50% ~ (p=0.669 n=10)
MapAccessMiss/Int64/256-8 13.12n ± 6% 11.34n ± 7% -13.56% (p=0.000 n=10)
MapAccessMiss/Int64/8192-8 15.71n ± 1% 14.03n ± 1% -10.66% (p=0.000 n=10)
MapAssignGrow/Int64/12-8 607.1n ± 2% 622.6n ± 2% +2.54% (p=0.000 n=10)
MapAssignGrow/Int64/256-8 25.98µ ± 3% 23.22µ ± 1% -10.64% (p=0.000 n=10)
MapAssignGrow/Int64/8192-8 792.3µ ± 1% 844.1µ ± 1% +6.54% (p=0.000 n=10)
MapAssignPreAllocate/Int64/12-8 450.2n ± 2% 409.2n ± 1% -9.11% (p=0.000 n=10)
MapAssignPreAllocate/Int64/256-8 10.412µ ± 1% 6.055µ ± 2% -41.84% (p=0.000 n=10)
MapAssignPreAllocate/Int64/8192-8 342.4µ ± 1% 232.6µ ± 2% -32.05% (p=0.000 n=10)
MapAssignReuse/Int64/12-8 374.2n ± 1% 235.4n ± 2% -37.07% (p=0.000 n=10)
MapAssignReuse/Int64/256-8 8.737µ ± 1% 4.716µ ± 4% -46.03% (p=0.000 n=10)
MapAssignReuse/Int64/8192-8 296.4µ ± 1% 181.0µ ± 1% -38.93% (p=0.000 n=10)
geomean 1.159µ 984.2n -15.11%
```


我们看到了除了少数测试项有不足外(比如MapAssignGrow以及一些元素数量少的情况下)，大多数测试项中，新版基于swiss table的map的性能都有大幅提升，有些甚至接近50%！

## 5. 小结

本文探讨了Go语言中的map实现的重塑，即引入Swiss Table这一高效哈希表结构的背景与优势。Swiss Table由Google工程师开发，旨在优化内存使用和提升性能，解决了传统哈希表在高负载情况下的性能瓶颈。通过对比现有的链式哈希实现，Swiss Table展示了在查询、插入和删除操作上显著提高的性能，尤其是在处理大规模数据时。

经过两年多的实验与评估，Go团队决定将Swiss Table作为Go map的底层实现，预计将在[Go 1.24](https://github.com/golang/go/milestone/322)中正式落地。新的实现不仅承继了原有的语义约束，还通过引入多表和渐进式扩容的设计，进一步优化了扩容过程的性能。尽管当前实现仍在完善中，但Swiss Table的引入无疑为Go语言的性能提升提供了新的可能性，并为未来进一步优化奠定了基础。

对于那些因Go引入[自定义iterator](https://tonybai.com/2024/06/24/range-over-func-and-package-iter-in-go-1-23/)而批评Go团队的Gopher来说，这个Go map的重塑无疑会很对他们的胃口。

本文涉及的源码可以在[这里](https://github.com/bigwhite/experiments/tree/master/swiss-table-map)下载。

## 6. 参考资料

[runtime: use SwissTable](https://github.com/golang/go/issues/54766)– https://github.com/golang/go/issues/54766[swiss table benchmark result](https://gist.github.com/aclements/9fb32ac0a287d2ff360f1bc166cdf4b8)– https://gist.github.com/aclements/9fb32ac0a287d2ff360f1bc166cdf4b8[Swisstable, a Quick and Dirty Description](https://faultlore.com/blah/hashbrown-tldr/)– https://faultlore.com/blah/hashbrown-tldr/[Swiss Tables Design Notes](https://abseil.io/about/design/swisstables)– https://abseil.io/about/design/swisstables[Designing a Fast, Efficient, Cache-friendly Hash Table, Step by Step](https://www.youtube.com/watch?v=ncHmEUmJZf4)– https://www.youtube.com/watch?v=ncHmEUmJZf4[Abseil’s Open Source Hashtables: 2 Years In](https://www.youtube.com/watch?v=JZE3_0qvrMg)– https://www.youtube.com/watch?v=JZE3_0qvrMg[Swiss Tables and absl::Hash](https://abseil.io/blog/20180927-swisstables)– https://abseil.io/blog/20180927-swisstables[SwissMap: A smaller, faster Golang Hash Table](https://www.dolthub.com/blog/2023-03-28-swiss-map/)– https://www.dolthub.com/blog/2023-03-28-swiss-map/[What is a Hash Map?](https://www.freecodecamp.org/news/what-is-a-hash-map/)– https://www.freecodecamp.org/news/what-is-a-hash-map/[Inside the Map Implementation](https://www.youtube.com/watch?v=Tl7mi9QmLns)– https://www.youtube.com/watch?v=Tl7mi9QmLns

[Gopher部落知识星球](https://public.zsxq.com/groups/51284458844544)在2024年将继续致力于打造一个高品质的Go语言学习和交流平台。我们将继续提供优质的Go技术文章首发和阅读体验。同时，我们也会加强代码质量和最佳实践的分享，包括如何编写简洁、可读、可测试的Go代码。此外，我们还会加强星友之间的交流和互动。欢迎大家踊跃提问，分享心得，讨论技术。我会在第一时间进行解答和交流。我衷心希望Gopher部落可以成为大家学习、进步、交流的港湾。让我相聚在Gopher部落，享受coding的快乐! 欢迎大家踊跃加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻) – https://gopherdaily.tonybai.com

我的联系方式：

- 微博(暂不可用)：https://weibo.com/bigwhite20xx
- 微博2：https://weibo.com/u/6484441286
- 博客：tonybai.com
- github: https://github.com/bigwhite
- Gopher Daily归档 – https://github.com/bigwhite/gopherdaily
- Gopher Daily Feed订阅 – https://gopherdaily.tonybai.com/feed

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2024, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

Go 标准库也有新实现的 NewHashTrieMap ，好像将来要替代 sync.Map，请老师也比对一下

https://github.com/golang/go/issues/67009 这个么？我看标记为not planned并被close了

是这个 https://github.com/golang/go/commits?author=mknyszek

也就是这个 https://github.com/golang/go/blob/master/src/internal/sync/hashtriemap.go

这个目前看是给unique包内部用的。虽然提及“can be used elsewhere as well”，但至少目前没看到有proposal说要用其换掉sync.Map的内部实现呢。

https://github.com/golang/go/commit/aecb8faa91e2b40e3651ee93c8e70635ed367677 这个提交不是替换原始的 sync.Map 吗

的确如你所说。不过，这个commit没有任何issue对应，似乎是runtime组自己的一个优化，且目前依然是experiment。看来我对hashtriemap的理解有误。以前sync.Map用的就很少，关注的也不多。

go 1.24中的确可以使用GOEXPERIMENT=synchashtriemap 开启基于hashtriemap的更快的sync.Map https://go.dev/cl/608335

是啊，之前没有任何讨论，就决定替换掉了原来的实现

不过今天发现，上星期提交者也开了 issue: https://github.com/golang/go/issues/70683

当然，代码已经提交，这个也就关掉了

有些时候compiler&runtime组是这样的，之前我也是完全不知道这事儿。

此外trie这种结构也叫prefix tree，hash trie更适合高效的前缀查找，比如下面场景：

- 自动补全：在输入时根据前缀快速查找可能的选项。

- 字典实现：用于高效的单词查找和存储。

- 路由表：在网络中管理路由信息。

但可能不适合作为通用hash map的实现。

我们看到：swiss table将所谓的桶（这里叫slot）分为多个group，每个group中有16个slot，这也是swiss table的创新，即将开放寻址方法中的probing(探测key碰撞后下一个可用的位置(slot))放到一个16个slot的group中进行，这样的好处是可以通过一个SIMD指令并行探测16个slot，这种方法也被称为Group Probing。

不是 8 个 slot 吗？

https://go.dev/blog/swisstable

是的，go的实现没有是16个slot，而是用了8个slot。google原生发布swiss table算法时默认应该是16 slot。Abseil C++ library采用的应该是16-slot的实现。