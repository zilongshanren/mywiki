---
tags: [source, x11, xi2, 输入, gnome, linux]
date: 2026-04-14
sources: 1
---

# "Barriers"（Jasper St. Pierre）

[[jasper-st-pierre]] 2013 年 3 月发表于 blog.mecheye.net 的短文，记录 GNOME 3.8 里新加的"压力式消息托盘"以及背后的 X11 **pointer barrier** 协议扩展（XI 2.3）。

## 摘要

GNOME 3.6 的消息托盘是用户最抱怨的一处设计——弹出时机错、想看时不来、不想看时来。原设计不是这个样子；它之所以成为临时妥协，是因为真正需要的交互——"光标推住屏幕边缘，推够一段时间再弹"——**当时 X server 不支持**。Unity 早年也想做同样的事，Christopher Halse Rogers 为此写过一组 Ubuntu downstream X server patch。Jasper 和 Peter Hutterer 把 Halse Rogers 的 patch 捡回来、清理、规范化，花了约六个月把它做成可以合入上游的 X 协议扩展，结果就是 **pointer barrier 的 pressure 属性**，发布在 **XI 2.3** 里。

Pointer barrier 原本的功能是"在两块屏幕拼接处竖一条虚拟墙"，防止光标从一块屏掉进另一块屏、或者防止光标溜出应用区。XI 2.3 给它加了一个 pressure 维度：barrier 记录光标累积推压的力度/时间，达到阈值就触发事件。GNOME 3.8 的消息托盘就是监听底部 barrier 的 pressure 事件——"推住屏幕底边"作为一个显式的、可被取消的手势。因为它是 X server 协议层的能力，GNOME 之外的任何桌面环境都能用。Jasper 顺手写了个"Android 风格"的压力可视化 bar 做 screenshot 用，后来打包成独立的 [GNOME Shell extension](https://extensions.gnome.org/extension/634/tray-pressure-visualizer/)。

## 关键要点

- **pointer barrier**：X11 的一个 feature，允许客户端在屏幕坐标空间里声明一条"虚拟墙"，光标无法穿越（除非使劲推——这就是 pressure 的出发点）。
- **pressure 属性**（XI 2.3）：barrier 携带一个"已累积推压量"状态，超过阈值触发 `XIBarrierPressedEvent`，这是一个 UI 设计可以依赖的**显式手势**，而不是靠 timeout 猜用户意图。
- **六个月上游协议设计**：Unity 的 Halse Rogers downstream patch → Peter Hutterer & Jasper 清理规范 → upstream XI 2.3，这种"从 downstream patch 到 upstream 协议"的路径是 Linux 输入栈很多 feature 的典型演化过程。
- **XI = X Input Extension**，是 X 协议里的输入子系统，2.x 版本引入了多指针、多键盘、浮点坐标、手势等现代输入栈需要的能力；2.3 是 pointer barrier pressure 所在的版本。
- **为什么必须改 X server**：timeout 驱动的弹出不可靠是因为 client 不知道光标在边缘的"推压历史"——那是 server 的状态。这件事必须做在 server 里。这也解释了 GNOME 3.6 为什么只能先做个丑陋的妥协版。
- **触屏设备的替代设计**：barrier 是光标语义，不适合触屏；评论里提到设计组准备给触屏另做一套"从底边上滑"的手势。

## 链接到的概念

- [[x11-pointer-barrier]]
- [[jasper-st-pierre]]

## 原文

- 链接：<https://blog.mecheye.net/2013/03/barriers/>
- 本地：`raw/articles/blog.mecheye.net/2013-03-19_barriers.md`
