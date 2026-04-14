---
tags: [wayland, 图形栈, 窗口系统, compositing, linux]
date: 2026-04-14
sources: 1
---

# Wayland：Compositor 即 Display Server

Wayland 最激进、也最容易被误解的设计决定是：**没有独立的 display server 进程**。没有 `/usr/bin/wayland` 跑在后台，也没有一个"所有 client 通过网络协议连进来"的 X server。"窗口管理器"自己就是 display server；Wayland 术语里叫它 **compositor**。

## Compositor 一个人做几件事

在 X 的世界里，一个现代桌面有三层：Xorg（display server）、mutter/Compiz（窗口管理器 + compositor）、应用程序（client）。三者之间靠 X11 协议 + DBus + 共享内存 + DRI2 来保持一致。这种一致性是脆弱的——mutter 里大约 **4000–5000 SLOC** 就是为了让"窗口焦点、堆叠顺序、位置"这几件事和 X server 里的状态不发生 drift。

Wayland 压缩了这个结构：compositor 进程自己负责

- 用 `evdev` 直接从内核读输入事件；
- 用 KMS + DRM 初始化 framebuffer、设置显示模式；
- 接收 client 的 buffer 并合成到屏幕；
- 分发输入事件到窗口——而"窗口位置"永远是 compositor 本地真相，不需要和谁对账。

据 [[jasper-st-pierre]] 的估算，一个能跑起来的 Wayland compositor 最小规模大约是 **2000–3000 SLOC**，比上面 mutter 那 4000–5000 SLOC 的"X 同步胶水"还要少。这是 Wayland 在架构账目上的核心收益：砍掉一层，就砍掉那一层的一致性代码。

## libwayland 只是"参考实现"

Wayland 协议本身是规范、不是库。`libwayland` 是一份参考实现，但 compositor 和 client 都可以用任何语言手写协议栈——有人写过纯 Python 的 Wayland compositor。这是它与 X 的另一个差别：X 的事实标准 `Xlib`/`XCB` 基本绑定了你只能用 C 系。

## Client 如何画

Wayland client 的画法是：向 compositor 请求一块 buffer（或自己分配一块并告诉 compositor），自己随便画——cairo、OpenGL、Vulkan 都行——然后 commit 给 compositor。Compositor 拿到 buffer 后可以做任何事：正常显示、扭曲、旋转、烧掉、贴到 3D 场景上。Compositor 是上帝，这件事在 X 下就因为 [[x11-composite-redirection|redirection 模型]] 里 X server 还保留一份"窗口真实位置"的状态而不成立。

## 为什么没有网络透明性

Wayland 刻意不提供 X 那样的"网络透明协议"。[[jasper-st-pierre]] 为这个决定辩护的理由是：X 的网络透明性在现代 Linux 桌面上早已实际失效——clipboard、drag-and-drop、DBus 服务、设备热插拔、现代 GL 的 indirect context——没有一样在跨网段的 X session 里能真正工作。"X 能跨网用"只剩下一种情形：在 LAN 里跑一个轻量 GTK 应用回本地显示。现代的替代是 RDP/SPICE 这样的"远程整个桌面"协议，或者 SSH tunnel + VNC——它们都在抽象层更高的地方做远程，而不是强迫 display server 本身网络透明。

## 服务端装饰 vs 客户端装饰

Wayland 倾向让 client 自己画窗口边框（client-side decorations），而不是像 X 那样由 compositor 统一接管。理由和旋转/缩放窗口时边框与内容之间的接缝问题有关——如果 compositor 自己画边框，缩放中会出现错位。代价是一致性：每个工具包都要各画各的边框。社区共识是未来需要一个 `libwayland-decorations` 来给出统一样式。

## 相关

- [[linux-graphics-stack-dri]]
- [[x11-composite-redirection]]
- [[jasper-st-pierre]]

## Sources

- [[sources/jasper-linux-graphics-stack]]
