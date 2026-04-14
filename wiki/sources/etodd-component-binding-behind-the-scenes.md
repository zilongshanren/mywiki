---
tags: [source, c-sharp, ecs, 组件, 数据绑定, mvvm]
date: 2026-04-14
sources: 1
---

# As promised: Component Binding "BEHIND THE SCENES"（Evan Todd / etodd.io）

[[people/evan-todd|Evan Todd]] 2011 年 6 月的实现细节篇，是 [[sources/etodd-refactoring-with-components|Refactoring with components]] 的姊妹文，回答读者「这套数据绑定具体怎么写」。配合那篇宣言式短文一起读，能完整还原 Todd 的 [[component-entity-data-binding|端口式组件实体]] 系统。

## 摘要

Todd 从一个传统 OO 继承层级（GameObject / Player / Camera / Map）出发，第一步是把所有对象共有的「位置」抽到一个 `TransformComponent`，再加 `ModelComponent`，用一个 `PlayerFactory` 把它们装进同一个 `Entity`。然后到了关键问题：**怎么让 `TransformComponent` 算出来的 `Matrix` 自动「流到」`ModelComponent`**？答案是 `Property<T>` 类——一个能侦测 setter 的泛型属性容器，加上 `Binding<T>` 类把两个 Property 链起来。Property 的 setter 会通知所有挂在自己身上的 Binding，Binding 再同步另一头的值。Todd 后来扩展出多种 Binding：单向 / 双向、跨类型（用 lambda 做投影，例如把玩家朝向 float 转成 `Matrix.CreateRotationY(x)`）、多输入合成、惰性求值。

文章用「crouch」按键的例子对照了 OOP 与 Binding 两种写法：OOP 要在 `Player.Update` 里写一段 `if (Keys.Crouch) height = 1 else 2`，把行为埋进过程式更新；Binding 写法只声明「`collisionComponent.Height` 是 `crouchKeyPressed` 的函数」一行——**从过程式变成声明式，像写 HTML markup 描述行为关系**。Todd 在文末还加了 Setter/Getter delegate（让 Property 直接 wrap 第三方对象比如 `AudioListener`）、以及 MVVM 风格的 `Command` / `CommandBinding`（Property 是值，Command 是事件），把 dataflow 系统补成了完整的「值 + 事件」双轨。他承认这套 pattern 不是银弹，自己代码里仍然有过紧的耦合，但已经向「自文档、可维护」前进了一步，也开源了核心类（旧 Google Code 仓库）。

## 关键要点

- `Property<T>`：泛型属性容器，setter 触发挂在身上的 Binding 同步另一端
- `Binding<T>` 多种变体：单向、双向、跨类型 lambda 投影、多输入合成、惰性
- crouch 例子：OOP 是过程式 update，Binding 是声明式关系——「像 HTML markup 描述行为」
- 「Blob 组件」过渡策略：先把所有旧的过程式代码塞进一个 Blob 组件，再慢慢拆
- Setter/Getter delegate：让 Property 包装第三方对象（例如 XNA 的 `AudioListener.Position`）
- 借鉴 MVVM：`Command` + `CommandBinding`，Property 管值、Command 管事件
- Todd 承认 pattern 不是银弹，仍有过紧耦合，但更接近自文档化

## 链接到的概念

- [[component-entity-data-binding]]
- [[ecs]]
- [[classitis-in-games]]
- [[information-hiding]]

## 原文

- 链接：https://etodd.io/2011/06/27/component-binding-behind-the-scenes/
- 本地：`raw/articles/etodd.io/2011-06-27_as-promised-component-binding-behind-the-scenes.md`
