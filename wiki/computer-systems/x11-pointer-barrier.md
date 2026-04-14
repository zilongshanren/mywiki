---
tags: [x11, 输入, xi2, 交互设计, linux, gnome]
date: 2026-04-14
sources: 1
---

# X11 Pointer Barrier 与"推压式"交互

**Pointer barrier** 是 X11 的一个小而深的协议扩展：让客户端在屏幕坐标空间声明一条"虚拟墙"，光标无法穿越这条墙——或者说，要穿越它得**推压**够力。GNOME 3.8 的消息托盘"把光标按在屏幕底部一小段时间才弹出"就是这个 feature 第一个面向用户的应用。这篇是它的机制简介与设计动因。

## 问题：timeout 驱动的交互为什么不可靠

GNOME 3.6 最初只能做"光标停在底边 N 毫秒后弹出"这种 timeout 式弹出，原因是 X client 拿不到"光标在边缘推压的历史"——那是 server 的状态。结果就是两类 bug 同时存在：

- **想弹不弹**：用户真需要它时，光标在底边的停留"不够直"或"中途晃了"，timeout 被打断；
- **不想弹也弹**：看视频时光标自然落在底部，timeout 就把托盘弹出来挡住视频。

这两类都不是参数调得不好——它们是把 UI 决策放在了**错误的层**。光标在边缘的力度/时间这个信号只能来自 server，client 没办法自己可靠地合成它。所以正确的解法只有一条：**修 X server**。

## 解法：把"墙"加一个 pressure 维度

Pointer barrier 早先只是个"真墙"，用在多显示器拼接处防止光标从一块屏意外掉进另一块屏。Unity 最早想把它用来做"dash pressure activation"，Christopher Halse Rogers 写过一组 Ubuntu downstream X server patch。Peter Hutterer 和 [[jasper-st-pierre]] 把 patch 捡回来清理、规范化，花了约六个月把它做成上游协议，结果就是 **XI 2.3**（X Input Extension 2.3）里的 pointer barrier pressure 属性。

改完之后的机制：

- 客户端通过 XInput 2.3 向 server 注册一条 barrier（起止坐标、朝向、pressure 阈值）；
- Server 维护每条 barrier 的累积推压量——光标靠在墙上的时间、速度、力的积分都能参与计算；
- 推压到达阈值时，server 发 `XIBarrierPressedEvent`（或类似名字的事件）给客户端，客户端据此显式响应手势；
- 推压解除、超时、光标离开 barrier 区域时累积量会被合理地衰减或清零。

这让"推屏幕边"从一个**猜测**变成一个**一等公民手势**：它可被显式取消、可被可视化、可被 UX 文案准确描述。

## 为什么 GNOME 要等这件事

GNOME 3.8 的消息托盘正是它的第一个大规模用户，"把光标推住底部"这个动作从此有了可信的服务器侧判据。Jasper 顺手写了一条"Android 风格"的压力可视化动画，screenshot 用，后来单独打包成 [GNOME Shell extension](https://extensions.gnome.org/extension/634/tray-pressure-visualizer/)。

比 feature 本身更重要的是这件事暴露出来的**分层真相**：有些 UX 感官——边缘推压、摇动手势、延迟 tap——不是单纯在客户端写 timer 能凑出来的，它们的信号源在 server/kernel，客户端只是消费者。把 "UX 感官"和"事件源"搞混是 UI 框架常见的陷阱，也是 GNOME 3.6 消息托盘 fiasco 的根因。

## 与 Wayland 的衔接

Wayland 合并了 server 与 compositor，pointer barrier 这类"服务器端输入决策"的设计空间天然更大——compositor 自己跑 evdev 又自己画所有东西，不需要单独协议扩展就能做压力手势、边缘滑入、速度感应。这也是 [[wayland-compositor-model|Wayland compositor 模型]] 的一个具体收益：不再需要先改协议、再改服务器、再改客户端这三段论。

## 历史路径：downstream patch → upstream 协议

barrier pressure 的演化轨迹——Unity 的 Ubuntu downstream patch → 六个月的上游化 → XI 2.3 协议扩展 → 被 GNOME 等环境共享——是 Linux 输入与图形栈里很多 feature 的典型形态。这条路径说明一件事：**"downstream 有人真跑起来一个原型"** 是 upstream 能否把一件事做成协议的重要前置条件——没有 Halse Rogers 的 Unity 侧原型，Peter Hutterer 和 Jasper 可能不会从头去做这件事。

## 相关

- [[x11-composite-redirection]]
- [[wayland-compositor-model]]
- [[jasper-st-pierre]]

## Sources

- [[sources/jasper-barriers]]
