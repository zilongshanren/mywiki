---
tags: [source, 计算机系统, 内存管理, 调试, C]
date: 2026-04-14
sources: 1
---

# 再谈模块接口设计：给 malloc 加壳（云风 / blog.codingnow.com）

[[cloudwu]] 发表于 2010 年 5 月的博客，用"给 malloc 加壳"作例子，阐述他关于接口设计的一贯立场：**不要指望文档和教诲让别人正确使用你的模块——接口设计得不好就重新设计，实在不行就加一层壳让错误尽早暴露**。

## 摘要

云风点名 C 标准的 `malloc / free / realloc` 作为例子：看似理所当然，却藏着一串坑——双重释放、泄漏、没初始化就读、越界、分配失败漏检、`realloc` 扩容失败时原指针还得自己释放（FreeBSD 为此另加了 `reallocf`）。他的处理是**收紧 API 语义**（断言分配永不失败、`malloc(0) == malloc(1)`、默认用 `0xCC` 填充便于崩得早）和**加狗牌 cookie**（头尾各放 magic number 以检测双重释放和尾部越界；把头狗牌**避开** cookie 第一字段以免被 freelist next 指针覆盖）。为了定位源码，他用一个小巧的宏技巧——`#define malloc malloc_proxy(__FILE__, __LINE__)`，让 `malloc_proxy` 返回函数指针而不是直接调用，这样 `func_ptr = malloc;` 这种赋值写法也能正确工作。泄漏检测方面把"一次性分配"和"真正动态分配"分开：前者打特殊 tag，任何 `free` 都 assert 错误，进程退出由 OS 收；后者串成双向链表在退出时扫描。全文的最终立论：给内存管理模块加壳是成本最低的 [[information-hiding]]——上层代码不改一行用法就自动得到保护。

## 关键要点

- "怪自己没设计好，不要怪使用者用错"。
- `assert` 分配永不失败——在内存预算可控的项目里能简化大量调用代码。
- `malloc(0) → malloc(1)`、默认填 `0xCC`（x86 的 `int3`）。
- 狗牌放 cookie 第二字段以避开 freelist next 指针覆盖。
- `__FILE__ / __LINE__` 经宏 + 全局变量旁路传递，不改 `my_malloc` 签名。
- `#define malloc malloc_proxy(...)` 返回函数指针，让 `func_ptr = malloc;` 仍合法。
- 一次性分配 vs 动态分配分类，简化泄漏检测的信噪比。

## 链接到的概念

- [[malloc-wrapper-debug]]
- [[information-hiding]]
- [[interface-vs-implementation]]
- [[virtual-memory]]
- [[linear-allocator]]
- [[cloudwu]]

## 原文

- 链接：https://blog.codingnow.com/2010/05/
- 本地：`raw/articles/blog.codingnow.com/2010-05-27_yun-feng-de-blog.md`
