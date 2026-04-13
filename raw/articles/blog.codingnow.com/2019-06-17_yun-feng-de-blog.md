---
title: 云风的 BLOG
url: https://blog.codingnow.com/2019/06/string_comparison.html
published: '2019-06-17'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

### 快速字符串对象比较

这段时间在想办法解决多个 lua 虚拟机间共享对象的问题。这里的一个核心问题是，lua 的短字符串做了 interning ，虚拟机在比较两个字符串时只需要比较字符串对象指针即可。而多个 lua vm 如果想共享数据，必须解决这个问题。前段时间实现的 [并发 Hash Map](https://blog.codingnow.com/2019/04/concurrent_hash_map.html) ，和 [共享表](https://blog.codingnow.com/2019/04/share_table.html) 就是在这方面做的努力。

随着 lua 5.4 的临近，我最近尝试了在 lua 5.4 的 alpha 版上做类似的 patch 。但是 lua 5.4 对 gc 的修改极大，这让我尝试去找其它的办法来做这件事。

我觉得，如果允许 vm 在处理短字符串比较时，不严格遵守 interning 的约定，那么就不再需要对 gc 流程做改造了。这样，从外部共享来的字符串，只要做全量值比较，依然可以得到正确的结果。

这样的修改固然对 lua 的代码影响极小，但很可能会有很大的性能损失。毕竟，字符串比较从原来的 O(1) 一次指针比较，变成了复杂得多的 memcmp O(n) 。而这明显是 vm 的性能瓶颈所在。

我首先想的是把 lua 字符串对象 TString 从一个连续结构体改造成包含一个指针的间接引用。也就是说 TString 里不再直接包含字符串数据，而引用另一块数据块。如果首次比较两个 TString ，我们可以先比较内部的数据指针，不同的话再进一步比较数据内容。如果数据内容相同，就把两个内部指针合并成同一个。下次比较就可以通过比较指针完成。

但是，在多线程环境下，简单的引用计数却很难管理好这个内部数据块指针的生命期。我想了很久的无锁算法，感觉无解。可如果加锁，损失的性能或许更大，甚至大于直接比较短字符串的内存（毕竟最多才 40 字节）。

今天，我突然想到另一个巧妙地方法，非常值得一提。

我们可以给每个 TString 对象增加一个 64bit id 。一般情况下，这个 id 都是 0 。当我们需要把一个字符串共享出去时，则用简单的原子自增的方式分配一个唯一 id 给它。由于 id 有 64bit 所以不需要考虑 id 用完的情况。

当我们比较两个 TString 时，先比较 id 是否相同。如果 id 不同，再用 memcmp 做全量比较，如果最终结果相同，我们就把 id 较小的那个 TString 的 id 修改成较大的那个。

如果 id 相同，则可以认为两个 TString 的值相同，不需要进一步做 memcmp。

比如，在 A B 两个虚拟机中，都有字符串 "foo" ，它们都把自己共享出去。一开始 A 中的 foo id 为 1 ，B 中的 foo id 为 2 。

在 C 这个虚拟机中，一开始也有字符串 foo ，id 为 0 。当我们第一次将 C 本地的 foo 和 A 引入的 foo 比较后，C 的 foo 的 id 会修改为 1 。再次比较就不再需要 memcmp 。如果其后和 B 引入的 foo 比较，本地的 foo 的 id 会变成 2 ，再次遇到 A 的 foo ，则会把 A 的 id 也提升为 2 。

即使 A B 共享的 foo 在多线程下，被不同的虚拟机共享，也不需要加锁，因为 id 永远是向上提升，最终都会稳定下来。而且这个 id 仅仅是作为一个比较的参考而已。

通常这个方法，值相同的对象，在经过第一次比较后，以后的每次比较都可以通过一个 id 比较得到结果；值不同的对象，它们的 hash 值也几乎不可能相同，所以再后续的 hash 值比较中也能得到结果。

## Comments

Posted by: A | (9) July 23, 2019 10:34 AM

Posted by: A | (8) July 23, 2019 10:29 AM

Posted by: cat | (7) June 26, 2019 08:58 AM

Posted by: wks | (6) June 25, 2019 09:18 PM

Posted by: Cloud | (5) June 18, 2019 02:38 PM

Posted by: resty | (4) June 18, 2019 12:04 PM

Posted by: dwing | (3) June 18, 2019 11:12 AM

Posted by: threezhiwang | (2) June 18, 2019 10:11 AM

Posted by: joe wulf | (1) June 18, 2019 12:46 AM