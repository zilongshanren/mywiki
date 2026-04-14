---
tags: [gui, rust, ecs, borrow-checker, 架构]
date: 2026-04-14
sources: 1
---

# Rust UI 的"类 ECS"架构：用整数 id 和 state splitting 对抗借用检查器

2018 年 [[raph-linus]] 在写 xi-win（xi-editor 的 Windows 前端）时自己手写了一套 UI 层 `xi-win-ui`，写完之后发现用起来竟然比预想的顺利很多。他把这个经验写成文章，一开始叫"ECS architecture for UI in Rust"，后来在 Reddit 讨论里被社区指出"这其实不是真正的 ECS"，于是改口为**"受 ECS 启发的混合架构"**。更准确的说法是：**它从游戏 ECS 那里借走了两个关键想法——把 component 存进一个大 `Vec`、用 `usize` 作为节点 id——然后配上 Rust 特有的 state splitting 和"data flow 而非 control flow"两个手法**，系统化地回答了"Rust 里 GUI 怎么写才不打架"。

这篇文章之所以重要，是因为它对 **Rust GUI 为什么难** 给出了一个结构化诊断，而不只是吐槽。

## Rust 里的 GUI 之难

- 传统 GUI widget 树里，每个 widget **握着指向父子的引用**、**持有自己一块状态**、**可以直接调兄弟或父的方法**——这基本等同于"所有 widget 的状态对所有 widget 同时可写"。
- Rust 的借用检查器不允许这种任意共享的可变。最直白的 workaround 是 `Rc<RefCell<T>>`（或多线程下的 `Arc<Mutex<T>>`），把借用检查从编译期推到运行期，代价是满屏的 `.borrow_mut()`、时不时的 panic、以及"不 idiomatic"的 Rust 品味扣分。
- 另一个压力是**增量性**：GUI 要 fast path 就得只重算改变的那一部分 widget、只重绘脏区。架构必须能表达"局部变更"。

> Raph 的观点是：`RefCell` 满天飞是一种"不 idiomatic Rust"的味道——它在告诉你**架构选错了**，而不是 Rust 本身的锅。这和整个 [[reactive-ui-rust|Rust 反应式 UI]] 研究的底层判断一致。

## 第一招：整数 id 而非指针引用

把所有 widget 存进一个 `Vec<Box<Widget>>`，对外暴露的"引用"是这个 vec 的 **`usize` 下标**。parent/child 关系也用 id 记录。于是整个 widget 树变成一张图，遍历靠 id 查表——这条路绕开了"持有指向树其他节点的引用"这个借用检查死结。

这一招本身早就是 Rust 生态的共识：conrod 也用类似手法，社区有 "Idiomatic tree and graph like structures in Rust" 这样的参考文章。Raph 在这里只是再提供一个数据点。

## 第二招：state splitting

关键洞察：**"一个 widget 在不同阶段需要的 mutable 范围不一样"**。

- layout 阶段：`graph` 不变、`components` 可变（要存 layout 结果）、`geometry` 可变
- paint 阶段：`geometry` 不变、render target 可变
- event handler：一个 `context` struct 持有"够这一步用的那部分可变引用" + 一个 event queue

惯用的 Rust 做法是：进入系统时拿整个 `&mut UiState`，然后立刻把它**拆成**几个独立字段的引用，某些字段 `&`、某些字段 `&mut`，以类型签名让借用检查器在**编译期**就证明这个访问模式是安全的。

这就避免了把一切塞进 `RefCell` 后在运行期祈祷不 panic——Raph 特别强调这是比 interior mutability 更 idiomatic 的路子。

## 第三招：data flow 而非 control flow

真正棘手的是 **递归**。Flutter 风格的 layout 是 container 递归调用 child 的 layout 方法——但 container 要调 child，必须从自己的 `&mut [Box<Widget>]` 里再 `&mut` 借一次，而自己此刻已经被一次 `&mut` 借走了，借用检查器当场拒绝。

Raph 的解法是 **continuation 风格**：widget 不自己去调 child，而是**返回**一个 `RequestChild(id)` 结果，告诉 system "帮我去递归那个 id 一下然后把结果带回来给我"。system 拥有完整的 `&mut UiState`，它来负责递归，递归完再重新进入 widget 的 layout 方法并把结果传进来。

event listener 机制用同一个套路：按钮的 click handler **不直接调** listener（因为那可能会修改任何 widget），而是**往 context 里的事件队列 push 一条 event**，等 handler 返回、mutable borrow 释放之后，system 再把 event 派给 listener，listener 此刻持有完整的 `&mut UiState`，想干嘛都行。

Raph 还顺手提了一个漂亮的 Rust 技巧：event queue 用 `Box<dyn Any>` 来容纳不同 widget 发出的不同类型，concrete listener 自己知道该 downcast 到什么类型——把类型擦除局限在那一小块需要的地方。

## 与真·ECS 的差异

- 真正的游戏 ECS 是 **database 模型**：component 按类型分别存储、system 是跨类型的查询和处理。
- xi-win-ui 的 component 是 `Box<dyn Widget>`——没有按类型拆开，也没有系统意义上的"System"。它只借了 ECS 的"entity 是 usize、数据集中存储"两个表象。
- 社区讨论之后 Raph 自己承认这个描述不准，改称"hybrid"。这点值得记住——很多 Rust GUI 文章提到 "ECS for UI" 其实都是这种 hybrid，真·ECS（Bevy UI 那种）是另一回事。

> 对游戏 ECS 的深度讨论参见 [[ecs]]。

## 和 Druid / Xilem 的关系

xi-win-ui 是 [[reactive-ui-rust|Druid]] 的原型祖先。Druid 正式版抛弃了"类 ECS"这个框架，改用 **lens + data flow** 模型——但两者的共同基因是一致的：**用编译期已知的借用结构代替 `RefCell`、用 data flow 替代 control flow**。后来的 **Xilem** 进一步把这套思路抽象成"view tree diff + message 队列"的架构。

这是 linebender 路线图的第一块砖。

## 对"先 crates.io 还是先自研"的小结

Raph 在文章里给出了一个结论：**如果你要在 Rust 里从零造 GUI，这组手法（整数 id、state splitting、continuation-style data flow）可以让你的代码里完全不出现 `RefCell`**。这不是 ECS、不是 react、不是 immediate mode——它是 Rust 本身约束下挤出来的架构形状。

## 相关

- [[reactive-ui-rust]] — Druid / Xilem 的反应式研究，是这套架构的后续演进
- [[rust-gui-ecosystem]] — linebender 路线与其他 Rust GUI 的对比
- [[ecs]] — 真正的游戏 ECS 作为对照
- [[raph-linus]]

## Sources

- [[sources/raphlinus-ecs-ui-rust]]
