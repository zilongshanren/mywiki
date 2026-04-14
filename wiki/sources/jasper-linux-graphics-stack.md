---
tags: [source, linux, 图形栈, x11, wayland, mesa]
date: 2026-04-14
sources: 1
---

# "The Linux Graphics Stack"（Jasper St. Pierre）

[[jasper-st-pierre]] 2012 年 6 月发表于 blog.mecheye.net 的长篇综述，是他日后 [[sources/jasper-dri-linux-graphics-stack|"DRI" 一文]] 的前身，目标是给非内核开发者一份可读的 Linux 图形栈"导览地图"。由 Adam Jackson、David Airlie 技术 review。

## 摘要

文章沿着"一个程序如何把像素送上屏幕"这条主线，把 Linux 开源图形栈从上到下各层串起来：应用用 **OpenGL** 或 **cairo** 画图；OpenGL 路径走 **Mesa**（内含软件后端 swrast/softpipe/llvmpipe 和硬件驱动），radeon/nouveau 驱动通过 **Gallium** 框架把 OpenGL state 翻成中间表示 **TGSI** 再翻成硬件指令，Intel 驱动拒绝 Gallium 层、直接走自己的栈；2D 路径走 cairo → **XRender** X 协议扩展 → Xorg 驱动或 **pixman** 软件光栅化。再往下，Mesa 和 Xorg 共享 **libdrm**，通过 **GEM/TTM** ioctl 与内核 **DRM** 子系统通信；**KMS**（Kernel Mode Setting）负责设置显示模式与 framebuffer，`Plymouth` 启动画面是只用 KMS 的典型例子。作者还讲了 **DRI2** 做同步、**COMPOSITE 扩展** 与 **COW**（Composite Overlay Window）、**Texture from Pixmap (TFP)** 让 compositor 把 X11 窗口当作 GL 纹理、**AIGLX** 的临时 hack 身份、**redirection / unredirection** 的优化，以及 **Wayland** 为什么选择复用这一整套底层、但砍掉 `/usr/bin/Xorg` 进程、让 compositor 直接读 evdev、调 KMS/DRM 显示 buffer——"窗口管理器就是 display server 本身"。最后用"networked transparency 在现代 Linux 桌面上早已半瘫"为 Wayland 的激进选择做了辩护。

## 关键要点

- **两条路径，一套底座**：OpenGL 和 cairo/XRender 是两条不同的上层 API，但最终都会通过 libdrm → DRM → GPU 完成上屏，这是理解 Linux 图形栈的第一步。
- **Mesa 不只是 `libGL.so`**：它同时提供多种软件后端（swrast/softpipe/llvmpipe）和硬件驱动；Gallium 是其中的驱动构建框架，Intel 驱动不走 Gallium 是一个真实的反例。
- **TGSI**：Gallium 驱动用的中间表示，上游由 state tracker（OpenGL / GLSL / D3D）产出，下游由硬件后端消费。
- **libdrm 里的 GEM 与 TTM**：两套 ioctl buffer 管理方案——GEM 来自 Intel、当初号称比 TTM 简单，后来复杂度追齐。
- **DRI2** = Mesa、Xorg、内核之间的同步协议；DRI1 被弃用。
- **Expose 模型 → Redirection**：80 年代的 X11 窗口是"丢失的"——窗口被遮挡后要自己 repaint。现代 compositor 通过 COMPOSITE 扩展 + COW + TFP 让窗口无损：X server 为每个窗口维持一张 pixmap，compositor 拉出来当 GL 纹理画回 COW。
- **AIGLX** 是"把 GL 放在软件里跑，避开 GPU 拷贝"的过渡 hack；DRI2 成熟后已被 TFP + 零拷贝取代。
- **Unredirection**：全屏窗口可以跳过 compositing 路径直接走 front buffer，保 60 FPS 游戏性能。
- **Wayland 的精简账**：把 display server 与 window manager 合并之后，mutter 里用来维持 X server 一致性的几千行代码可以删掉；compositor 本身只需 2000–3000 SLOC 就能跑起 evdev → KMS → buffer → draw 的整条路径。
- **network transparency 的现状**：X 的网络透明性已被 DBus、clipboard、drag-and-drop 等非 X 通道抽空，Wayland 放弃网络透明是承认现实而非开倒车。
- **DIX/DDX**：Xorg 内部的"Device Independent X / Device Dependent X"分层，DDX 驱动 = 过去所谓的 Xorg 驱动。

## 链接到的概念

- [[linux-graphics-stack-dri]]
- [[jasper-st-pierre]]
- [[x11-composite-redirection]]
- [[wayland-compositor-model]]

## 原文

- 链接：<https://blog.mecheye.net/2012/06/the-linux-graphics-stack/>
- 本地：`raw/articles/blog.mecheye.net/2012-06-16_the-linux-graphics-stack.md`
