---
tags: [游戏引擎, 内存分配, SoA, 数据导向设计, bitsquid, cache]
date: 2026-04-19
sources: 1
---

# DataComponent：八步把 STL 怪兽压成单 buffer

[[niklas-frykholm|Niklas Frykholm]] 2015 年《Allocation Adventures 1》是一份可逐步对照的**数据布局改造笔记**——把一个"存任意小段动态数据"的 `DataComponent` 从 `std::map<std::string, std::vector<std::string>>` 风格的递归 STL 怪兽，一步步压缩成**一次 allocation 即装下所有动态数据**的单 buffer 结构。适合任何"小而杂的动态数据"类 component。

## 设计目标

两条总目标，和 [[bitsquid-data-oriented-entity-system|Bitsquid ECS]] 的 SoA 思路一脉相承：

- **线性访问内存**——[[cache-friendliness|cache 友好]] 的根本；
- **最小化 allocation 数**——碎片少、profile 好做、可随意 memcpy 整搬、无需 pointer patching。

对静态资源 [[offset-based-resource-blobs|blob 方法]] 轻松达到两者；动态数据就是本文挑战。

## 八步重构

**用例**：character sheet、status effect 之类小而零碎的数据，JSON 子集限制到 **bool / float / string / object / number-array** 五种——string 和 number-array 视作 monolithic 不可嵌套；这个限制让"所有操作归约成对 object key 赋值"，合并语义简单可推理。

### 1. Hash key

`std::map<unsigned, DataValue>`——32 位够用（key 数量预期小），省 string 比较与每个 string 的 alloc。

### 2. Flatten 树到一维

放弃"枚举一个 object 下全部 key"的能力，把 `stats.health` 合成 key 一次性 hash（注意：**每段分别 hash 再合并**，不能直接 hash `"stats.health"`——否则含 `"."` 的 key 会冲突）。整个 DataComponent 可以退化成 `std::vector<Entry>`，线性扫描对小数据比 `std::map` 还快。

### 3. AoS → SoA

`Entry { key; type; value }` 拆成三条并行 vector：`keys[] / types[] / values[]`。搜索 key 时 **只把 `keys[]` 灌 cache**——省掉无关字节。

### 4. Co-allocate 三条 vector

三条 vector 用**一个 buffer**，共享同一对 `capacity / size`——从三次 alloc 变成一次：

```
-----------------------------------
buffer | keys | types | values |
-----------------------------------
```

```c
char *buffer = allocate(capacity * (sizeof(unsigned) + sizeof(DataType) + sizeof(Value)));
keys   = (unsigned *)buffer;
types  = (DataType *)(keys + capacity);
values = (Value *)(types + capacity);
```

### 5. 去掉 STL

union 里的 `std::string*` / `std::vector<float>*` 换成手写 `{char* data}` 和 `{int capacity, size; float* data}`。`Value` 先从 64 bit 膨到 128 bit——暂时退步。

### 6. Value buffer

所有 string 和 number-array 放进一条**共享 value buffer**：

```
-------------------------------------------------------------
| "hello" | [0 1 3] | "mana" | [0 2] | ... unused space ... |
-------------------------------------------------------------
```

要长大的 value 去顶端分新坑位、旧位置留洞。小规模下不做 defrag；buffer 满了的 realloc 顺手就把洞挤掉。

### 7. Offset + size 替指针

value 引用改成 `{uint16_t offset; uint16_t size}`——64K 对小 component 足够，省内存又**让 buffer 可自由搬**（无需 pointer patching）。`Value` 瘦回 32 bit。

### 8. Header + Value 合流 + 反向生长

header（keys/types/values 元信息）从 buffer **bottom-up**、value buffer 从 **top-down**——**共享中间 free space**：

```
----------------------------------------------------------
| Header | ........ free space ........ | Values |
----------------------------------------------------------
```

谁先撑不住谁触发 realloc。此时整个 DataComponent 仅持**一块 buffer**——可 `memcpy` 整搬、无需 serialize/deserialize、直接落盘再直接读回。

## 关键 insight

- **"去 STL 不是 regression"**：STL 为通用性优化，但这里我们知道"每个 DataComponent 小、access 模式明确"，自己手写能更简单更快；
- **offset 代替 pointer 是多次登场的工具**——blob 资源、value buffer 内引用，都是同一手法；
- **双向生长是可爱的小技巧**：header + value 共 free space，用光决定 realloc 点；
- **指针算术不是智力表演**——作者说"写错会轰轰烈烈地崩，不会阴险微错"，所以可接受；
- **讨论者问"alignment 怎么办、要不要做通用模板类？"** —— Niklas 明确反对"完美库类"（如 6 个 bool trait 的 Singleton monster），偏好 **"hackable" 的简明代码**：今天加 "跳过初始化"，明天加"复用 slot"……与其在模板里卷不如保持易改。

## 留下的问题：1000 个 DataComponent 怎么办

每个 DataComponent 装下单 buffer 很美，但 **1000 个 entity 各挂一个小 DataComponent** 就是 1000 次 alloc。"Where there is one, there are many"要再推一步——让 N 个动态变长的对象**共用一块大 buffer**。这就是 [[arrays-of-arrays-allocation|Part 2 的"数组的数组"问题]]。

## 相关

- [[arrays-of-arrays-allocation]] — Part 2 接上去解决 N 个 component 的共存
- [[offset-based-resource-blobs]] — 静态资源版本的同手法
- [[aos-vs-soa]] — SoA 在 memory-bound 下的 18% 经验优势
- [[bitsquid-data-oriented-entity-system]] — Bitsquid ECS 里 component manager 的默认 SoA 布局
- [[linear-allocator]]
- [[custom-allocator-interface]] — Bitsquid Allocator 抽象接口
- [[cache-friendliness]]

## Sources

- [[sources/bitsquid-allocation-adventures-1-datacomponent]]
