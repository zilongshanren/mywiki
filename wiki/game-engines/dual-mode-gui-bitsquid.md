---
tags: [gui, 渲染, 批处理, 引擎架构, bitsquid]
date: 2026-04-19
sources: 1
---

# Bitsquid 双模 GUI

Bitsquid 的 GUI 子系统用**同一套 API、同一份实现**同时支持 retained mode 和 immediate mode，两者的区别只是一个开关。这个对称设计的关键不在"两种模式各写一份然后共用接口"，而在于把状态从 GUI 层里彻底拿掉——[[immediate-vs-retained-mode|retained 和 immediate 在 Bitsquid 的语境下合并成了同一件事]]，只是生命周期不同。

## 渲染层：只保留顶点，不保留状态

GUI 里"成百上千个小元素"会把 batch 打爆，所以渲染层核心是 batching：

- 每个 GUI 对象被主线程给一个 **id**；
- 按 **(layer, material)** 作为 batch key，同一 batch 的顶点全塞在一个大 vertex buffer 里；
- 主线程把 `(id, batch_key, vertex_data)` 发给 renderer；
- renderer 查 batch：有就 append，没就新建。修改等于拿同样 id 重发一份，renderer 先删老的再插新的。

整个 renderer 不保留"这段文本是什么字体、什么颜色"——它只知道**顶点**。字体、颜色、字符串本体都在调用方那边。

## API：update 必须一次给齐所有参数

上层接口长这样：

```
create_text(pos, text, font, color) -> id
update_text(id, pos, text, font, color)
destroy_text(id)
```

注意**没有** `set_color()` / `set_text()` / `move()` 这种 setter。想改什么？都得把整个状态重新送一遍。

这听起来反常识，但 Frykholm 的解释是：**上层本来就有那些数据**。文本显示的 `player_name`、颜色、字体大小都是 UI 调用方的状态变量。如果 GUI 层里也存一份 retained state，会变成"两份状态要同步"——多一个 bug source。不如每次都让调用方把当前状态全塞进 update——反正不会更贵，数据都在那儿。

这是把 [[intent-vs-state|intent vs state]] 倒过来看：GUI 层退化成**纯 intent pipeline**，不持有状态——调用方每次声明"当前这个 id 应该长什么样"。

## 双模：只改 renderer 的 lifetime policy

在这个基础上：

- **retained 模式**：create → update 任意次 → destroy。对象跨帧存在于 batch 里，renderer 不主动清理；
- **immediate 模式**：renderer 每帧开头清一遍所有 batch；调用方每帧重新 `create()` 一次想画的东西。update / destroy 在这个模式下用不上。

两种模式走**同一套接口、同一套 batching 代码、同一段 renderer 实现**。差别只有"renderer 每帧清不清"这一个布尔标志。

## 代价与边界

评论里有人追问：立即模式的 UI 不是该能"返回 widget 状态"吗（点击了、scrollbar 滑了）？Frykholm 的回答揭示了模式是**纯渲染层**的：

> "GUI 不持有状态，所以也不返回状态。"

scrollbar 的当前位置存在 `scroll_value` 这个**外部变量**里，`create_scroll_bar(pos, size, 0, 100, scroll_value)` 只负责把这个数值画出来。Dear ImGui 那种"返回值就是新状态"的体验是**上层再包一层**的事——Bitsquid 这层只管把 draw 做好。输入的处理是更高层次的系统（window GUI 一套、gamepad GUI 一套）的职责，不混进来。

## 为什么这个设计能自洽

- renderer 只保留**画什么**（顶点），不保留**为什么画**；
- API 把修改定义成"整个重发"，拒绝增量 setter；
- 两种模式的区别被压缩到一个布尔位——因为**驱动"什么时候清"的那个决定**是两种模式唯一真正的差别。

这是把**状态"属于谁"这个问题**先想清楚的典型案例。砍掉 retained 内部状态之后，retained/immediate 不再是两个实现，只是两个使用协议。

## 相关

- [[immediate-vs-retained-mode]]
- [[batching]]
- [[draw-call]]
- [[intent-vs-state]]
- [[niklas-frykholm]]

## Sources

- [[sources/bitsquid-dual-mode-guis]]
