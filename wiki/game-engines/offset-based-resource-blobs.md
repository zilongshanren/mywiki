---
tags: [游戏引擎, 序列化, 数据导向设计, 资源管理, bitsquid]
date: 2026-04-19
sources: 1
---

# 用 offset 替代 pointer patching 的 blob 资源

把一份资源（粒子定义、动画、材质参数表……）压成**一整块连续字节**，一次磁盘读取、DMA 友好、cache 友好——这是"blob"式资源的吸引力。[[niklas-frykholm|Niklas Frykholm]] 2010 年这篇《The Blob and I》回顾了自己过去在 C++ 引擎里用的 `placement new + pointer patching` 方案，然后转向了一个更朴素的做法：**不要 pointer，只要 offset**。

## 传统方案：placement new + pointer patching

经典 C++ blob 的流程是：

1. 保存时，把 blob 里所有对象按顺序摊开，指针字段全部转成"从 blob 起始的 offset"；
2. 把整块字节写盘；
3. 读取时，整块字节读回内存，对根对象做 `new (blob) A(blob)`——一个特殊构造函数；
4. 这个特殊构造函数做三件事：
   - 由编译器在 placement new 里**重建 vtable 指针**（因为写盘时存的 vtable 指针在运行时无效）；
   - 把自己字段里的 offset **加回 base 地址**，变回合法 pointer；
   - 对每个"子对象"也递归地 `new` 一遍，让它们的 vtable 同样被修复。

这套能工作，而且"用了 vtable + placement new + 偏移"带来"Gods that walk the earth"的智力成就感。但现实里它有一堆坑：

- **基类指针必须存真实类型**，否则 placement new 不知道要构造哪个派生类；
- **std::vector、std::map 等标准容器全部不能用**——它们假设指针是真指针；
- **序列化顺序 = 深度优先遍历**，一旦你的访问顺序不是深度优先，仍然在 cache 里跳；想改顺序要改全世界；
- 所有类被绑架成"serialization-aware"——加一个 `save()`、一个特殊构造函数，**整个 code base 都依赖序列化系统**。

## Bitsquid 的方案：不要 pointer，只有 offset

Bitsquid 的资源是 **data-centric** 而非 class-centric——数据结构先设计、按访问模式摊平、然后才写对它操作的函数。class / virtual function 只用在更高层的 system 里，不入资源结构。这么一来：

- 资源里全是 **POD struct**，没有 vtable，不需要 placement new，**直接 `fread` 到内存就能用**；
- 指针的"定位"问题用一个极简的约定解决：**资源里不存 pointer，全部存 offset**。

访问时做一次 offset + base 的加法：

```c
int get_array_item(int_array *a, size_t i) {
    int *start = (int*)((char*)a + sizeof(int_array));
    return start[i];
}
```

有人会觉得"多一次加法是不是慢了"——Frykholm 的反驳是：**如果你频繁做这个加法以至于能测到开销，说明你在 blob 里疯狂跳——那个跳才是真正的性能问题。**

## 好处一览

- blob 在内存里可以**自由移动、复制、拼接**（和另一个 blob 合并成更大的），因为所有"指针"都是相对的；
- **磁盘 / 内存完全同构**，单次 `read` / `write` 就能整块搬；
- **没有 serialization framework**——因为根本不需要 patching pass。引擎别的子系统也不需要知道你的数据怎么存；
- 跨资源引用用**资源名的 hash**而不是 pointer——runtime 里由 [[handle-based-resource-manager|资源管理器]] 按 hash 解析成 pointer，存在动态数据侧。

## 变长数组的约定

评论里有人问怎么处理动态数组。Bitsquid 用 header + trailing bytes 的做法：

```c
struct int_array { size_t num_ints; };  // 后面紧跟 num_ints 个 int
```

"blob 是只读 runtime 数据"的前提让它不需要 grow/shrink，这个约定就够用了。离线 data compile 时想生成多长就多长。

## 平台差异怎么办

Bitsquid 把 runtime blob 做成**平台相关**，所有 blob 都在 Win32 上**交叉编译**（见 [[decoupled-tool-engine-json-rpc]]）：

- **byte-order**：cross-compiler 在写 blob 时做 endian swap，目标平台读的时候不用处理；
- **alignment**：按所有目标平台里最严格的那个对齐 blob，读取端 `malloc` 时也保证同样对齐。

这让 runtime 端的代码最简单——一次 read，一个指针 cast，直接用。

## 和数据导向设计的关系

这篇是 Bitsquid 把 [[data-driven-architecture|data-driven]] / 数据导向设计贯彻到资源层的具体体现：**设计数据的排布**而不是设计类的继承，结果是更简单、更快、更模块化、跨系统更解耦。Bitsquid 后来的 entity system、粒子系统、动画系统都沿用这条路。

## Sources
- [[sources/bitsquid-the-blob-and-i]]
- [[sources/bitsquid-visual-scripting-data-oriented]] — Flow graph blob 是同一思路在脚本 runtime 的应用
- [[sources/bitsquid-entity-system-part4-resources]] —— ECS Part 4：blob 思路在 entity resource 上的具体应用（按 component 类型分组 + offset 查找）
