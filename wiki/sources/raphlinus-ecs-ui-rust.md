---
tags: [source, gui, rust, ecs, 架构]
date: 2026-04-14
sources: 1
---

# Entity-Component-System architecture for UI in Rust（Raph Levien 2018）

[[raph-linus]] 2018 年 5 月为 `xi-win-ui`（xi-win 里手写的 GUI 层）写的架构笔记。这是 [[reactive-ui-rust|Druid]] 最早期的原型设计文档——Druid 后来抛弃了它的 ECS 风格，但"用整数 id + state splitting + continuation 对抗借用检查器"这三个手法被继承到了整条 linebender 路线。

## 摘要

Raph 先诊断了 **Rust GUI 为什么难**：传统 OOP widget 需要持有父子引用并互相调方法，但 Rust 的借用检查器不允许这种任意共享可变；回退到 `Rc<RefCell<T>>` 会让代码充斥 `.borrow_mut()`、时不时 panic，"不 idiomatic"到让人不想写。他从游戏 ECS 借了两个想法——**所有 component 存进一个大 `Vec`、`usize` 做 entity id**——再配上两个 Rust 特有的手法：**state splitting**（进系统时把 `&mut UiState` 拆成若干子字段引用，让借用检查器在编译期证明访问模式安全）和 **data flow 而非 control flow**（widget 不直接递归调用 child 的 layout，而是返回一个 `RequestChild(id)` 让 system 代劳；事件 handler 不直接调 listener 而是往 queue 里 push event，borrow 释放后 system 再派发）。整篇文章被 Raph 自己事后承认"这其实不是真正的 ECS，更像 hybrid——真 ECS 是 database + system 模型，而 xi-win-ui 把 UiState 同时当了 database 和 system 用"。尽管如此，核心诊断"Rust GUI 应该用 data flow 而非 control flow"在后续 Druid / Xilem 的设计里反复被验证。

## 关键要点

- **`RefCell` 满天飞 = 架构选错的味道**，不是 Rust 的锅
- **整数 id 代替指针引用** 绕开"树节点互相持有引用"的借用检查死结
- **state splitting** 是 idiomatic Rust 的核心手法：编译期证明访问模式安全，比 interior mutability 更可预测
- **continuation 风格的 data flow**：用 return value + event queue 代替直接的递归 / callback，让 borrow 生命周期能规范切分
- **`Box<dyn Any>` 作为 event queue 的数据载体**：把类型擦除局限在需要的地方，concrete listener 自己负责 downcast
- Reddit 讨论后作者承认这**不是真·ECS**——只是借了"entity = integer + components in Vec"两个表象；真 ECS（Bevy UI 那种）是另一回事
- Flutter 的 "constraints 向下、sizes 向上"layout 模型在 Rust 里需要用 return-and-call-back 模式实现

## 链接到的概念

- [[ecs-for-rust-ui]]
- [[reactive-ui-rust]]
- [[rust-gui-ecosystem]]
- [[ecs]]
- [[raph-linus]]

## 原文

- 链接：https://raphlinus.github.io/personal/2018/05/08/ecs-ui.html
- 本地：`raw/articles/raphlinus.github.io/2018-05-08_entity-component-system-architecture-for-ui-in-rust.md`
