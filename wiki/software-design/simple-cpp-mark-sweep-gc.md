---
tags: [软件设计, C++, 垃圾回收, 生命期管理]
date: 2026-04-14
sources: 1
---

# 极简 C++ 标记清除 GC

云风 2010 年春节写了一个不到 200 行的 C++ GC 玩具。目的是给引擎的 C++ 中间层补上 GC——因为底层是 C + Lua，原本靠 Lua 的 GC 托管 C 对象生命期，当把中间层搬到 C++ / Qt 时就缺少了这一层。这篇笔记很有代表性地展现了他的工程趣味：**不用模板魔术、接口和实现分离、最低功能集、代码短到一眼能读懂。**

## 需求

- 标记清除，而非引用计数——因为要解决**循环引用**。
- 实现比引用计数复杂不了太多，性能相当或更好。
- 接口/实现尽量分离，但不强求做成 COM 式的 ABI。
- 使用尽量简单，会用即可，易读易扩展。

## 对象模型

两个纯虚接口：

```cpp
interface i_gcobject {
    virtual ~i_gcobject() {}
    virtual void touch() {}          // 供 mark 回调——遍历子引用
    virtual void mark()    = 0;      // 打标记
    virtual void grab()    = 0;      // 挂到 root
    virtual void release() = 0;      // 从 root 摘下
    static  void collect();          // 触发一次 mark-sweep
};

interface i_gcholder : virtual i_gcobject {
    virtual void hold  (i_gcobject *) = 0;
    virtual void unhold(i_gcobject *) = 0;
    static  i_gcholder* create();
};
```

`gcobject` 是默认实现：一个 `bool marked` 字段 + 全局 `gc_pool` 容器登记所有存活对象。标记位采用"乒乓开关"——每次 `collect` 切换 `gc_trigger` 的值，省去了遍历清零的开销。

`gcholder` 是 root，持有一组"必须存活的对象"，提供 `hold/unhold`。内部用两个待处理 set（`hold_set` / `unhold_set`）延迟合并，避免每次抓放都立即打扰核心结构。

## 派生自定义对象的写法

实现者的心智负担被压到最小：

1. 先定义业务接口（如 `i_tree`），虚继承 `i_gcobject`。
2. 实现类虚继承 `gcobject` 和 `i_tree`。
3. 如果自己持有其他 gc 对象，重载 `touch()`，在里面对所有子引用调 `mark()`。
4. 析构函数可以写（相当于 finalize），但**不要**在里面释放相关 gc 对象——让 GC 自己收。

示例 `tree` 节点在 `touch()` 里同时 `mark` parent 和所有 children，双向引用由 GC 自然处理。

## 关键细节

- **mark 乒乓位**：`collect()` 结束时翻转 `gc_trigger`，下一轮老的标记就等效为未标记。不需要 pre-pass 清零。
- **root 之外的 collect**：`collect` 从 root 开始 mark，再用 `remove_if` + `f_unmarked` 一次性清理 `gc_pool` 中未标记的对象并 `delete`。
- **hold/unhold 延迟合并**：两个无序数组在 `touch()` 首次被调用时才合并去重，避免每次操作都触发排序。
- **多级 holder 理论上支持**，但云风指出对于有主循环的程序没必要——在循环末尾 collect 就够，在调用栈深处 collect 反而会让临时对象来不及被晚些时候产生的引用捡回。

## 设计取舍

这个玩具刻意避开了模板和 CRTP：云风不喜欢用"苦力或高智慧结晶堆出来的代码"。接口虚函数足够表达语义，`static` 在接口上做为工厂入口，避免调用者接触到 `gcobject` 的具体细节——只有实现方才 `#include "gcobject.h"`。这正是 [[information-hiding]] 的 C++ 体现。

相比之下，现代 C++ 里更常见的做法是用 `shared_ptr` + `weak_ptr`，但那解决不了循环引用而不泄漏的根本问题；云风选择跟 Lua、Java 同路的 tracing GC，是把"生命期语义"从 RAII 的确定性世界里解耦出去——和他在 [[c-interface-oop]] 里强调的"生命期独立管理"是一致的哲学。

## 相关

- [[information-hiding]]
- [[interface-vs-implementation]]
- [[garbage-collector]]
- [[c-interface-oop]]
- [[cloudwu]]

## Sources

- [[sources/cloudwu-cpp-mark-sweep-gc]]
