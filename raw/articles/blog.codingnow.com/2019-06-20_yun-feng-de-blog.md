---
title: 云风的 BLOG
url: https://blog.codingnow.com/2019/06/
published: '2019-06-20'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

### 字符串比较用 id 管理策略

前两天写了 [快速字符串对象比较](https://blog.codingnow.com/2019/06/string_comparison.html) ，我把这个想法提交到 Lua 的邮件列表，建议 Lua 的未来版本去掉长短字符串，不做 string interning ，用这个方法解决字符串比较的性能问题。Lua 的主要维护者 Reberbo 表示了兴趣，同时也提出了几点问题。

其中一个问题是，Lua 未必运行在 64bit 平台上，所以并没有直接使用 64bit 整数类型。而如果使用 32bit id 就无法简单的通过自增来保证 id 永远唯一。

我就这个问题考虑了几天，提了好几个解决方案，其中一个方案我最为满意，在这里重新用中文记录一下。

我们可以把 32bit id 分为两个区，0 到 0x7fffffff 为 old 区，0x80000000 到 0xffffffff 为 young 区。

一开始，id 从 0x80000000 开始分配，所有的新增字符串都属于 young 。

每次 GC ，在 sweep 阶段，把所有的 young id 重新分配到 old 区。这样，每轮只改变当轮新增的 id 。由于 gc 是分步进行的，sweep 过程也可能新增 id ，所以在 sweep 阶段开始时，让新增 id 直接放在 old 区，也就是说， sweep 阶段只会把 id 从 young 变成 old ，或直接增加 old ，不会产生新的 young id 。

sweep 结束后，再把新增 id 重新调回 0x80000000 。

在比较字符串时，如果字符串值相同，但 id 不同，把较大的 id 变成较小的那个。这样，如果两个 id 一个是 young 一个是 old ，young id 也会变成 old id 。

在这个算法下，old id 的自增速度就会大大的减慢。因为：一轮 gc 中，临时字符串会被回收掉，不占用 old id 的空间；比较过程很有可能把新增的 young id 变成 old id ，不会等到 sweep 阶段再分配新的 old id 。

如果 old id 快用完了，这种情况虽然罕见，但出现了还是有方法的。一个确保方案是用一个原子过程，遍历所有的字符串，把所有的 old id 重新排列到 young 区。因为 old 区全部空出来了，这样上面正常的 gc 流程又能正确工作了。