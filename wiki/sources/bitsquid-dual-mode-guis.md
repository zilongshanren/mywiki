---
tags: [source, bitsquid, gui, 渲染, 引擎架构]
date: 2026-04-19
sources: 1
---

# BitSquid's Dual Mode GUIs（Niklas Frykholm / Bitsquid）

[[niklas-frykholm|Niklas Frykholm]] 2010 年 8 月的 post，讲 Bitsquid GUI 子系统用**同一 API、同一实现**同时支持 retained 模式和 immediate 模式的设计。关键不在多写一份 immediate 实现，而在把状态从 GUI 层里彻底拿掉。

## 摘要

GUI 渲染最大的性能挑战是大量小对象打爆 batch。Bitsquid 的 renderer 按 `(layer, material)` 做 batch，每个 GUI 对象发过来的是 `(id, batch_key, vertex_data)`，同 batch 的顶点全塞进一个 buffer。修改等于拿相同 id 重发一份，renderer 删旧插新；销毁等于请 renderer 把该 id 对应的顶点删掉。API 长这样：`create_text(pos, text, font, color)`、`update_text(id, pos, text, font, color)`、`destroy_text(id)`——**没有** `set_color()` 这种 setter，要改就整套重发。这看似笨，但逻辑是：上层本来就有那些数据（玩家名、颜色、字体），让 GUI 层再存一份只会产生同步 bug。整个 GUI 层**不持有任何跨帧状态**，renderer 只有顶点。于是 retained 和 immediate 的差别被压缩到一个布尔位——renderer **每帧是否清空所有 batch**。immediate 模式下每帧重新 create 即可。读者追问 scrollbar 怎么返回状态；Frykholm 答：GUI 不持状态，scroll 值存在外部 `scroll_value` 变量里，GUI 只负责画。输入如何变状态是更高层系统的事。

## 关键要点

- GUI 大量小对象 → 必须 **(layer, material)** batching；
- renderer 持有的唯一 retained 东西是**顶点**；
- API 不提供增量 setter，update 必须**一次给齐**——单一 source of truth 在调用方；
- **retained vs immediate = renderer 每帧是否清空 batch**，其他完全一致；
- 立即模式的"返回值"那类 API（Dear ImGui 风格）属于更高层 UI 框架，不是 renderer 的事；
- 状态放在调用方、不重复在 GUI 层——[[intent-vs-state|intent-only]] 思路。

## 链接到的概念

- [[dual-mode-gui-bitsquid]]
- [[immediate-vs-retained-mode]]
- [[batching]]
- [[draw-call]]
- [[intent-vs-state]]

## 原文

- 链接：<https://bitsquid.blogspot.com/2010/08/bitsquids-dual-mode-guis.html>
- 本地：`raw/articles/bitsquid.blogspot.com/2010-08-25_bitsquid-s-dual-mode-guis.md`
