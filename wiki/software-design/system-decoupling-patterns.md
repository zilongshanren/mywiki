---
tags: [系统设计, 耦合, 模块化, 引擎架构, bitsquid]
date: 2026-04-19
sources: 1
---

# 引擎里的解耦四条（Managing Coupling）

[[niklas-frykholm|Niklas Frykholm]] 2011 年 Bitsquid Blog《Managing Coupling》系列第一篇。中心论断一句话：**维持一个大型复杂引擎的神志清醒，唯一办法是把它视作许多更小、更简单的系统的集合；而这只有在这些系统被合理解耦之后才可能**。

每个子系统理想状态：自己的 `update()`、自己的数据结构、外人只能看到它暴露的 API；重写、优化、删除其中任何一个都不影响别人。"完全隔离"不可能做到，关键是**在必须发生的交互面前依然保住这种隔离感**。

> 如果你发现自己宁愿在一个 toy project 里验证一个想法也不愿在真正的引擎里试一下——这是耦合过多的一个明确信号。

作者也直言**耦合蠕变（coupling creep）**：引擎往往一开始是解耦的，到了 deadline 前，一个 feature 塞不进现有 API，有人就开一扇后门；久而久之，引擎代码的编辑体验一点点变差。

## 四条原则

### 1. 警惕"框架"

这里"框架"是广义的——**任何要求你其他所有代码都遵从它某个世界观的系统**：

- 所有对象必须继承的 root class
- RTTI / 反射系统
- 序列化框架
- 引用计数框架

Niklas 的理由很实在：这些全局设施会把"某个特定设计选择"强加在整个引擎上，而这个选择可能根本不适合某个子系统。一个糟糕的 refcount 系统会禁死子系统的多线程；一个平庸的序列化系统会让 linear loading 变得不可能。

常见为"全局系统"辩护的理由是"maintainability——改一个点就全改完"。**实操里往往反着来**：全局系统侵入太深后，任何修改都要在无数地方同步进行，反而不可能再改。**每个子系统自己的 `save()` / `load()` 往往要好得多。**

对比 [[static-site-antiframework]] / [[middleware-vs-open-source]]：同样的警惕，换了个侧面。

### 2. 用高层系统调度低层系统

低层子系统之间**不要直接耦合**；让一个高层系统来搬运数据。

典型例子：脚步声涉及动画、材质、声音三个系统。它们两两之间都不该知道对方存在。由 gameplay 层去 poll 动画系统的事件、从材质系统取地面类型、然后让声音系统播对应音效。

Bitsquid 把这种"到处戳子系统的脏活"关在**Lua / Flow**（可视化脚本）里——**语言边界充当防火墙**，防止 mess 渗回下层引擎。

这也是很多成熟引擎的共同结构：**clean engine core + messy gameplay glue**，两层之间有一条明确的界线。参考 [[decoupled-tool-engine-json-rpc]]、[[flow-graph-data-oriented-runtime]] 的设计。

### 3. 代码重复有时是对的

"不要重复"是软件设计的老生常谈，但 Niklas 提醒：**代码共享是有代价的——它增加了系统耦合**。

他给了几个具体场景：

- **String 类滥用**：很多处理字符串的代码并不需要 `locale`、`find_first_of()`；一个 `const char *` + `strcmp()` + 几行自己写的小函数就够了，还能轻松搬到 SPU。
- **FixedArray / Vector 的泛滥**：函数签名吃 `const Vector<T>& v` 强迫调用方使用特定容器；如果改成 `const T* begin, const T* end`，调用方啥容器都能用。
- **工具代码重复读取 bundle 头**：一个用 C# 写的 patch 工具和 C++ 引擎都能解析 bundle header。要共享这段代码得：
  1. 剥成独立库；
  2. 因工具需要额外功能（大小端转换）得加 `#define TOOL_COMPILE`；
  3. 建专门的 build config；
  4. 将来重构引擎时被工具绑架。

  而**重写这 10 分钟的解析代码**？——将来 bundle 格式改一次，也就多花 10 分钟。

中心思想：**写代码从来不是问题，阻止你写代码的那些乱糟糟的耦合才是问题**。

参考 [[deep-modules]] / [[information-hiding]]：同样对"表面的 DRY"保持怀疑。

### 4. 用 ID 而不是指针引用外部对象

当一个系统必须持有对另一个系统对象的引用（gameplay 要改特效参数、要移动特效等），**不要存指针**：

- **裸指针 / `shared_ptr`**：生命期从被引用系统手里被剥走。
- **`weak_ptr` / 带 refcount 的 handle**：间接指针会被两个系统都访问（dereference 与 refcount 操作），天然产生线程问题；同时它也暗示"外部系统任何时候都能 deref 并用这个对象"，但子系统内部 `update()` 跑的时候可能不希望外人乱摸。

Niklas 的方案：**用 ID（整型）作为外部引用**。ID 是 POD，没有 "释放" 动作，可以随便拷、随便 DMA、随便丢给 Lua，不需要维护引用计数。

系统内部实现 ID → 对象 的快速映射（**不要用 `std::map`**）——最简单的方式是一个固定大小的 lookup 数组：

```
Object *lookup[MAX_OBJECTS];
// ID = 低 12 位索引 + 高 20 位 unique ID
```

低位当 `lookup[]` 下标，高位做"原对象是否已经被换掉"的校验。数组的空闲位置用 **in-place free list**（把下一空位下标写回 slot 本身）管理。

这个模式和 [[id-based-lifetime-with-kill-flag]]（cloudwu skynet 2.0）、[[handle-based-resource-manager]] 是一家人，只是侧重不同：Niklas 这里强调"**解耦**"——ID 让被引用的系统保留了**任意时刻重排内存、删除对象、异步双缓冲**的完整自由。

评论里还延伸出一个有意思的技巧——"**null 对象**"：把系统的 0 号槽预留成一个合法但无害的 null 对象；ID 失效时返回 0，外部代码不用分支即可安全读写（写入只污染 null 对象，等价于 /dev/null）。

## 为什么这四条特别有效

四条其实指向同一件事：**让系统的"内部决策空间"尽可能宽**。

- 不强加全局框架 → 内部数据结构自由；
- 让高层去搬数据 → 不会被横向兄弟拖下水；
- 不怕重复 → 不被"为了复用"的脆弱依赖绑架；
- 用 ID → 内存布局、生命期、双缓冲完全自己说了算。

这四条在 Bitsquid 后续的 [[data-driven-architecture]] / [[c-opaque-struct-modules]] / [[handle-based-resource-manager]] / [[custom-allocator-interface]] 里都能看到具体落地。

## 相关

- [[polling-callbacks-events]] — 本系列第二篇：低层系统如何把事件上报给高层
- [[id-based-lifetime-with-kill-flag]] — cloudwu 把类似思路做成了并发友好的生命期模型
- [[handle-based-resource-manager]] — 句柄式资源系统
- [[c-opaque-struct-modules]] — 用不透明结构体划边界
- [[decoupled-tool-engine-json-rpc]] — Bitsquid 工具 vs 引擎的解耦
- [[dependencies]] / [[modular-design]] / [[information-hiding]]
- [[niklas-frykholm]]

## Sources

- [[sources/bitsquid-managing-coupling]]
