---
tags: [source, 游戏引擎, 内存分配, SoA, 数据导向设计, bitsquid]
date: 2026-04-19
sources: 1
---

# Allocation Adventures 1: The DataComponent（Niklas Frykholm / Bitsquid）

[[niklas-frykholm]] 2015 年 6 月 12 日第一篇"分配冒险"——把一个存 JSON 子集的 `DataComponent` **从 STL 递归容器一步步压成单块 buffer**。完整展示了从 `std::map<std::string, std::vector<std::string>>` 这种"怪兽"蜕变到**一个 allocation 就装下所有动态数据**的八步变换。

## 摘要

low-level 系统设计先定 data layout，两条总目标：**线性访问** + **最小化 allocation 数**。前者是 [[cache-friendliness|cache 友好]] 的根本，后者带来更少碎片、更易 profile、更容易搬/复制（无需 pointer patching）、更 *neat*。静态资源靠 [[offset-based-resource-blobs|blob 方法]] 轻松达到两者；动态数据就是本文主题。

DataComponent 是 Bitsquid entity system 里"塞任意小段动态数据"的坑位——典型用法是存 character sheet `{name, stats.{health, mana}, status_effects.{drunk, delirious}}`。作者限制 JSON 子集到 **bool/float/string/object/number-array** 五种，string 和 number-array 视为 monolithic 不可嵌套——这个限制让所有操作可规约成"对 object key 赋值"，让 collaborative merge 易推理。

然后八步重构：**(1)** key 做 hash，`std::map<unsigned, DataValue>`——省串比较、省 alloc。**(2)** 放弃"枚举一个 object 下全部 key"的能力，把整棵树 flatten 成一维，hash 各段后再一起 hash（避免 `"."` 导致的碰撞）——整个 DataComponent 可存 `std::vector<Entry>`，线性查找比 `std::map` 快。**(3)** AoS → **SoA**：key/type/value 各自一条 `vector`，搜索时只把 key 数组灌 cache。**(4)** 把三条 vector co-allocate 到**一个 buffer**，共享 capacity/size。**(5)** 去掉 STL，手写 `{char* data}` 和 `{int capacity,size; float* data}`——`Value` union 膨胀到 128 bit，是阶段回退。**(6)** 所有 string / float array 走一条**共享 value buffer**——value 长度变则顶上分新坑位（留洞），再 realloc 顺便 defrag。**(7)** 用 16-bit offset + 16-bit size 替换指针，`Value` 瘦回 32 bit——一共占 64K 对小 component 足够。**(8)** header buffer 和 value buffer 合并：header **bottom-up**、value **top-down**、共享中间 free space——两边谁先撑不住谁触发 realloc。

留下的尾巴：上面都是**单个** DataComponent 用一块 buffer。但"一个千 entity、每个挂一个小 DataComponent"就是一千次 alloc——这是 Part 2 要解决的"数组的数组"问题。

## 关键要点

- 两条总目标：线性访问 + 最少 allocation
- 限制 JSON 到 bool/float/string/object/number-array，string 和 array monolithic——让 merge 好推理
- hash key 代替 string key——省比较、省 alloc
- flatten 树到一维平铺，放弃按父 key 枚举子 key
- AoS → SoA：搜索 key 时只 cache key 数组
- 三条 vector co-allocate 到单 buffer，共享 capacity/size
- 去 STL：`Value` union 先膨到 128 bit，再靠 offset+size 瘦回 32 bit
- **bump-style value buffer**：长度变就占新坑位留洞，realloc 顺手 defrag
- header bottom-up + value top-down **共享中间 free space**——单 realloc 决定点
- 指针算术像血压——但一次写对之后错误"会崩得很惨不会阴微"
- 结论：单 buffer 结构可 memcpy 整搬、无需 serialization 代码
- 留"数组的数组"问题给 Part 2：1000 个 component 仍是 1000 次 alloc

## 链接到的概念

- [[datacomponent-single-buffer-allocation]]
- [[offset-based-resource-blobs]]
- [[aos-vs-soa]]
- [[bitsquid-data-oriented-entity-system]]
- [[linear-allocator]]
- [[custom-allocator-interface]]
- [[cache-friendliness]]

## 原文

- 链接：https://bitsquid.blogspot.com/2015/06/allocation-adventures-1-datacomponent.html
- 本地：`raw/articles/bitsquid.blogspot.com/2015-06-12_allocation-adventures-1-the-datacomponent.md`
