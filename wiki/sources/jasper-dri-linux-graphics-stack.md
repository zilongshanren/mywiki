---
tags: [source, linux, 图形栈, 系统]
date: 2026-04-14
sources: 1
---

# "DRI"（Jasper St. Pierre）

[[jasper-st-pierre]] 2016 年 1 月发表于 blog.mecheye.net 的短文，目标是一次把 Linux 图形栈里"DRI / DRM / KMS / libdrm / wl_drm"这几个长得差不多的缩写拆开讲清楚。

## 摘要

"DRI" 原意是 [Direct Rendering Infrastructure](http://dri.freedesktop.org/wiki/DriHistory/)——把 Mesa OpenGL 实现、Xorg 服务器和 Linux 内核粘到一起、让 Linux 第一次能用 GPU 做硬件 3D 渲染的工程。但这个名字被反复复用到了至少三个不同的东西上：内核里的 **DRM**（Direct Rendering Manager）子系统、Mesa 里的 **DRI driver model**（两代 DRI1/DRI2，和 X 协议重名）、以及 X 服务器端的 **DRI X 协议扩展**（DRI1/DRI2/DRI3）。`/dev/dri/card0` 的 "dri" 和 `dri2proto` 的 "dri2" 完全是两回事。文章还顺带点了 **libdrm**（DRM ioctl 的用户态包装库），**KMS**（Kernel Mode Setting，DRM 下的显示控制器 API，也叫 DRM mode），和 Mesa/Wayland 之间的 `wl_drm` 内部协议。作者的结论是：命名是整个工程的最大技术债，但 backward compatibility 让它无法被清理。

## 关键要点

- **DRI ≠ DRM**。DRI 是项目名和代号；DRM 是内核子系统名。Userspace 通过 `/dev/dri/*` 节点与 DRM 通信——设备节点的命名属于历史遗留。
- **三块代码同名很危险**：Mesa 的 `i915_dri.so` 指的是 Mesa 内部的 "DRI driver model"；Xorg 的 DRI1/DRI2/DRI3 是 X 协议扩展；内核的 DRM 是运行时驱动。
- **DRI driver model 有两代**（DRI1/DRI2，纯 Mesa 内部），**X DRI 协议有三代**（DRI1/DRI2/DRI3），二者独立演化，编号却高度相似，Mesa 代码里可能一个文件既出现 DRI2 又出现 DRI3，分别指两件不同的事。
- **KMS = DRM mode**：DRM 子系统内部其实并列了两套 API，一套控制渲染（command submission、buffer allocation），一套控制显示输出（modesetting、CRTC、connector）。后者就是 **KMS / DRM mode**。长期计划是把二者拆成两种设备节点：**render nodes** 和 **KMS nodes**。
- **libdrm 是 DRM 用户态包装**：减少 Xorg 和 Mesa 之间关于 buffer 管理的重复代码；其中 Intel 的 GEM buffer manager 在 libdrm 里也有非平凡实现。
- **wl_drm**：Mesa 内部用的 Wayland 私有协议，负责 Wayland client 与 compositor 之间的 buffer 分享，作用上非常像 DRI3，两者的存在本身就说明"命名没收敛、事情都在重复发明"。
- **分层动因**：大多数驱动代码在用户态而非内核态，是因为 (a) GLSL→TGSI→机器码编译器太大不适合进内核、(b) 崩溃不拖系统、(c) 升级驱动无需重启内核、(d) 开发调试可直接 LD_LIBRARY_PATH 切换驱动。
- **Gallium3D**：Mesa 里一套构建驱动的公共基础设施，Intel 以外的家族都在用；Intel 因为有自建 stack 与历史包袱，选择不走 Gallium。

## 链接到的概念

- [[linux-graphics-stack-dri]]（本次新增）
- [[jasper-st-pierre]]
- [[gpu-hazard-tracking]] —— 用户态驱动为什么能做得这么重：见 DRM 把底层 ioctl 下沉、上层留给 Mesa

## 原文

- 链接：<https://blog.mecheye.net/2016/01/dri/>
- 本地：`raw/articles/blog.mecheye.net/2016-01-19_dri.md`
