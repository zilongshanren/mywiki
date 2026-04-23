---
tags: [source, bitsquid, c++, api-design]
date: 2026-04-19
sources: 1
---

# PIMPL vs Pure Virtual Interfaces（Niklas / Bitsquid）

[[niklas-frykholm]] 2012 年 3 月 21 日对 C++ 里三种"接口-实现分离"写法的横向评测，最终定调他个人偏好**在头文件里写纯虚抽象类**。

## 摘要

文章先摆出分离的三条动机：隐藏实现、减头文件依赖、降低接口/实现耦合。C 版本用 forward-declared struct + 自由函数实现；C++ 的主流教学是 PIMPL——`_impl` 指针 + 一堆方法转发 stub；Niklas 推荐的第三种方式是把类写成纯虚抽象基类，在 `.cpp` 里派生实现、配合 `make / destroy` 工厂。对比下来 PIMPL 的优势——能 `new`、能栈分配、能实现继承——在 Bitsquid 的实际用法里都不成立：所有这类对象都是大型系统对象、走自定义 allocator、拒绝实现继承。Niklas 的判据变成了**谁少写样板 + 谁更容易加 helper 方法**，两项都指向纯虚。

文章另一条副线：批量化 API（`set_sound_positions` 而非 `set_sound_position`）让虚函数开销可以忽略，同时利好 DMA 和并行。结尾给 C 一个感叹——"每年我越来越欣赏 C，越来越被 C++ 打击"。

## 关键要点

- PIMPL 的"通用灵活性"在 Bitsquid 场景下全部失效，只剩下一堆转发 stub。
- 纯虚抽象基类省掉 `.h` / `.cpp` 同步义务，加私有 helper 不用先声明。
- **每一行代码都是债务**——样板代码的真实成本是让代码分解粒度变粗。
- 批量化 API 与虚函数隔离天然配合：一次虚调分摊到一批数据。

## 链接到的概念

- [[pimpl-vs-pure-virtual]]
- [[c-opaque-struct-modules]]
- [[interface-vs-implementation]]
- [[api-fast-path-design]]
- [[niklas-frykholm]]

## 原文

- 链接：https://bitsquid.blogspot.com/2012/03/pimpl-vs-pure-virtual-interfaces.html
- 本地：`raw/articles/bitsquid.blogspot.com/2012-03-21_pimpl-vs-pure-virtual-interfaces.md`
