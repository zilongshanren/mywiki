---
tags: [performance, 方法论, 架构, 泛化, 缓存]
date: 2026-04-19
sources: 1
---

# 性能末日的四骑士

[[ben-supnik|Ben Supnik]] 2015-01-31 的续篇，接 [[performance-by-design]]。论点：有**具体可列举**的力量在拖慢程序，而且它们**都在设计早期就已经被决定**——这解释了为什么"先写再 profile"救不回来一个架构错误的系统。

## 适用范围的自我界定

不是所有代码都值得被这套标准衡量。对话框打开花 30 ms 他不在乎。但应用启动时间、编辑器响应延迟、滚动平滑度、游戏里能渲染多少栋楼、音频程序能播多少轨——这类**核心路径**上的性能，确实决定产品质量。四骑士只针对这类核心路径。

## 四骑士

### 1. 冗余工作（Doing Unnecessary Work）

大 O 谈的那类——排序是 O(N²) 还是 O(N log N)——只是这桶里的一小部分。Supnik 举的例子大多**超越算法层面**：

- 表格重绘时去拉整张表的数据，而不是用户能看到的那一段；
- 不 cache 重复计算结果；
- 在 OpenGL 当前状态已满足时仍然设一次冗余状态，触发驱动内部大量 thrash；
- 编辑器批量改对象时每改一个就刷 UI；
- 游戏里的 terrain shading 是 GPU 实时算，还是提前烤到盘上（**"ahead of time"往往是最好的计算时机**）；
- 赛车游戏全地图铺房子 vs 只在赛道附近铺——加载、剔除、渲染全部是冗余。

**能在设计末期修掉吗？不能**——这是算法选型和产品定义的一部分。

### 2. 常数时间低效（Constant-Time Inefficiencies）

即使算法 Big-O 最优，常数因子也能毁一切。Supnik 的具体清单：

- 能放栈/静态/class 里的，不要 malloc；
- `std::map` 在绝大多数场合都不如有序 `std::vector`——map 的 locality 差、`malloc` 无数次；
- 能用 free function / inline 的不要虚函数；
- 能静态转换的不要 `dynamic_cast`；
- 别用 cache-unfriendly 的内存布局。

两条背景：**CPU 与内存的差距在扩大**——L1 hit 3 周期、RAM miss 300 周期，常数因子已经是 100×；**桌面的"不 care"到了 console / mobile 就是灾难**。他承认自己在 Mac Pro 上粗写的代码到 iPhone 4S 就趴下。

痛点不在单点——是**这类慢 idiom 会渗透到 100% 的代码里**。WED（WorldEditor）代码库里 `std::map<string, ...>` 出现 588 次，`std::set<...>` 822 次——近乎整个项目都在用次优 idiom。这不是 hot spot，这是**全局重写级别**的债。

### 3. 不必要的泛化（Unnecessary Generalization）

程序员的职业病：**总是想泛化**。他给的辨识准则："当你选的方案不像手套一样贴合问题形状"。

实例：

- 用"任意多边形与带洞多边形求交"的算法，去做"三角形 vs 轴对齐包围盒裁剪"；
- 写一个"能画任意带颜色/纹理/位置三角形"的通用 draw 函数，让整个应用都走它；
- 为了**简化抽象**而牺牲性能——WorldEditor 不追踪脏区域，任何局部变化都重绘整屏。没人要管脏区域是方便了，但通用形式做了一堆不必要的工作。

**最难修**：一旦抽象落地，大量代码都基于它写。拔出抽象往往意味着**重写**。[[false-abstraction]] 是同一主题的另一侧。

### 4. 复利（Compound Interest）

这是最重要的一条。**性能问题会乘起来**——三个泛化各让你慢 25%，合起来就是慢 2×。

这解释了"先写后 profile"失败的机制：如果慢是**均匀分布的**（所谓 "uniformly slow code"，每个函数都吃 1% CPU），profile 告诉你没有热点，但整体已经跑不动——你得做 100 次分散的优化才能让指针动。这笔钱在设计时几乎免费，在维护期几乎付不起。

他把这条写成："1% fee 在金融里是大事，1% 性能在驱动代码里是大事"——见 [[optimization-leverage-ratio]]。

## Knuth 的原文其实包含了这条

Supnik 引原论文里 Knuth 自己的话：**编译器应该自动反馈每段代码的开销，除非显式关掉**。他的点是——**Knuth 从来没说别管性能；他说的是别在没 profile 的时候瞎调**。但即使照做也不够：**你要按下列顺序设计**——

1. 估数据规模与计算量，选一个能在预算内解的算法；
2. 选能"按预算"实现该算法的编码 idiom；
3. 只加增值的抽象，不加破预算的抽象。

## 相关

- [[performance-by-design]]
- [[pragmatic-performance-philosophy]]
- [[strategic-programming]]
- [[tactical-programming]]
- [[false-abstraction]]
- [[cheat-by-solving-less]]
- [[optimization-leverage-ratio]]
- [[cache-friendliness]]
- [[aos-vs-soa]]
- [[stl-not-abstraction-prescription]]
- [[memory-latency-human-metaphor]]

## Sources

- [[sources/supnik-four-horsemen]]
